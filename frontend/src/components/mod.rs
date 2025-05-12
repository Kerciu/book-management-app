pub mod registraction_form;
pub mod login_form;
pub mod book_list;

use gloo_net::http::{Request, Response};
use serde::{de::DeserializeOwned, Deserialize};
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

pub async fn send_get_request<'a, T>(endpoint: &str) -> anyhow::Result<T>
where
    T: DeserializeOwned
{
    let endpoint = format!("{BACKEND}{endpoint}");
    let response = Request::get(&endpoint)
        .header("Content-Type", "application/json")
        .send()
        .await?;
    Ok(response.json().await?)
}