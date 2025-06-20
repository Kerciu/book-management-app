use anyhow::anyhow;
use leptos::prelude::*;
use leptos_router::hooks::use_navigate;
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
    let navigate = use_navigate();

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
                Ok(response) => {
                    response.clone()
                },
                Err(err) => {
                    log::log!(Level::Error, "{err}");
                    RegisterResponse::NoResponse
                }
            },
            None => RegisterResponse::NoRequest,
        }
    };

    let _response_display = move || match response() {
        RegisterResponse::Ok => "Registration successful",
        RegisterResponse::NoResponse => "Something went wrong, try again",
        RegisterResponse::NoRequest => "",
        RegisterResponse::Waiting => "",
        RegisterResponse::Err(_) => "Registration failed",
    };

    Effect::new(move || if matches!(response(), RegisterResponse::Ok) {
        navigate("/verify_email", Default::default());
    });

    let (error_msg, set_error_msg): (ReadSignal<String>, WriteSignal<String>) = signal("".to_string());
    let (show_error_msg, set_show_error_msg) = signal(false);

    // TODO: Can we write a macro to not repeat the form's fields?
    //       Should we?
    view! {
        <form>
            <div>
                <input type="text" placeholder="Username" bind:value=request.username required />
                <p>
                {move ||
                    if let RegisterResponse::Err(arr) = response()
                    && let Some(ValidationError::Username(error)) = arr
                        .iter()
                        .find(|i| matches!(i, ValidationError::Username(_))) {
                        set_error_msg(format!("Username: {}", error.to_string()));
                        set_show_error_msg(true);
                    } else {
                     }
                }
                </p>
            </div>
            <div>
                <input type="email" placeholder="Email" bind:value=request.email required />
                <p>
                {move ||
                    if let RegisterResponse::Err(arr) = response()
                    && let Some(ValidationError::Email(error)) = arr
                        .iter()
                        .find(|i| matches!(i, ValidationError::Email(_))) {
                        set_error_msg(format!("Email: {}", error.to_string()));
                        set_show_error_msg(true);
                    } else {
                    }
                }
                </p>
            </div>
            <div>
                <input type="text" placeholder="First name" bind:value=request.first_name required />
                <p>
                {move ||
                    if let RegisterResponse::Err(arr) = response()
                    && let Some(ValidationError::FirstName(error)) = arr
                        .iter()
                        .find(|i| matches!(i, ValidationError::FirstName(_))) {
                        set_error_msg(format!("First name: {}", error.to_string()));
                        set_show_error_msg(true);
                    } else {
                    }
                }
                </p>
            </div>
            <div>
                <input type="text" placeholder="Last name" bind:value=request.last_name required />
                <p>
                {move ||
                    if let RegisterResponse::Err(arr) = response()
                    && let Some(ValidationError::LastName(error)) = arr
                        .iter()
                        .find(|i| matches!(i, ValidationError::LastName(_))) {
                        set_error_msg(format!("Last name: {}", error.to_string()));
                        set_show_error_msg(true);
                    } else {
                    }
                }
                </p>
            </div>
            <div>
                <input type="password" placeholder="Password" bind:value=request.password required />
                <p>
                {move ||
                    if let RegisterResponse::Err(arr) = response()
                    && let Some(ValidationError::Password(error)) = arr
                        .iter()
                        .find(|i| matches!(i, ValidationError::Password(_))) {
                        set_error_msg(format!("Password: {}", error.to_string()));
                        set_show_error_msg(true);
                    } else {
                    }
                }
                </p>
            </div>
            <div>
                <input type="password" placeholder="Repeat password" bind:value=request.re_password required />
                <p>
                {move ||
                    if let RegisterResponse::Err(arr) = response()
                    && let Some(ValidationError::RePassword(error)) = arr
                        .iter()
                        .find(|i| matches!(i, ValidationError::RePassword(_))) {
                        set_error_msg(format!("Repeat Password: {}", error.to_string()));
                        set_show_error_msg(true);
                    } else {
                    }
                }
                </p>
            </div>
            <div class="container-flex" style="padding: 0px; align-items: center; justify-content: center;">
                <input type="button" class="button-squash" on:click=move |_| {
                    send_request.dispatch(request);
                } value="Register" />
            </div>
            <Show when=move || !show_error_msg.get() fallback=move || 
                    view! {
                        <div class="body-text" style="color: #d6b5dc; text-align: center; margin-top: 10px">{error_msg.get()}</div>
                    }
                > 
                <div></div>
            </Show>
        </form>

    }
}
