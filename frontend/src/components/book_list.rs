use super::send_get_request;
use crate::components::{get_shelves, put_book_in_shelf};
use crate::components::{handle_request, shelves_list::remove_book_from_shelf};
use leptos::prelude::*;
use leptos_router::hooks::*;
use log::Level;
use serde::Deserialize;
use serde::Serialize;
use std::{iter, time::Duration};

#[allow(dead_code, reason = "Faithful representation of endpoint data")]
#[derive(Deserialize, Debug, Clone)]
pub struct Author {
    pub name: String,
    pub birth_date: Option<String>,
    pub death_date: Option<String>,
}

#[allow(dead_code, reason = "Faithful representation of endpoint data")]
#[derive(Deserialize, Debug, Clone, Default)]
pub struct Book {
    pub id: usize,
    pub cover_image: Option<String>,
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
//

#[component]
fn get_shelves_list(book_id: usize, set_show_shelves: WriteSignal<bool>) -> impl IntoView {
    let shelves = LocalResource::new(move || get_shelves());
    let shelves = move || match &*shelves.read() {
        Some(Ok(res)) => res.clone(),
        _ => Default::default(),
    };
    let action = handle_request(&put_book_in_shelf);

    view! {
        <For
            each=move || shelves()
            key=|shelf| shelf.id
            children=move |shelf| {
                view! {
                    <div class="title-text" style="font-size:20px;" on:click=move |ev| {
                    ev.stop_propagation();
                    action.dispatch((book_id, shelf.id));

                    set_show_shelves.set(false);
                    }>{shelf.name}</div>
                    <div class="divider-horizontal" style="margin-bottom:5px; margin-top:5px;"></div>

                 }
            }
        />
    }
}

#[derive(Deserialize, Clone, Debug, Default)]
pub struct Genre {
    pub id: usize,
    pub name: String,
}

impl PartialEq for Genre {
    fn eq(&self, other: &Self) -> bool {
        self.id == other.id
    }
}

impl PartialOrd for Genre {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        self.name.partial_cmp(&other.name)
    }
}

impl Eq for Genre {}

impl Ord for Genre {
    fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        self.name.cmp(&other.name)
    }
}

#[allow(dead_code, reason = "Faithful representation of endpoint data")]
#[derive(Deserialize, Clone, Debug, Default)]
struct GenreResponse {
    count: usize,
    next: Option<String>,
    previous: Option<String>,
    results: Vec<Genre>,
}

async fn get_categories() -> anyhow::Result<Vec<Genre>> {
    const ENDPOINT: &str = "/api/book/genres/";
    let mut res: GenreResponse = send_get_request(&ENDPOINT).await?;
    let mut ret = vec![res];

    while let Some(ref endpoint) = ret.last().unwrap().next {
        res = send_get_request(endpoint).await?;
        ret.push(res);
    }

    Ok(ret
        .into_iter()
        .map(|GenreResponse { results, .. }| results)
        .flatten()
        .collect())
}

#[component]
pub fn book_info(
    book: Book,
    is_library: bool,
    #[prop(optional)] refetch: Signal<()>,
    #[prop(optional)] shelf_id: usize,
) -> impl IntoView {
    let Book {
        cover_image,
        genres,
        authors,
        title,
        description,
        published_at,
        id,
        page_count,
        ..
    } = book;
    let navigate = use_navigate();
    let navigate_collection = navigate.clone();
    let authors = authors
        .into_iter()
        .map(|Author { name, .. }| name)
        .intersperse(", ".to_string())
        .collect_view();

    let genres = genres
        .into_iter()
        .map(|Genre { name, .. }| name)
        .collect_view();
    let delete_book_from_collection = handle_request(&remove_book_from_shelf);
    let (show_shelves, set_show_shelves) = signal(false);
    // TODO: Make costanat variable out of this "100"
    let short_description = description.chars().take(100).collect::<String>();
    view! {

            <div class="book-item" style="margin-right: 20px; margin-left: 20px;">
                <img src={cover_image} alt="Description" on:click=move |_| {navigate(&format!("/books/details/{id}"), Default::default());}
                    style="margin-top: 20px; padding-bottom:20px; height: 316px; object-fit: cover; width: auto; object-fit: contain; " >
                </img>
                <div class="book-details">
                    <h4 style = "max-width: 400px;     word-wrap: break-word; overflow-wrap: break-word;"><a
                    href=format!("/books/details/{id}")
                    style="color: inherit; text-decoration: none;"
                    >{title}</a></h4>
                    <p style = "max-width: 400px;     word-wrap: break-word; overflow-wrap: break-word;">"by "{authors}</p>
                    <p style = "max-width: 400px;     word-wrap: break-word; overflow-wrap: break-word;">{format!("Published: {}", published_at)}</p>
                    <p style = "max-width: 400px;     word-wrap: break-word; overflow-wrap: break-word;">{format!("Page count: {}", page_count.map(|v: usize| ToString::to_string(&v)).unwrap_or("unknown".to_string()))}</p>
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
                            let _navigate_collection = navigate_collection.clone();
                            (!is_library).then_some(view! {
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
                                })
                        }}
                        {move || is_library.then_some(view!{<div class="book-actions">
                            <button class="btn-small btn-danger" on:click=move |_| { delete_book_from_collection.dispatch((id, shelf_id)); set_timeout(move || refetch(), Duration::from_millis(500));}>"Remove from the collection"</button>
                        </div>})}
                </div>
            </div>
    }
}

#[allow(unused, reason = "can't prefix due to macro expansion")]
#[component]
pub fn book_list(is_library_page: bool) -> impl IntoView {
    const ENDPOINT: &'static str = "/api/book/books/";
    let (title, set_title) = signal(String::new());
    let (genre, set_genre) = signal(String::new());
    let (page, set_page) = signal(1 as usize);
    let (sort, set_sort) = signal(String::new());

    let request_url = move || {
        format!(
            "{ENDPOINT}?title={}&genres__name={}&page={}&ordering={}",
            title.read(),
            genre.read(),
            page.read(),
            sort.read()
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
            // .filter(move |Book { genres, .. }| {
            //     genres
            //         .iter()
            //         .any(move |Genre { name, .. }| name.contains(&genre()) || genre() == "")
            // })
            // .filter(move |book| {
            //     book.title
            //         .to_ascii_lowercase()
            //         .contains(&title().to_ascii_lowercase())
            //         || title() == ""
            // })
            .collect::<Vec<_>>()
    };

    let genre_request = LocalResource::new(move || get_categories());

    let all_genres = move || {
        let mut ret = match &*genre_request.read() {
            Some(Ok(vec)) => vec.clone(),
            _ => Default::default(),
        };
        ret.sort();
        ret
    };

    let all_genres = move || {
        all_genres()
            .into_iter()
            .map(|Genre { name, .. }| {
                view! {<option value=name.clone() on:click=move |_| set_page(1)>{name.clone()}</option>}.into_any()
            })
            .chain(iter::once(
                view! {<option value="" on:click=move |_| set_page(1)>Select genre</option>}.into_any(),
            ))
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
                <option value="title" on:click=move |_| set_page(1)>Sort by Title</option>
                <option value="page_count" on:click=move |_| set_page(1)>Sort by Page Count</option>
                <option value="published_at" on:click=move |_| set_page(1)>Sort by Date Added</option>
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
        <div>
            <button class="btn-small" on:click=move |_| set_page.update(|v| *v = (*v-1).max(1))>"←"</button>
            "   "{move || page()}"   "
            <button class="btn-small" on:click=move |_| set_page.update(|v| *v = (*v+1).max(1))>"→"</button>
        </div>
    }
}
