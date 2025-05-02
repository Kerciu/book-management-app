pub mod registraction_form;
pub mod login_form;

pub use registraction_form::*;

use gloo_net::http::{Request, Response};
use crate::BACKEND;


/// Utility function to send POST requests as JSON
pub async fn send_post_request(data: impl serde::Serialize, endpoint: &str) -> anyhow::Result<Response> {
    let endpoint = format!("{BACKEND}{endpoint}");
    let body = serde_json::to_string(&data)?;
    let response = Request::post(&endpoint)
        .header("Content-Type", "application/json")
        .body(body)?
        .send()
        .await?;
    Ok(response)
}