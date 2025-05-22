// TODO: Remove this later
#![allow(dead_code, reason = "Testing")]
use leptos::prelude::*;
use log::Level;
use serde::{Deserialize, Serialize};

use super::Reviews;
use crate::components::send_get_request;

// INFO: Copied from `book_list.rs`, should we move both
//       versions to common space?
//       vvvvv COPIED vvvvv
#[derive(Deserialize, Debug, Clone)]
struct Author {
    first_name: String,
    middle_name: String,
    last_name: String,
    bio: String,
    birth_date: String,
    death_date: String,
}

#[derive(Deserialize, Debug, Clone)]
struct Genre {
    name: String,
}

#[derive(Deserialize, Debug, Clone)]
struct Book {
    genres: Vec<Genre>,
    authors: Vec<Author>,
    page_count: usize,
    title: String,
    description: String,
    isbn: String,
    published_at: String,
    language: String,
}

#[derive(Deserialize, Debug, Clone)]
struct BookResponse {
    count: usize,
    next: Option<String>,
    previous: Option<String>,
    result: Vec<Book>,
}

#[derive(Serialize, Debug, Clone, Default)]
struct BookRequest {
    title: RwSignal<String>,
    genre: RwSignal<String>,
    isbn: RwSignal<String>,
    page: RwSignal<usize>,
}
// INFO: ^^^^^ COPIED ^^^^^

async fn get(book_id: usize) -> anyhow::Result<Option<Book>> {
    const ENDPOINT: &'static str = "/api/book/books/";
    let endpoint = format!("{ENDPOINT}{book_id}/");
    let res: BookResponse = send_get_request(&endpoint).await?;
    Ok(res.result.get(0).cloned())
}

enum BookData {
    Ok(Book),
    Err,
    NotExist,
    Unknown,
}

#[component]
pub fn book_info(book_id: ReadSignal<usize>) -> impl IntoView {
    let book_request = LocalResource::new(move || get(book_id()));
    let book_data = move || match &*book_request.read() {
        None => BookData::Unknown,
        Some(Ok(Some(book))) => BookData::Ok(book.clone()),
        Some(Ok(None)) => BookData::NotExist,
        Some(Err(err)) => {
            log::log!(Level::Error, "{err}");
            BookData::Err
        }
    };

    let book_error_display = move || match book_data() {
        BookData::Err => "Something went wrong, please try again".into_view(),
        BookData::Unknown => "Waiting for server".into_view(),
        BookData::NotExist => "Given book does not exist".into_view(),
        BookData::Ok(_) => "".into_view(),
    };

    let book_data_display = move || {
        if let BookData::Ok(Book {
            genres,
            authors,
            page_count,
            title,
            description,
            isbn,
            published_at,
            language,
        }) = book_data()
        {
            let authors = authors
                .into_iter()
                .map(
                    |Author {
                         first_name,
                         middle_name,
                         last_name,
                         ..
                     }| { format!("{first_name} {middle_name} {last_name}") },
                )
                .intersperse(", ".to_string())
                .collect_view();

            let genres = genres
                .into_iter()
                .map(|Genre { name }| name)
                .intersperse(", ".to_string())
                .collect_view();

            Some(view! {
                {title} " by " {authors} <br/>
                "genres: " {genres} ". ISBN: " {isbn} <br/>
                "Written in " {language} ". Published " {published_at} ". Page count: " {page_count} <br/>
                {description} <br/>
                <Reviews book_id=book_id />
            })
        } else {
            None
        }
    };

    view! {
        {book_data_display}
    }
}
