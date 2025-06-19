use leptos::prelude::*;
use log::Level;
use serde::Serialize;

use crate::components::{handle_request, send_post_request};

#[derive(Serialize, Clone, Debug, Default, Copy)]
struct EmailResendRequest {
    email: RwSignal<String>,
}

#[derive(Clone, Debug)]
enum EmailResendResponse {
    /// Account verified
    Ok,
    /// Unknown error
    Err(String),
    Waiting,
    NoRequest,
    NoResponse,
}

async fn post(request: EmailResendRequest) -> anyhow::Result<EmailResendResponse> {
    const ENDPOINT: &str = "/api/resend-email/";
    let res = send_post_request(request, ENDPOINT).await?;

    // HTTP Codes
    Ok(match res.status() {
        200 => EmailResendResponse::Ok,
        _ => EmailResendResponse::Err(res.text().await?),
    })
}

#[component]
pub fn EmailResendForm() -> impl IntoView {
    let request = EmailResendRequest::default();
    let send_request = handle_request(&post);
    let response = move || {
        if send_request.pending().get() {
            return EmailResendResponse::Waiting;
        }

        let maybe_result = &*send_request.value().read();
        match maybe_result {
            Some(res) => match res {
                Ok(res) => res.clone(),
                Err(err) => {
                    log::log!(Level::Error, "{err}");
                    EmailResendResponse::NoResponse
                }
            },
            None => EmailResendResponse::NoRequest,
        }
    };

    let response_display = move || match response() {
        EmailResendResponse::Ok => "Email verified successfully".to_string(),
        EmailResendResponse::Err(err) => format!("error: {err}"),
        EmailResendResponse::Waiting => "Waiting for server".to_string(),
        EmailResendResponse::NoRequest => "".to_string(),
        EmailResendResponse::NoResponse => "Something went wrong, try again".to_string(),
    };

    view! {
        <p>
            "Type your email to resend verification code"
        </p>
        <form>
            <div>
                <label>"E-mail"</label>
                <input type="email" bind:value=request.email required />
            </div>
            <input type="button" on:click=move |_| {
                send_request.dispatch(request);
            } value="Submit" />
        </form>
        <p>
            {response_display}
        </p>
    }
}
