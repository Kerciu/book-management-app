use crate::auth;
use anyhow::anyhow;
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
    code: String,
}

#[derive(Deserialize)]
struct AuthResponse {
    code: String
}

#[component]
pub fn github_auth_button() -> impl IntoView {
    view! { <button on:click=move |_| auth::github::init()>"Github OAuth"</button> }
}

async fn post(code: String) -> anyhow::Result<AuthResponse> {
    let res = send_post_request(AuthRequest { code }, "/api/auth/github-auth/")
        .await?;
    if !res.ok() {
        return Err(anyhow!("{}", res.status_text()))
    }
    Ok(res.json().await?)
}

#[component]
pub fn github_auth_handler() -> impl IntoView {
    let params = use_query::<AuthData>();

    let code = move || match &*params.read() {
        Ok(AuthData {
            code: Some(code),
            state: Some(state),
        }) if *state
            == web_sys::window()
                .unwrap()
                .local_storage()
                .unwrap()
                .unwrap()
                .get_item("github_oauth_state")
                .unwrap()
                .unwrap_or_default() =>
        {
            Some(code.clone())
        }
        Err(err) => {log::log!(Level::Error, "{err}"); None},
        _ => {log::log!(Level::Error, "bad params in url querry"); None},
    };

    let code = LocalResource::new(move || post(code().unwrap_or_default()));
    let code = move || code.read().as_ref().unwrap().as_ref().unwrap().code.clone();
    Effect::new(move || provide_context(auth::github::Token(code())));
    Effect::new(move || log::log!(Level::Debug, "{:?}", use_context::<auth::github::Token>()));

    view! {}
}
