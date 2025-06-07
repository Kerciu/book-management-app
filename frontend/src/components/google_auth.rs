use crate::auth;
use leptos::prelude::*;
use leptos_router::hooks::use_query;
use leptos_router::params::Params;
use log::Level;
use serde::{Deserialize, Serialize};

use super::send_post_request;

#[derive(PartialEq, Params)]
struct AuthData {
    code: Option<String>,
    state: Option<String>,
}

#[derive(Serialize, Debug)]
struct AuthRequest {
    access_token: String,
}

#[derive(Deserialize)]
struct AuthResponse;

#[component]
pub fn google_auth_button() -> impl IntoView {
    view! { <button on:click=move |_| auth::google::init()>"Google OAuth"</button> }
}

async fn post(access_token: String) -> anyhow::Result<AuthResponse> {
    let res = send_post_request(AuthRequest { access_token }, "/api/auth/google-auth/")
        .await?
        .json()
        .await?;
    Ok(res)
}

#[component]
pub fn google_auth_handler() -> impl IntoView {
    let params = use_query::<AuthData>();

    Effect::new(move || match &*params.read() {
        Ok(AuthData {
            code: Some(code),
            state: Some(state),
        }) if *state
            == web_sys::window()
                .unwrap()
                .local_storage()
                .unwrap()
                .unwrap()
                .get_item("google_oauth_state")
                .unwrap()
                .unwrap_or_default() =>
        {
            let code = code.clone();
            let _ = LocalResource::new(move || post(code.clone()));
        }
        Err(err) => log::log!(Level::Error, "{err}"),
        _ => log::log!(Level::Error, "bad params in url querry"),
    });

    view! {}
}
