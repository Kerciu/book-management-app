use anyhow::anyhow;
use leptos::prelude::*;
use log::Level;
use serde::Serialize;

use super::send_post_request;

#[derive(Serialize, Clone, Copy, Default)]
/// contains items necesary to send request
struct RegisterRequest {
    email: RwSignal<String>,
    first_name: RwSignal<String>,
    last_name: RwSignal<String>,
    password: RwSignal<String>,
    re_password: RwSignal<String>,
}

#[derive(Debug, Clone)]
/// Errors that may be returned from request
enum ValidationError {
    Email(String),
    Password(String),
    RePassword(String),
    FirstName(String),
    LastName(String),
}

#[derive(Debug, Clone)]
/// Representation of Request's status
enum RegisterResponse {
    /// Request successful
    Ok,
    /// Didn't receive valid response
    NoResponse,
    /// Didn't send request
    NoRequest,
    /// Waiting for response
    Waiting,
    /// Response received, contains errors
    Err(Vec<ValidationError>),
}

async fn post(data: RegisterRequest) -> anyhow::Result<RegisterResponse> {
    const ENDPOINT: &str = "/api/auth/register/";
    let res = send_post_request(data, ENDPOINT).await?;

    if res.ok() {
        return Ok(RegisterResponse::Ok);
    } else {
        let res: serde_json::Value = res.json().await?;
        let res = res.as_object().ok_or(anyhow!("Empty Response"))?;
        let mut ret = Vec::new();

        if res
            .iter()
            .any(|(key, _)| !["email", "password", "re_password"].contains(&key.as_str()))
        {
            return Err(anyhow!(
                "Invalid resposce: unexpected keys. Content:\n{res:?}"
            ));
        }

        for (key, value) in res {
            let array = value
                .as_array()
                .ok_or(anyhow!("Exepected Array, got {:?}", value))?;
            for value in array {
                let value = value
                    .as_str()
                    .ok_or(anyhow!("Exepected String, got {:?}", value))?
                    .to_string();
                ret.push(match key.as_str() {
                    "email" => ValidationError::Email(value),
                    "password" => ValidationError::Password(value),
                    "re_password" => ValidationError::RePassword(value),
                    _ => unreachable!(),
                });
            }
        }

        return Ok(RegisterResponse::Err(ret));
    }
}

#[component]
pub fn registraction_form() -> impl IntoView {
    let request = RegisterRequest::default();

    let send_request = move |request: &RegisterRequest| {
        let request = request.clone();
        async move { post(request).await }
    };
    let send_request = Action::new_unsync(send_request);
    let response = move || {
        if send_request.pending().get() {
            return RegisterResponse::Waiting;
        }

        let t = &*send_request.value().read();
        match t {
            Some(result) => match result {
                Ok(response) => response.clone(),
                Err(err) => {
                    log::log!(Level::Error, "{err}");
                    RegisterResponse::NoResponse
                }
            },
            None => RegisterResponse::NoRequest,
        }
    };

    let response_display = move || match response() {
        RegisterResponse::Ok => "Registration Successful",
        RegisterResponse::NoResponse => "Something went wrong, try again",
        RegisterResponse::NoRequest => "",
        RegisterResponse::Waiting => "Waiting for server",
        RegisterResponse::Err(_) => "Registration failed",
    };

    let form_email = move || {
        view! {
            <div>
                <label>"E-mail"</label>
                <input type="email" bind:value=request.email required />
                <p>
                {move ||
                    if let RegisterResponse::Err(arr) = response()
                    && let Some(ValidationError::Email(error)) = arr
                        .iter()
                        .find(|i| matches!(i, ValidationError::Email(_))) {
                        error.clone()
                    } else {
                        "".to_string()
                    }
                }
                </p>
            </div>
        }
    };

    let form_password = move || {
        view! {
            <div>
                <label>"Password"</label>
                <input type="password" bind:value=request.password required />
                <p>
                {move ||
                    if let RegisterResponse::Err(arr) = response()
                    && let Some(ValidationError::Password(error)) = arr
                        .iter()
                        .find(|i| matches!(i, ValidationError::Password(_))) {
                        error.clone()
                    } else {
                        "".to_string()
                    }
                }
                </p>
            </div>
        }
    };

    let form_repassword = move || {
        view! {
            <div>
                <label>"Repeat Password"</label>
                <input type="password" bind:value=request.re_password required />
                <p>
                {move ||
                    if let RegisterResponse::Err(arr) = response()
                    && let Some(ValidationError::RePassword(error)) = arr
                        .iter()
                        .find(|i| matches!(i, ValidationError::RePassword(_))) {
                        error.clone()
                    } else {
                        "".to_string()
                    }
                }
                </p>
            </div>
        }
    };

    view! {
        <form>
            { form_email }
            <div>
                <label>"First Name"</label>
                <input type="text" bind:value=request.first_name required />
            </div>
            <div>
                <label>"Last Name"</label>
                <input type="text" bind:value=request.last_name required />
            </div>
            { form_password }
            { form_repassword }

            <input type="button" on:click=move |_| {
                send_request.dispatch(request);
            } value="Register" />
        </form>
        <p>
        {response_display}
        </p>
    }
}
