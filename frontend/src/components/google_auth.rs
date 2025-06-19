use crate::auth::{self, Token};
use leptos::prelude::*;
use leptos_router::hooks::{use_navigate, use_query};
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
    id_token: String,
}

#[derive(Deserialize)]
struct AuthResponse {
    code: String
}

#[component]
pub fn google_auth_button() -> impl IntoView {
    view! { <button on:click=move |_| auth::google::init()>"Google OAuth"</button> }
}

async fn post(access_token: String) -> anyhow::Result<AuthResponse> {
    provide_context::<Option<Token>>(None);
    let res = send_post_request(AuthRequest { id_token: access_token }, "/api/auth/google-auth/")
        .await?;
    if !res.ok() {
        return Err(anyhow::anyhow!("{}", res.status_text()))
    }
    let res: serde_json::Value = serde_json::from_str(&res.text().await?)?;
    Ok(AuthResponse { code: res["user"]["access"].to_string() })
}

#[component]
pub fn google_auth_handler() -> impl IntoView {
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
                .get_item("google_oauth_state")
                .unwrap()
                .unwrap_or_default() =>
        {
            Some(code.clone())
        }
        Err(err) => {log::log!(Level::Error, "{err}"); None},
        _ => {log::log!(Level::Error, "bad params in url querry"); None},
    };

    let code = LocalResource::new(move || post(code().unwrap_or_default()));
    Effect::new(move || if let Some(Ok(AuthResponse { code })) = &*code.read() {
        provide_context(Some(auth::google::Token::new(code.clone())));
        use_navigate()("/books/list", Default::default());
    });
    Effect::new(move || log::log!(Level::Debug, "{:?}", use_context::<auth::github::Token>()));

    view! {}
}
