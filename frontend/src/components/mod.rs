mod book_info;
mod category_select_list;
mod login_form;
mod registraction_form;
mod book_details;
mod book_list;
mod friends_list;
// mod reviews;
// pub use reviews::Reviews;
pub use book_list::BookList;
use leptos::prelude::Action;
pub use login_form::LoginForm;
pub use registraction_form::RegistractionForm;
pub use friends_list::FriendList;
pub use book_details::BookDetails;

use crate::BACKEND;
pub use category_select_list::CategorySelectList;
use gloo_net::http::{Request, Response};
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
