use std::collections::HashMap;

use leptos::prelude::*;
use log::{Level, log};
use serde::Deserialize;

use super::send_get_request;

#[derive(Deserialize, Debug, Clone)]
struct BookResponse {
    id: usize,
    title: String,
    published_at: String,
    #[serde(alias = "author_id")]
    author: usize,
    categories: Vec<usize>,
}

#[derive(Deserialize, Debug, Clone)]
struct AuthorResponse {
    id: usize,
    name: String,
}

#[derive(Deserialize, Debug, Clone)]
struct CategoryResponse {
    id: usize,
    name: String,
}

struct Book {
    id: usize,
    title: String,
    published_at: String,
    author: String,
    categories: Vec<String>,
}

async fn get_books() -> anyhow::Result<Vec<BookResponse>> {
    let endpoint = "/api/books/";
    send_get_request(endpoint).await
}

async fn get_authors() -> anyhow::Result<HashMap<usize, String>> {
    let endpoint = "/api/authors/";
    let res: Vec<AuthorResponse> = send_get_request(endpoint).await?;
    Ok(res
        .into_iter()
        .map(|AuthorResponse { id, name }| (id, name))
        .collect())
}

async fn get_categories() -> anyhow::Result<HashMap<usize, String>> {
    let endpoint = "/api/categories/";
    let res: Vec<CategoryResponse> = send_get_request(endpoint).await?;
    Ok(res
        .into_iter()
        .map(|CategoryResponse { id, name }| (id, name))
        .collect())
}

#[component]
fn book_info(book: Book) -> impl IntoView {
    let Book {
        title,
        published_at,
        author,
        categories, 
        .. 
    } = book;
    view! {
            <div class="book-display">
                    <div class="container-flex" style="padding: 0px;">
                        //image url
                        <img src="https://ecsmedia.pl/cdn-cgi/image/format=webp,width=544,height=544,/c/the-rust-programming-language-2nd-edition-b-iext138640655.jpg" alt="Description" class="image-side" style="margin-top: 20px; padding-bottom:20px;"></img>
                        <div class="text-side" style="margin-top: 20px;">
                            <div class="text-title" style="color: #FFFFFF; margin-left:0px;">{title}</div>
                            <div class="body-text" style="color: #cac1ce; margin-left:0px;">{format!("by {}", author)}</div>
                            <div class="body-text" style="color: #cac1ce; margin-left:0px;">{format!("Published: {}", published_at)}</div>
                            <div class="body-text" style="color: #FFFFFF; margin-left:0px; font-size: 20px; margin-top:10px;">
                                //description
                                "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."
                            </div>
                            <div class="categories-container" style="margin-top:10px;">
                                <div class="chips-container">
                                    {categories.into_iter()
                                        .map(|category| view! { 
                                            <span class="chip">{category}</span> 
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
pub fn book_list() -> impl IntoView {
    let book_templates = LocalResource::new(get_books);
    let authors = LocalResource::new(get_authors);
    let categories = LocalResource::new(get_categories);

    let authors = move || {
        let maybe_authors = &*authors.read();
        match maybe_authors {
            Some(response) => match response {
                Ok(authors) => authors.clone(),
                Err(err) => {
                    log!(Level::Error, "{}", err);
                    return Default::default();
                }
            },
            None => return Default::default(),
        }
    };

    let categories = move || {
        let maybe_categories = &*categories.read();
        match maybe_categories {
            Some(response) => match response {
                Ok(categories) => categories.clone(),
                Err(err) => {
                    log!(Level::Error, "{}", err);
                    return Default::default();
                }
            },
            None => return Default::default(),
        }
    };

    let books = move || {
        let maybe_templates = &*book_templates.read();
        let templates = match maybe_templates {
            Some(response) => match response {
                Ok(templates) => templates,
                Err(err) => {
                    log!(Level::Error, "{}", err);
                    return Default::default();
                }
            },
            None => return Default::default(),
        };

        templates
            .into_iter()
            .map(|template| Book {
                id: template.id,
                title: template.title.clone(),
                author: authors()
                    .get(&template.author)
                    .map(Clone::clone)
                    .unwrap_or_default(),
                published_at: template.published_at.clone(),
                categories: template
                    .categories
                    .iter()
                    .map(|id| categories().get(id).map(Clone::clone).unwrap_or_default())
                    .collect(),
            })
            .collect::<Vec<_>>()
    };

    view! {
        <div class="container-flex-row" style="padding:0px;">
            <input type="text" placeholder="Search" style="margin-left:0px; border-radius: 16px; height:19px; margin-top:0px;"/>
            <button class="button-pop" style="width: auto;">"Filter"</button>
            <button class="button-pop" style="width: auto;">"Sort"</button>
        </div>
        <For
            each=move || books()
            key=|book| book.id
            children=move |book| {
                view! {
                    <BookInfo book=book />
                }
            }
        />
    }
}
