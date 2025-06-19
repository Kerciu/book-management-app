use std::{collections::BTreeSet, iter};

use leptos::prelude::*;
use leptos_router::hooks::*;
use log::Level;
use serde::Deserialize;
use super::send_get_request;
use serde::Serialize;

#[allow(dead_code, reason = "Faithful representation of endpoint data")]
#[derive(Deserialize, Debug, Clone)]
pub struct Author {
    pub name: String,
    pub birth_date: Option<String>,
    pub death_date: Option<String>,
}

#[derive(Deserialize, Debug, Clone, PartialEq, Eq, PartialOrd, Ord)]
pub struct Genre {
    pub name: String,
}

#[derive(Deserialize, Debug, Clone, Default)]
pub struct Book {
    pub id: usize,
    pub genres: Vec<Genre>,
    pub authors: Vec<Author>,
    pub page_count: Option<usize>,
    pub title: String,
    pub description: String,
    pub isbn: String,
    pub published_at: String,
    pub language: String,
}

#[allow(dead_code, reason = "Faithful representation of endpoint data")]
#[derive(Deserialize, Debug, Clone)]
struct BookResponse {
    count: usize,
    next: Option<String>,
    previous: Option<String>,
    results: Vec<Book>,
}

#[allow(dead_code, reason = "Faithful representation of endpoint data")]
#[derive(Serialize, Debug, Clone, Default)]
struct BookRequest {
    title: RwSignal<String>,
    genre: RwSignal<String>,
    isbn: RwSignal<String>,
    page: RwSignal<usize>,
}

async fn get(request: String) -> anyhow::Result<BookResponse> {
    let res = send_get_request(&request).await?;
    Ok(res)
}
/// tempo

#[derive(Debug, Clone)]
struct Shelf {
    id: usize,
    user: usize,
    name: String,
    is_default: bool,
    shelf_type: String,
}

fn generate_example_shelves() -> Vec<Shelf> {

    (1..=50)
        .map(|i| Shelf {
            id: i,
            user: i % 10 + 1, // Just cycle user ids from 1 to 10
            name: format!("Shelf {}", i),
            is_default: i % 10 == 0, // Every 10th shelf is default
            shelf_type: if i % 2 == 0 { "custom".to_string() } else { "default".to_string() },
        })
        .collect()
}

#[component]
fn get_shelves_list(book_id: usize, set_show_shelves: WriteSignal<bool>) -> impl IntoView {
    let shelves = generate_example_shelves();
    view!{
        {shelves.into_iter()
            .map(|shelve| view!{
                <div class="title-text" on:click=move |ev| {
                    ev.stop_propagation();
                    //put_book_in_shelf(book_id, shelve.id);
                    set_show_shelves.set(false);
                    }>{shelve.name}</div>
            })
            .collect_view()
        }
    }
}

/// 

#[component]
fn book_info(book: Book, is_library: bool) -> impl IntoView {
    let Book {
        genres,
        authors,
        page_count,
        title,
        description,
        isbn,
        published_at,
        language,
        id,
    } = book;
    let navigate = use_navigate();
    let navigate_collection = navigate.clone();
    let authors = authors
        .into_iter()
        .map(|Author { name, .. }| name)
        .intersperse(", ".to_string())
        .collect_view();

    let genres = genres.into_iter().map(|Genre { name }| name).collect_view();
    
    let (show_shelves, set_show_shelves) = signal(false);


    // TODO: Make costanat variable out of this "100"
    let short_description = description.chars().take(100).collect::<String>();
    view! {

            <div class="book-item" style="margin-right: 20px; margin-left: 20px;">
                <img src="https://ecsmedia.pl/cdn-cgi/image/format=webp,/c/the-rust-programming-language-2nd-edition-b-iext138640655.jpg" alt="Description"
                    style="margin-top: 20px; padding-bottom:20px; height: 316px; object-fit: cover; width: auto; object-fit: contain; " on:click=move |_| {
                    navigate(&format!("/books/details/{id}"), Default::default());
                    }>
                </img>
                <div class="book-details">
                    <h4 style = "max-width: 400px;     word-wrap: break-word; overflow-wrap: break-word;"><a href=format!("/books/details/{id}")>{title}</a></h4>
                    <p style = "max-width: 400px;     word-wrap: break-word; overflow-wrap: break-word;">"by "{authors}</p>
                    <p style = "max-width: 400px;     word-wrap: break-word; overflow-wrap: break-word;">{format!("Published: {}", published_at)}</p>
                    <div class="body-text" style="color: #FFFFFF; margin-left:0px; font-size: 20px; margin-top:10px;">
                        {short_description}"..."
                    </div>
                    <div class="categories-container" style="margin-top:20px;">
                                <div class="chips-container">
                                    {genres.into_iter()
                                        .map(|genre| view! {
                                            <span class="chip">{genre}</span>
                                        })
                                        .collect_view()}
                                </div>
                    </div>  
                        {move || { 
                            let navigate_collection = navigate_collection.clone(); 
                            (!is_library).then_some(view! {
                                <div class="book-actions">
                                    <button class="btn-small" on:click=move |_| navigate_collection(&format!("/books/select_collection/{id}"), Default::default())>"Add to the collection"</button>
                                </div>
                            })
                        }}
                        {move || is_library.then_some(view!{<div class="book-actions">
                            <button class="btn-small btn-danger">"Remove from the collection"</button>
                        </div>})}
                </div>
            </div>
    }
}

#[component]
pub fn book_list(is_library_page: bool) -> impl IntoView {
    const ENDPOINT: &'static str = "/api/book/books/";
    let (title, set_title) = signal(String::new());
    let (genre, set_genre) = signal(String::new());
    let (isbn, set_isbn) = signal(String::new());
    let (page, set_page) = signal(String::new());
    let (sort, set_sort) = signal(String::new());

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
            log::log!(Level::Error, "{}", err);
            None
        }
        None => None,
    };

    let books = move || {
        request()
            .into_iter()
            .map(|BookResponse { results, .. }| results)
            .flatten()
            .filter(move |Book { genres, .. }| {
                genres
                    .iter()
                    .any(move |Genre { name }| name.contains(&genre()) || genre() == "")
            })
            .filter(move |book| {
                book.title.to_ascii_lowercase().contains(&title().to_ascii_lowercase()) || title() == ""
            })
            .collect::<Vec<_>>()
    };

    let books = move || {
        let mut books = books();
        books.sort_by_key(move |book| match &sort() as &str {
            "title" => book.title.clone(),
            "author" => book.authors[0].name.clone(),
            "date" =>  book.published_at.clone(),
            _ => unreachable!()
        });
        books
    };

    let all_genres = move || {
        request()
            .into_iter()
            .map(|BookResponse { results, .. }| results)
            .flatten()
            .map(|Book {genres, ..}| genres)
            .flatten()
            .collect::<BTreeSet<_>>()
    };

    let all_genres = move || {
        all_genres()
            .into_iter()
            .map(|Genre { name }| view! {<option value=name.clone()>{name.clone()}</option>}.into_any())
            .chain(iter::once(view! {<option value="">Select genre</option>}.into_any()))
            .rev()
            .collect_view()
        };

    view! {
        <div class="controls">
            <input type="text" id="book-search" placeholder="Search books..." class="search-input" style="align-items: center; margin-top: 0px;" bind:value=(title, set_title)/>
            <select id="genre-filter" class="filter-select" style="align-items: center;" bind:value=(genre, set_genre)>
                {move || all_genres()}
            </select>
            <select id="sort-books" class="sort-select" style="align-items: center;" bind:value=(sort, set_sort)>
                <option value="title">Sort by Title</option>
                <option value="author">Sort by Author</option>
                <option value="date">Sort by Date Added</option>
            </select>
        </div>
        <div class="books-grid" id="books-grid">
            <For
                each=move || books()
                key=|book| book.id
                children=move |book| {
                    view! {
                        <BookInfo book=book is_library=false/>
                    }
                }
            />
        </div>
    }
}
