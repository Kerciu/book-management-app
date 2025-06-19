use leptos::prelude::*;
use leptos_router::hooks::{use_navigate, use_params, use_params_map};
use serde::Deserialize;
use serde_json::json;
use anyhow::anyhow;
use crate::components::{book_list::Book, handle_request, send_get_request, send_post_request};
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

pub async fn put_book_in_shelf((book_id, shelf_id): (usize, usize)) -> anyhow::Result<()> {
    let endpoint= format!("/api/shelf/shelves/{shelf_id}/add_book/");
    let request = json!({"book_id": book_id});

    let response = send_post_request(request, &endpoint).await?;

    if response.ok() {
        Ok(())
    } else {
        Err(anyhow!(response.text().await?))
    }
}
pub async fn remove_book_from_shelf(book_id: usize, shelf_id: usize) -> anyhow::Result<()> {
    let endpoint= format!("/api/shelf/shelves/{shelf_id}/remove_book/");
    let request = json!({"id": book_id});

    let response = send_post_request(request, &endpoint).await?;

    if response.ok() {
        Ok(())
    } else {
        Err(anyhow!(response.text().await?))
    }
}

async fn get_books_from_shelf(shelf_id: usize) -> anyhow::Result<Vec<Book>> {
    let endpoint = format!("/api/shelf/shelves/{shelf_id}/books/");
    return send_get_request(&endpoint).await;
}

#[component]
pub fn shelves_list() -> impl IntoView {
    let shelves = LocalResource::new(move || get_shelves());
    let shelves = move || match &*shelves.read() {
        Some(Ok(res)) => res.clone(),
        // TODO: Error handling
        _ => Default::default(),
    };

    let (shelf_id, set_shelf_id) = signal(None);

    view! {
        <For
            each=move || shelves()
            key=|shelf| shelf.id
            children=move |shelf| {
                view! {
                    <button on:click=move |_| set_shelf_id(Some(shelf.id))></button>
                }
            }
        />
        {move || shelf_id().map(|id| view! { <ShelfBookList shelf_id=id.into() />})}
    }
}

#[component]
pub fn shelf_select() -> impl IntoView {
    let navigate = use_navigate();
    let book_id = move || use_params_map().read().get("book_id").unwrap().parse::<usize>().unwrap();
    let shelves = LocalResource::new(move || get_shelves());
    let shelves = move || match &*shelves.read() {
        Some(Ok(res)) => res.clone(),
        // TODO: Error handling
        _ => Default::default(),
    };
    let shelves = move || shelves().into_iter().map(move |s| (book_id(), s));
    let action = handle_request(&put_book_in_shelf);

    view! {
        <For
            each=move || shelves()
            key=|(_, shelf)| shelf.id
            children=move |(book_id, shelf)| {
                let navigate = navigate.clone();
                view! {
                    <button on:click=move |_| { action.dispatch((book_id, shelf.id.clone())); navigate("/main", Default::default()); }>{move || shelf.name.clone()}</button>
                }
            }
        />
    }
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