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
        <p>
            {title}
            " by "
            {author}
            " published at "
            {published_at}
            " genres: "
            {
                categories.into_iter().map(|category| {
                    view! {
                        <br/>
                        {category}
                    }
                }).collect_view()
            }
        </p>
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
        <p>"Book List:"</p>
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
