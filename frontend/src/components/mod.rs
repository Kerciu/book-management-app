mod book_details;
mod book_list;
mod email_resend_form;
mod email_verify_form;
mod friends_list;
mod github_auth;
mod google_auth;
mod login_form;
mod registraction_form;
mod recommendation_list;
mod review;
mod review_input;
mod review_list;
mod shelves_list;

pub use book_details::BookDetails;
pub use book_list::{BookList, get_example_book};
pub use email_verify_form::EmailVerificationForm;
pub use friends_list::FriendList;
pub use github_auth::{GithubAuthButton, GithubAuthHandler};
pub use login_form::LoginForm;
pub use registraction_form::RegistractionForm;
pub use recommendation_list::BookReccomendationList;
pub use review_list::ReviewList;
pub use review_input::ReviewInput;
pub use shelves_list::{ShelvesList, put_book_in_shelf, get_shelves};

use crate::{BACKEND, auth};
use gloo_net::http::{Request, Response};
use leptos::prelude::*;
use serde::de::DeserializeOwned;

/// Utility function to send POST requests as JSON
async fn send_post_request(
    data: impl serde::Serialize,
    endpoint: &str,
) -> anyhow::Result<Response> {
    let endpoint = format!("{BACKEND}{endpoint}");
    let body = serde_json::to_string(&data)?;
    let mut request = Request::post(&endpoint).header("Content-Type", "application/json");
    if let Some(token) = use_context::<auth::Token>() {
        request = request.header("Authorization", &format!("Bearer {}", &token as &str))
    }
    let response = request.body(body)?.send().await?;
    Ok(response)
}

async fn send_delete_request(endpoint: &str) -> anyhow::Result<()> {
    let endpoint = format!("{BACKEND}{endpoint}");
    let mut request = Request::delete(&endpoint).header("Content-Type", "application/json");
    if let Some(token) = use_context::<auth::Token>() {
        request = request.header("Authorization", &format!("Bearer {}", &token as &str))
    }
    let _ = request.send().await?;
    Ok(())
}

async fn send_get_request<'a, T>(endpoint: &str) -> anyhow::Result<T>
where
    T: DeserializeOwned,
{
    let endpoint = format!("{BACKEND}{endpoint}");
    let mut request = Request::get(&endpoint).header("Content-Type", "application/json");
    if let Some(token) = use_context::<auth::Token>() {
        request = request.header("Authorization", &format!("Bearer {}", &token as &str))
    }
    let response = request.send().await?;
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
