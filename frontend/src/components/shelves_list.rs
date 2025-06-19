use leptos::prelude::*;
use serde::Deserialize;
use serde_json::json;
use anyhow::anyhow;
use crate::components::{book_list::Book, send_get_request, send_post_request};
use log::Level;

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
    let endpoint = format!("/api/shelf/shelves/{shelf_id}/books");
    return send_get_request(&endpoint).await;
}

#[component]
pub fn shelves_list() -> impl IntoView {

}

#[component]
pub fn shelf_book_list(shelf_id: Signal<usize>) -> impl IntoView {
    let books = LocalResource::new(move || get_books_from_shelf(shelf_id()));
    let books = move || match &*books.read() {
        Some(res) => match res {
            Ok(vec) => vec.clone(),
            Err(err) => {
                log::log!(Level::Error, "{err}");
                Default::default()
            }
        },
        None => Default::default(),
    };
}