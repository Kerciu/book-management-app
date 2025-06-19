use leptos::prelude::*;
use leptos_router::hooks::*;
use log::Level;
use serde::Deserialize;
use super::send_get_request;
use serde::Serialize;
use crate::components::{get_shelves, put_book_in_shelf};

#[allow(dead_code, reason="Faithful representation of endpoint data")]
#[derive(Deserialize, Debug, Clone)]
pub struct Author {
    pub first_name: String,
    pub middle_name: String,
    pub last_name: String,
    pub bio: String,
    pub birth_date: String,
    pub death_date: String,
}

#[derive(Deserialize, Debug, Clone)]
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

#[allow(dead_code, reason="Faithful representation of endpoint data")]
#[derive(Deserialize, Debug, Clone)]
struct BookResponse {
    count: usize,
    next: Option<String>,
    previous: Option<String>,
    results: Vec<Book>,
}

#[allow(dead_code, reason="Faithful representation of endpoint data")]
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
                    put_book_in_shelf(book_id, shelve.id);
                    set_show_shelves.set(false);
                    }>{shelve.name}</div>
            })
            .collect_view()
        }
    }
}

/// 

#[component]
fn book_info(book: Book, is_library:bool) -> impl IntoView {
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

    let genres = genres.into_iter().map(|Genre { name }| name).collect_view();
    
    let (show_shelves, set_show_shelves) = signal(false);


    // TODO: Make costanat variable out of this "100"
    let short_description = description.chars().take(100).collect::<String>();
    view! {

            <div class="book-item" style="margin-right: 20px; margin-left: 20px;" on:click=move |_| {
                    navigate(&format!("/books/details/{id}"), Default::default());
                    }>
                <img src="https://ecsmedia.pl/cdn-cgi/image/format=webp,/c/the-rust-programming-language-2nd-edition-b-iext138640655.jpg" alt="Description"
                    style="margin-top: 20px; padding-bottom:20px; height: 316px; object-fit: cover; width: auto; object-fit: contain; ">
                </img>
                <div class="book-details">
                    <h4 style = "max-width: 400px;     word-wrap: break-word; overflow-wrap: break-word;">{title}</h4>
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
                    <Show when=move || is_library fallback=move || 
                        view! {
                            <div class="book-actions">
                                <button class="btn-small" on:click=move |ev| {
                                    ev.stop_propagation();
                                    set_show_shelves(!show_shelves.get());
                                }>"Add to the collection"</button>
                            </div>
                            <div class="shelf-list-container" class:hidden=move || !show_shelves.get()
                                style=move || {
                                if show_shelves.get() {
                                    "position: absolute; z-index: 1000; background: #250633; max-height: 200px; overflow-y: auto; transition: max-height 0.3s ease; margin-top: 10px; border: 1px solid #ccc; border-radius: 8px; padding: 10px; width: 250px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);".to_string()
                                } else {
                                    "display: none;".to_string()
                                }
                            }>
                                    <GetShelvesList book_id=id set_show_shelves=set_show_shelves/>
                            </div>
                        }
                    >
                        <div class="book-actions">
                            <button class="btn-small btn-danger">"Remove from the collection"</button>
                        </div>
                    </Show>
                </div>
            </div>
    }
}

// temporary functions for testing

pub fn get_example_book() -> Book {
    Book {
        id: 1,
        genres: get_example_genres(),
        authors: get_example_authors(),
        page_count: Some(523),
        title: "The Rust Programming Language".to_string(),
        description: "The official book on Rust, written by the Rust development team at Mozilla. This book will teach you about Rust's unique features and how to use them effectively.".to_string(),
        isbn: "978-1593278281".to_string(),
        published_at: "2018-05-15".to_string(),
        language: "English".to_string(),
    }
}

fn get_example_genres() -> Vec<Genre> {
    vec![
        Genre {
            name: "Programming".to_string(),
        },
        Genre {
            name: "Technology".to_string(),
        },
        Genre {
            name: "Computer Science".to_string(),
        },
    ]
}

fn get_example_authors() -> Vec<Author> {
    vec![
        Author {
            first_name: "Steve".to_string(),
            middle_name: "".to_string(),
            last_name: "Klabnik".to_string(),
            bio: "Steve Klabnik is a member of the Rust core team and has been involved in Rust documentation.".to_string(),
            birth_date: "1985-02-02".to_string(),
            death_date: "".to_string(),
        },
        Author {
            first_name: "Carol".to_string(),
            middle_name: "".to_string(),
            last_name: "Nichols".to_string(),
            bio: "Carol Nichols is a Rust developer and educator.".to_string(),
            birth_date: "1984-05-08".to_string(),
            death_date: "".to_string(),
        },
    ]
}

//

#[component]
pub fn book_list(is_library_page:bool) -> impl IntoView {
    const ENDPOINT: &'static str = "/api/book/books/";
    let (title, set_title) = signal(String::new());
    let (genre, set_genre) = signal(String::new());
    let (isbn, set_isbn) = signal(String::new());
    let (page, set_page) = signal(String::new());

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
            .collect::<Vec<_>>()
    };

    view! {
        <div class="controls">
            <input type="text" id="book-search" placeholder="Search books..." class="search-input" style="align-items: center; margin-top: 0px;"/>
            <select id="genre-filter" class="filter-select" style="align-items: center;">
                <option value="">All Genres</option>
                <option value="fiction">Fiction</option>
                <option value="non-fiction">Non-Fiction</option>
                <option value="sci-fi">Sci-Fi</option>
                <option value="mystery">Mystery</option>
            </select>
            <select id="sort-books" class="sort-select" style="align-items: center;">
                <option value="title">Sort by Title</option>
                <option value="author">Sort by Author</option>
                <option value="rating">Sort by Rating</option>
                <option value="date">Sort by Date Added</option>
            </select>
        </div>
        <div class="books-grid" id="books-grid">

            //temp solution for testing
            <BookInfo book=get_example_book() is_library=is_library_page/>
            <BookInfo book=get_example_book() is_library=is_library_page/>
            <BookInfo book=get_example_book() is_library=is_library_page/>
            <BookInfo book=get_example_book() is_library=is_library_page/>
            <BookInfo book=get_example_book() is_library=is_library_page/>

            //

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
