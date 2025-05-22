use std::collections::HashMap;
use leptos_router::hooks::*;
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

    let navigate = use_navigate();
    view! {
            <div class="book-display" on:click=move |_| {
                    navigate("/books/details", Default::default());
                    }>
                    <div class="container-flex" style="padding: 0px;">
                        //image url
                        <img src="https://ecsmedia.pl/cdn-cgi/image/format=webp,width=544,height=544,/c/the-rust-programming-language-2nd-edition-b-iext138640655.jpg" alt="Description" class="image-side" style="margin-top: 20px; padding-bottom:20px;"></img>
                        <div class="text-side" style="margin-top: 20px;">
                            <div class="text-title" style="color: #FFFFFF; margin-left:0px;">{title}</div>
                            <div class="body-text" style="color: #cac1ce; margin-left:0px;">"by "{authors}</div>
                            <div class="body-text" style="color: #cac1ce; margin-left:0px;">{format!("Published: {}", published_at)}</div>
                            <div class="body-text" style="color: #FFFFFF; margin-left:0px; font-size: 20px; margin-top:10px;">
                                //description
                                "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."
                            </div>
                            <div class="categories-container" style="margin-top:10px;">
                                <div class="chips-container">
                                    {genres.into_iter()
                                        .map(|genre| view! { 
                                            <span class="chip">{genre}</span> 
                                        })
                                        .collect_view()}
                                </div>
                            </div>
                        </div>
                    </div>
            </div>
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
        //<div class="container-flex-row" style="padding:0px;">
        //    <input type="text" placeholder="Search" style="margin-left:0px; border-radius: 16px; height:19px; margin-top:0px;"/>
        //    <button class="button-pop" style="width: auto;">"Filter"</button>
        //    <select name="Sort" class="custom-select">
        //        <option value="relevance">"Relevance"</option>  
        //        <option value="alphabetically">"Alphabetically"</option>  
        //        <option value="date">"Date published"</option>  =
       //     </select>
       // </div>
       // <For
        //    each=move || books()
        //    key=|book| book.id
         //   children=move |book| {
          //      view! {
          //          <BookInfo book=book />
           //     }
           // }
        ///>
    }
}
