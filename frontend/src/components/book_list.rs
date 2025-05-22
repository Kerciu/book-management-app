use leptos::prelude::*;
use log::Level;
use serde::Deserialize;

use super::send_get_request;
use serde::Serialize;

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

async fn get(request: String) -> anyhow::Result<BookResponse> {
    let res: BookResponse = send_get_request(&request).await?;
    Ok(res)
}

#[component]
fn book_info(book: Book) -> impl IntoView {
    let Book {
        genres,
        authors,
        page_count,
        title,
        description,
        isbn,
        published_at,
        language,
    } = book;

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

    // TODO: Make costanat variable out of this "100"
    let short_description = description[..100].to_string();

    view! {
        "-----" <br/>
        {title} " by " {authors} <br/>
        "genres: " {genres} ". ISBN: " {isbn} <br/>
        "Written in " {language} ". Published " {published_at} ". Page count: " {page_count} <br/>
        {short_description} "..." <br/>
        "-----" <br/>
    }
}

#[component]
pub fn book_list(
    title: ReadSignal<String>,
    genre: ReadSignal<String>,
    isbn: ReadSignal<String>,
    page: ReadSignal<usize>,
) -> impl IntoView {
    const ENDPOINT: &'static str = "/api/book/books/";
    let request_url = move || {
        format!(
            "{ENDPOINT}?title={}&genre={}&isbn={}&page={}",
            title.read(),
            genre.read(),
            isbn.read(),
            page.read()
        )
    };
    let request = LocalResource::new(move || get(request_url()));

    let request = move || match &*request.read() {
        Some(Ok(res)) => Some(res.clone()),
        Some(Err(err)) => {
            log::log!(Level::Error, "{err}");
            None
        }
        None => None,
    };

    let book_list = move || {
        request()
            .into_iter()
            .map(|BookResponse { result, .. }| result)
            .flatten()
            .collect::<Vec<_>>()
    };

    let book_view_list = move || {
        book_list()
            .into_iter()
            .map(|book| view! {<BookInfo book=book />})
            .collect_view()
    };

    view! {
        {book_view_list}
    }
}
