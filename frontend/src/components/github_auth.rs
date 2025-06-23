use crate::auth::{self, Token};
use anyhow::anyhow;
use leptos::prelude::*;
use leptos_router::hooks::{use_navigate, use_query_map};
use leptos_router::params::{Params, ParamsMap};
use log::Level;
use serde::{Deserialize, Serialize};

use super::send_post_request;

#[derive(PartialEq, Params, Debug)]
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
    code: String,
}

#[component]
pub fn github_auth_button() -> impl IntoView {
    view! { <button on:click=move |_| auth::github::init()>"Github OAuth"</button> }
}

async fn post(code: String) -> anyhow::Result<AuthResponse> {
    provide_context::<Option<Token>>(None);
    let _ = web_sys::window()
        .unwrap()
        .local_storage()
        .unwrap()
        .unwrap()
        .remove_item("access_token");
    let res = send_post_request(AuthRequest { code }, "/api/auth/github-auth/").await?;
    if !res.ok() {
        return Err(anyhow!("{}", res.status_text()));
    }
    let res: serde_json::Value = serde_json::from_str(&res.text().await?)?;
    let code = res["code"]["access"]
        .to_string()
        .trim_matches('"')
        .to_string();
    let _ = web_sys::window()
        .unwrap()
        .local_storage()
        .unwrap()
        .unwrap()
        .set_item("access_token", &code.clone());
    Ok(AuthResponse { code })
}

#[component]
pub fn github_auth_handler() -> impl IntoView {
    let params_map = move || use_query_map();
    let params = move || AuthData {
        code: params_map().read().get("code"),
        state: params_map().read().get("state"),
    };

    let code = move || match params() {
        AuthData {
            code: Some(code),
            state: Some(state),
        } if *state
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
        x => {
            log::log!(Level::Error, "{x:?}");
            None
        }
    };

    let code = LocalResource::new(move || post(code().unwrap_or_default()));
    Effect::new(move || {
        if let Some(Ok(AuthResponse { code })) = &*code.read() {
            provide_context(Some(auth::github::Token::new(code.clone())));
            use_navigate()("/main", Default::default());
        }
    });
    Effect::new(move || log::log!(Level::Debug, "{:?}", use_context::<auth::github::Token>()));

    view! {}
}
