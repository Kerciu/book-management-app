use crate::components::{
    book_list::{Book, Genre}, handle_request, send_get_request, send_post_request, BookInfo
};
use anyhow::anyhow;
use leptos::prelude::*;
use leptos_router::hooks::{use_navigate, use_params_map};
use log::Level;
use serde::Deserialize;
use serde_json::json;

#[allow(dead_code, reason = "Faithful representation of endpoint data")]
#[derive(Debug, Default, Deserialize, Clone)]
struct ShelvesResponse {
    count: usize,
    next: Option<String>,
    previous: Option<String>,
    results: Vec<Shelf>,
}

#[allow(dead_code, reason = "Faithful representation of endpoint data")]
#[derive(Debug, Default, Deserialize, Clone)]
pub struct Shelf {
    pub id: usize,
    user: usize,
    pub name: String,
    is_default: bool,
    shelf_type: String,
    created_at: String,
    updated_at: String,
}

pub async fn get_shelves() -> anyhow::Result<Vec<Shelf>> {
    const ENDPOINT: &str = "/api/shelf/shelves/";
    let mut res: ShelvesResponse = send_get_request(ENDPOINT).await?;
    let mut ret = vec![res];

    while let Some(ref endpoint) = ret.last().unwrap().next {
        res = send_get_request(endpoint).await?;
        ret.push(res);
    }

    Ok(ret
        .into_iter()
        .map(|ShelvesResponse { results, .. }| results)
        .flatten()
        .collect())
}

pub async fn put_book_in_shelf((book_id, shelf_id): (usize, usize)) -> anyhow::Result<()> {
    let endpoint = format!("/api/shelf/shelves/{shelf_id}/add_book/");
    let request = json!({"book_id": book_id});

    let response = send_post_request(request, &endpoint).await?;

    if response.ok() {
        Ok(())
    } else {
        Err(anyhow!(response.text().await?))
    }
}
pub async fn remove_book_from_shelf((book_id, shelf_id): (usize, usize)) -> anyhow::Result<()> {
    let endpoint = format!("/api/shelf/shelves/{shelf_id}/remove_book/");
    let request = json!({"book_id": book_id});

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

#[allow(dead_code, reason = "Faithful representation of endpoint data")]
#[derive(Debug, Default, Deserialize, Clone)]
struct StatsResponse {
    read: usize,
    in_progess: usize,
    want_to_read: usize,
    favourite_genre: Genre
}

async fn get_stats() -> anyhow::Result<serde_json::Value> {
    const ENDPOINT: &str = "/api/stats/stats/";
    send_get_request(ENDPOINT).await
}

#[component]
pub fn shelves_list() -> impl IntoView {
    let shelves = LocalResource::new(move || get_shelves());
    let shelves = move || match &*shelves.read() {
        Some(Ok(res)) => res.clone(),
        // TODO: Error handling
        _ => Default::default(),
    };

    let stats_request = LocalResource::new(move || get_stats());
    let stats = move || match &*stats_request.read() {
        Some(Ok(obj)) => obj.clone(),
        _ => Default::default()
    };

    let stats = move || {
        let mut obj = stats();
        obj["currently_reading"] = obj["in_progress"].clone();
        obj
    };

    view! {
        <div>"Your favourite genre is "{move || {let s = stats()["favourite_genre"]["name"].to_string(); if s == "null" { "unknown".to_string() } else { s }}}</div> 
        <For
            each=move || shelves()
            key=|shelf| shelf.id
            children=move |shelf| {
                let (expanded, set_expanded) = signal(false);
                let toggle = move |_| {
                    set_expanded(!expanded.get());
                };
                view! {
                    <div class="expandable-container">
                        <div style="display: flex;   flex-direction: row; align-items:center; margin-left:20px;">
                            <div class="text-title-home-page" style="color: #FFFFFF; margin-left:0px; margin-top:10px;">{shelf.name.clone()}: {move || stats()[shelf.name.clone().to_ascii_lowercase().replace(" ", "_")].to_string()}</div>
                            <button class="toggle-button" style="margin-left: 20px; border-radius: 100px;" on:click=toggle>
                                {move || if expanded() { "▲" } else { "▼" }}
                            </button>
                        </div>
                        <div class={move || {
                            if expanded() {
                                "expandable-content expanded"
                            } else {
                                "expandable-content"
                            }
                        }}>
                            <div>
                                {move || if expanded() {
                                    Some(view! {
                                        <ShelfBookList shelf_id=shelf.id.into() refetch_stats=Signal::derive(move || stats_request.refetch()) />
                                    })
                                } else {
                                    None
                                }}
                            </div>
                        </div>
                    </div>
                    <div class="divider-horizontal"></div>

                 }
            }
        />
    }
}

#[component]
pub fn shelf_select() -> impl IntoView {
    let navigate = use_navigate();
    let book_id = move || {
        use_params_map()
            .read()
            .get("id")
            .unwrap()
            .parse::<usize>()
            .unwrap()
    };
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

                    <button on:click=move |_| { action.dispatch((book_id, shelf.id.clone())); let _ = web_sys::window()
                .unwrap()
                .local_storage()
                .unwrap()
                .unwrap()
                .set_item("main_section", "my_books"); navigate("/main", Default::default()); }>{move || shelf.name.clone()}</button>
                }
            }
        />
    }
}

#[component]
pub fn shelf_book_list_proxy() -> impl IntoView {
    let id = move || {
        use_params_map()
            .read()
            .get("id")
            .unwrap()
            .parse::<usize>()
            .unwrap()
    };
    return view! {
        <ShelfBookList shelf_id=Signal::derive(move || id()) />
    };
}

#[component]
pub fn shelf_book_list(shelf_id: Signal<usize>, #[prop(optional)] refetch_stats: Signal<()>) -> impl IntoView {
    let books_request = LocalResource::new(move || get_books_from_shelf(shelf_id()));
    let books = move || match &*books_request.read() {
        Some(res) => match res {
            Ok(vec) => vec.clone(),
            Err(err) => {
                log::log!(Level::Error, "{err}");
                Default::default()
            }
        },
        None => Default::default(),
    };

    view! {
        <For
            each=move || books()
            key=|book| book.id
            children=move |book| {
                view! {
                     <BookInfo book=book is_library=true shelf_id=shelf_id() refetch=Signal::derive(move || {books_request.refetch(); refetch_stats()})/>
            }
        }
         />
    }
}
