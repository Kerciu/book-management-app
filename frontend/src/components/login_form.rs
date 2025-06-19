use anyhow::anyhow;
use leptos::prelude::*;
use log::Level;
use serde::Serialize;
use leptos_router::hooks::*;

use crate::components::send_post_request;
use crate::auth::email::Token as AuthToken;

#[derive(Serialize, Clone, Copy, Default)]
/// contains items necesary to send request
struct LoginRequest {
    email: RwSignal<String>,
    password: RwSignal<String>,
}

#[derive(Debug, Clone)]
enum LoginResponse {
    /// Request successful, contains token
    Token(AuthToken),
    /// Response received, contains error
    Err(String),
    /// Didn't receive valid response
    NoResponse,
    /// Didn't send request
    NoRequest,
    /// Waiting for response
    Waiting,
}

async fn post(data: LoginRequest) -> anyhow::Result<LoginResponse> {
    const ENDPOINT: &str = "/api/auth/login/";
    let res = send_post_request(data, ENDPOINT).await?;

    if res.ok() {
        let res: serde_json::Value = res.json().await?;
        let token = res
            .get("user")
            .ok_or(anyhow!("Response malformed, can't find parameter \"user\""))?
            .get("access")
            .ok_or(anyhow!(
                "Response malformed, cant' find parameter \"user.access\""
            ))?;
        let token = token
            .as_str()
            .ok_or(anyhow!("user.access - expected String, got {:?}", token))?
            .to_string();
        return Ok(LoginResponse::Token(AuthToken::new(token)));
    } else {
        let res: serde_json::Value = res.json().await?;
        let error = res.get("detail").ok_or(anyhow!(
            "response malformed, can't find parameter \"detail\""
        ))?;
        let error = error
            .as_str()
            .ok_or(anyhow!("detail - expected String, got {:?}", error))?
            .to_string();
        return Ok(LoginResponse::Err(error));
    }
}

#[component]
pub fn login_form() -> impl IntoView {
    let navigate = use_navigate();

    let request = LoginRequest::default();

    let send_request = move |request: &LoginRequest| {
        let request = request.clone();
        async move { post(request).await }
    };
    let send_request = Action::new_unsync(send_request);

    let response = move || {
        if send_request.pending().get() {
            return LoginResponse::Waiting;
        }

        let maybe_result = &*send_request.value().read();
        match maybe_result {
            Some(result) => match result {
                Ok(response) => response.clone(),
                Err(err) => {
                    log::log!(Level::Error, "{err}");
                    LoginResponse::NoResponse
                }
            },
            None => LoginResponse::NoRequest,
        }
    };

    let response_display = move || match response() {
        LoginResponse::Token(_) => "Log In successful".to_string(),
        LoginResponse::Err(err) => err,
        LoginResponse::NoResponse => "Something went wrong, try again".to_string(),
        LoginResponse::NoRequest => "".to_string(),
        LoginResponse::Waiting => "".to_string(),
    };

    Effect::new(move || {
        if let LoginResponse::Token(token) = response() {
            provide_context(token);
            navigate("/books/list", Default::default());
        }
    });

    view! {
        <form>
            <div>
                <input type="email" placeholder="Email" bind:value=request.email required />
            </div>
            <div style="margin-top=12px;">
                <input type="password" placeholder="Password" bind:value=request.password required />
            </div>
            <div class="container-flex" style="padding: 0px; align-items: center; justify-content: center;">
                <input type="button" class="button-squash" on:click=move |_| {
                    send_request.dispatch(request);
                } value="Log in" />
            </div>
        </form>
        <div class="container-flex" style="padding: 0px; align-items: center; justify-content: center;">
            <div class="body-text" style="color: #d6b5dc; text-align: center; margin-top: 20px;">
                {response_display}
            </div>
        </div>
    }
}
