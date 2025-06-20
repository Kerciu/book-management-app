use leptos::prelude::*;
use log::Level;
use serde::Serialize;

use crate::components::{handle_request, send_post_request};

#[derive(Serialize, Clone, Debug, Default, Copy)]
struct EmailVerifyRequest {
    email: RwSignal<String>,
    otp: RwSignal<String>,
}

#[derive(Clone, Debug)]
enum EmailVerifyResponse {
    /// Account verified
    Ok,
    /// Invalid OTP
    Err,
    /// Account already verified
    AlreadyVerified,
    Waiting,
    NoRequest,
    NoResponse,
}

async fn post(request: EmailVerifyRequest) -> anyhow::Result<EmailVerifyResponse> {
    const ENDPOINT: &str = "/api/auth/verify-user/";
    let res = send_post_request(request, ENDPOINT).await?;

    // HTTP Codes
    Ok(match res.status() {
        200 => EmailVerifyResponse::Ok,
        208 => EmailVerifyResponse::AlreadyVerified,
        404 => EmailVerifyResponse::Err,
        _ => unreachable!(),
    })
}

#[component]
pub fn EmailVerificationForm() -> impl IntoView {
    let request = EmailVerifyRequest::default();
    let send_request = handle_request(&post);
    let response = move || {
        if send_request.pending().get() {
            return EmailVerifyResponse::Waiting;
        }

        let maybe_result = &*send_request.value().read();
        match maybe_result {
            Some(res) => match res {
                Ok(res) => res.clone(),
                Err(err) => {
                    log::log!(Level::Error, "{err}");
                    EmailVerifyResponse::NoResponse
                }
            },
            None => EmailVerifyResponse::NoRequest,
        }
    };

    let response_display = move || match response() {
        EmailVerifyResponse::Ok => "Email verified successfully",
        EmailVerifyResponse::Err => "Email and OTP code does not match",
        EmailVerifyResponse::AlreadyVerified => "This email is already verified",
        EmailVerifyResponse::Waiting => "Waiting for server",
        EmailVerifyResponse::NoRequest => "",
        EmailVerifyResponse::NoResponse => "Something went wrong, try again",
    };

    view! {
        <div class="container">
            <div class="centered-box-email">
               <div class="form-wrapper">
             
                    <form>
                        <div>
                            <label>"E-mail"</label>
                            <input type="email" bind:value=request.email placeholder="Email" required  class="input-email"/>
                        </div>
                        <div>
                            <label>"Code"</label>
                            <input type="number" bind:value=request.otp placeholder="Code" required class="input-email" />
                        </div>
                        <input type="button" on:click=move |_| {
                            send_request.dispatch(request);
                        } value="Submit" />

                    </form>
                    <p>
                        {response_display}
                    </p>
                </div>
            </div>
        </div>
    }
}
