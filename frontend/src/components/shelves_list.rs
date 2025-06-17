use leptos::prelude::*;
use serde::Deserialize;
use serde_json::json;
use anyhow::anyhow;
use crate::components::{book_list::Book, send_get_request, send_post_request};


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

async fn put_book_in_shelf(book_id: usize, shelf_id: usize) -> anyhow::Result<()> {
    let endpoint= format!("/api/shelf/shelves/{shelf_id}/add_book");
    let request = json!({"id": book_id});

    let response = send_post_request(request, &endpoint).await?;

    if response.ok() {
        Ok(())
    } else {
        Err(anyhow!(response.text().await?))
    }
}
async fn remove_book_from_shelf(book_id: usize, shelf_id: usize) -> anyhow::Result<()> {
    let endpoint= format!("/api/shelf/shelves/{shelf_id}/remove_book");
    let request = json!({"id": book_id});

    let response = send_post_request(request, &endpoint).await?;

    if response.ok() {
        Ok(())
    } else {
        Err(anyhow!(response.text().await?))
    }
}

async fn get_books_from_shelf(shelf_id: usize) -> anyhow::Result<Vec<Book>> {
    todo!()
}

#[component]
pub fn shelves_list() -> impl IntoView {

}