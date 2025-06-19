mod book_details;
mod book_list;
mod email_resend_form;
mod email_verify_form;
mod friends_list;
mod google_auth;
mod login_form;
mod registraction_form;
mod github_auth;
mod review;
mod review_list;

pub use github_auth::{GithubAuthButton, GithubAuthHandler};
pub use book_details::BookDetails;
pub use book_list::BookList;
pub use email_verify_form::EmailVerificationForm;
pub use friends_list::FriendList;
pub use login_form::LoginForm;
pub use registraction_form::RegistractionForm;

use crate::{auth, BACKEND};
use gloo_net::http::{Request, Response};
use leptos::prelude::*;
use serde::{Deserialize, de::DeserializeOwned};

/// Utility function to send POST requests as JSON
async fn send_post_request(
    data: impl serde::Serialize,
    endpoint: &str,
) -> anyhow::Result<Response> {
    let endpoint = format!("{BACKEND}{endpoint}");
    let body = serde_json::to_string(&data)?;
    let response = Request::post(&endpoint)
        .header("Content-Type", "application/json")
        .header("Authorization", &format!("Bearer {}", &use_context::<auth::Token>().unwrap_or_default() as &str))
        .body(body)?
        .send()
        .await?;
    Ok(response)
}

async fn send_get_request<'a, T>(endpoint: &str) -> anyhow::Result<T>
where
    T: DeserializeOwned,
{
    let endpoint = format!("{BACKEND}{endpoint}");
    let response = Request::get(&endpoint)
        .header("Content-Type", "application/json")
        .header("Authorization", &format!("Bearer {}", &use_context::<auth::Token>().unwrap_or_default() as &str))
        .send()
        .await?;
    Ok(response.json().await?)
}

fn handle_request<Req, Res, F, Fu>(handler: &'static F) -> Action<Req, Res>
where
    F: Fn(Req) -> Fu,
    Fu: Future<Output = Res> + 'static,
    Req: Clone + Send + Sync + 'static,
    Res: Send + Sync + 'static,
{
    let handler = move |req: &Req| {
        let req = req.clone();
        async move { handler(req).await }
    };
    Action::new_unsync(handler)
}
