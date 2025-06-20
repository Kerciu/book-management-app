use crate::auth::google::Token;
use crate::auth::{self};
use gloo_net::http::Request;
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
    access_token: String,
}

#[component]
pub fn google_auth_button() -> impl IntoView {
    view! { <button on:click=move |_| auth::google::init()>"Google OAuth"</button> }
}

async fn post(code: String) -> anyhow::Result<AuthResponse> {
    provide_context::<Option<Token>>(None);
    let _ = web_sys::window()
        .unwrap()
        .local_storage()
        .unwrap()
        .unwrap()
        .remove_item("access_token");
    let token = get_id_token(code).await?;
    let res = send_post_request(
        AuthRequest {
            id_token: token.to_string(),
        },
        "/api/auth/google-auth/",
    )
    .await?;
    if !res.ok() {
        return Err(anyhow::anyhow!("{}", res.status_text()));
    }
    let access_token = res.json::<serde_json::Value>().await?["access"].to_string().trim_matches('"').to_string();
    let _ = web_sys::window()
        .unwrap()
        .local_storage()
        .unwrap()
        .unwrap()
        .set_item("access_token", &access_token.clone());
    Ok(AuthResponse { access_token })
}

async fn get_id_token(code: String) -> anyhow::Result<Token> {
    let data = format!(
        "code={}&redirect_uri={}&client_id={}&client_secret={}&grant_type=authorization_code",
        code,
        env!("GOOGLE_REDIRECT_URI_SIMPLE"),
        env!("GOOGLE_CLIENT_ID"),
        env!("GOOGLE_CLIENT_SECRET")
    );

    let endpoint = env!("GOOGLE_TOKEN_GET_URL");
    let res = Request::post(endpoint)
        .header("content-type", "application/x-www-form-urlencoded")
        .body(data)?
        .send()
        .await?;
    let mut code = res.json::<serde_json::Value>().await?["id_token"].to_string();
    code = code.replace('-', "+");
    code = code.replace('_', "/");
    code = code.trim_matches('"').to_string();
    Ok(Token::new(code))
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
        Err(err) => {
            log::log!(Level::Error, "{err}");
            None
        }
        _ => {
            log::log!(Level::Error, "bad params in url querry");
            None
        }
    };

    let code = LocalResource::new(move || post(code().unwrap_or_default()));
    Effect::new(move || {
        if let Some(Ok(AuthResponse { access_token })) = &*code.read() {
            provide_context(Some(auth::google::Token::new(access_token.clone())));
            use_navigate()("/main", Default::default());
        }
    });

    view! {}
}
