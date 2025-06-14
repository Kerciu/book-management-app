use leptos::prelude::*;
use serde::Deserialize;

use crate::components::send_get_request;


#[derive(Debug, Default, Deserialize, Clone)]
struct ShelvesResponse {
    count: usize,
    next: Option<String>,
    previous: Option<String>,
    results: Vec<Shelf>
}

#[derive(Debug, Default, Deserialize, Clone)]
struct Shelf {
    id: usize,
    user: usize,
    name: String,
    is_default: bool,
    shelf_type: String,
    created_at: String,
    updated_at: String
}

async fn get_shelves() -> anyhow::Result<Vec<Shelf>> {
    const ENDPOINT: &str = "/api/shelf/shelves/";
    let mut res: ShelvesResponse = send_get_request(ENDPOINT).await?;
    let mut ret = vec![res];

    while let Some(ref endpoint) = ret.last().unwrap().next {
        res = send_get_request(endpoint).await?;
        ret.push(res);
    }

    Ok(ret.into_iter().map(|ShelvesResponse {results, ..}| results).flatten().collect())
}

#[component]
pub fn shelves_list() -> impl IntoView {

}