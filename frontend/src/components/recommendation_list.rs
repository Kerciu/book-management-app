use leptos::prelude::*;
use serde::Deserialize;
use std::sync::Arc;

//Copied !!!
#[allow(dead_code, reason = "Faithful representation of endpoint data")]
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

#[allow(dead_code, reason = "Faithful representation of endpoint data")]
#[derive(Deserialize, Debug, Clone)]
pub struct Book {
    id: usize,
    genres: Vec<Genre>,
    authors: Vec<Author>,
    page_count: Option<usize>,
    title: String,
    description: String,
    isbn: String,
    published_at: String,
    language: String,
}

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

// INFO: ^^^^^ COPIED ^^^^^

#[component]
fn BookDetails(
    title: String,
    authors: String,
    published: String,
    genres: Vec<String>,
    description: String,
) -> impl IntoView {
    let is_des = description != "";

    view! {
        <>
            <h3>{title}</h3>
            <p class="author">{format!("by {}", authors)}</p>
            <Show
                when=move || is_des
                fallback=move ||
                    view! {
                        <div></div>
                    }
            >
                <p class="author">{format!("Published: {}", published)}</p>
                <div class="body-text" style="color: #FFFFFF; margin-left:0px; font-size: 20px; margin-top:10px;">
                            {description.clone()}
                </div>
            </Show>
            <div class="categories-container" style="margin-top:20px;">
                <div class="chips-container">
                    {genres.iter().map(|genre| {
                        view! {
                            <span class="chip">{genre.clone()}</span>
                        }
                    }).collect_view()}
                </div>
            </div>
            <button class="btn-primary" style="margin-top:10px; margin-bottom:20px;">"Add to Library"</button>
        </>
    }
}

#[component]
fn book_info(book: Book, is_first: bool) -> impl IntoView {
    let card_class = move || {
        if is_first {
            "book-card featured"
        } else {
            "book-card"
        }
    };

    let title = Arc::new(book.title.clone());
    let published = Arc::new(book.published_at.clone());

    let authors = Arc::new(
        book.authors
            .clone()
            .into_iter()
            .map(
                |Author {
                     first_name,
                     middle_name,
                     last_name,
                     ..
                 }| { format!("{first_name} {middle_name} {last_name}") },
            )
            .collect::<Vec<_>>()
            .join(", ")
            .clone(),
    );

    let genres = Arc::new(
        book.genres
            .clone()
            .into_iter()
            .map(|Genre { name }| name)
            .collect::<Vec<_>>(),
    );
    let short_description = book.description;
    let title_2 = title.clone();
    let authors_2 = authors.clone();
    let published_2 = published.clone();
    let genres_2 = genres.clone();

    view! {
        <div class=card_class>
            <Show
                when=move || !is_first
                fallback=move ||
                    view! {
                        <div class="book-item-rec">
                            <img src="https://ecsmedia.pl/cdn-cgi/image/format=webp,/c/the-rust-programming-language-2nd-edition-b-iext138640655.jpg" alt="Description"
                                style="margin-top: 20px; padding-bottom:20px; height: 316px; object-fit: cover; width: auto; object-fit: contain; ">
                            </img>
                            <div class="book-details">
                                <BookDetails title=title.to_string() authors=authors.to_string() published=published.to_string() genres=genres.to_vec() description=short_description.to_string()/>
                            </div>
                        </div>
                    }

            >
                <img
                    src="https://ecsmedia.pl/cdn-cgi/image/format=webp,/c/the-rust-programming-language-2nd-edition-b-iext138640655.jpg"
                    alt="Book cover"
                    style="margin-top: 20px; padding-bottom:20px; height: 316px; object-fit: contain; width: auto;">
                </img>
                <div class="book-info">
                    <BookDetails title=title_2.to_string() authors=authors_2.to_string() published=published_2.to_string() genres=genres_2.to_vec() description="".to_string()/>
                </div>
            </Show>
        </div>
    }
}

//Temp solution for testing
fn get_example_recommended_book_list() -> Vec<Book> {
    vec![
        get_example_book(),
        get_example_book(),
        get_example_book(),
        get_example_book(),
    ]
}

#[component]
pub fn book_reccomendation_list() -> impl IntoView {
    //Should be size 4
    let recommended_books_list = get_example_recommended_book_list();
    view! {
        <div class="recommendations-grid">
            {let mut iter = recommended_books_list.clone().into_iter();
             let first = iter.next();
             let rest = iter;

             view! {
                 {first.map(|book| view! {
                     <BookInfo book=book is_first=true />
                 })}
                 <For
                     each=move || rest.clone()
                     key=|book| book.id
                     children=move |book| {
                         view! {
                             <BookInfo book=book is_first=false />
                         }
                     }
                 />
             }
            }
        </div>
    }
}
