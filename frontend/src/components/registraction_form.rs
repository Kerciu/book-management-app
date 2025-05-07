use anyhow::anyhow;
use leptos::prelude::*;
use log::Level;
use serde::Serialize;

use super::send_post_request;

#[derive(Serialize, Clone, Copy, Default)]
/// contains items necesary to send request
struct RegisterRequest {
    username: RwSignal<String>,
    email: RwSignal<String>,
    first_name: RwSignal<String>,
    last_name: RwSignal<String>,
    password: RwSignal<String>,
    re_password: RwSignal<String>,
}

#[derive(Debug, Clone)]
/// Errors that may be returned from request
enum ValidationError {
    Username(String),
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

        if res.iter().any(|(key, _)| {
            ![
                "email",
                "password",
                "re_password",
                "username",
                "first_name",
                "last_name",
            ]
            .contains(&key.as_str())
        }) {
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
                    "email" => ValidationError::Email,
                    "password" => ValidationError::Password,
                    "re_password" => ValidationError::RePassword,
                    "username" => ValidationError::Username,
                    "first_name" => ValidationError::FirstName,
                    "last_name" => ValidationError::LastName,
                    _ => unreachable!(),
                }(value));
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

        let maybe_result = &*send_request.value().read();
        match maybe_result {
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
        RegisterResponse::Ok => "Registration successful",
        RegisterResponse::NoResponse => "Something went wrong, try again",
        RegisterResponse::NoRequest => "",
        RegisterResponse::Waiting => "Waiting for server",
        RegisterResponse::Err(_) => "Registration failed",
    };

    // TODO: Can we write a macro to not repeat the form's fields?
    //       Should we?
    view! {
        <form>
            <div>
                <label>"Username"</label>
                <input type="text" bind:value=request.username required />
                <p>
                {move ||
                    if let RegisterResponse::Err(arr) = response()
                    && let Some(ValidationError::Username(error)) = arr
                        .iter()
                        .find(|i| matches!(i, ValidationError::Username(_))) {
                        error.clone()
                    } else {
                        "".to_string()
                    }
                }
                </p>
            </div>
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
            <div>
                <label>"First Name"</label>
                <input type="text" bind:value=request.first_name required />
                <p>
                {move ||
                    if let RegisterResponse::Err(arr) = response()
                    && let Some(ValidationError::FirstName(error)) = arr
                        .iter()
                        .find(|i| matches!(i, ValidationError::FirstName(_))) {
                        error.clone()
                    } else {
                        "".to_string()
                    }
                }
                </p>
            </div>
            <div>
                <label>"Last Name"</label>
                <input type="text" bind:value=request.last_name required />
                <p>
                {move ||
                    if let RegisterResponse::Err(arr) = response()
                    && let Some(ValidationError::LastName(error)) = arr
                        .iter()
                        .find(|i| matches!(i, ValidationError::LastName(_))) {
                        error.clone()
                    } else {
                        "".to_string()
                    }
                }
                </p>
            </div>
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
            <input type="button" on:click=move |_| {
                send_request.dispatch(request);
            } value="Register" />
        </form>
        <p>
            {response_display}
        </p>
    }
}
