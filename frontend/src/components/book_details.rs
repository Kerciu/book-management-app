use super::book_list::{Author, Book, Genre};
use crate::components::{ReviewInput, ReviewList, send_get_request};
use leptos::prelude::*;
use log::Level;
use serde::{Deserialize, Serialize};

// //temporary solution for testing
// pub fn get_example_book() -> Book {
//     Book {
//         id: 1,
//         genres: get_example_genres(),
//         authors: get_example_authors(),
//         page_count: Some(523),
//         title: "The Rust Programming Language".to_string(),
//         description: "The official book on Rust, written by the Rust development team at Mozilla. This book will teach you about Rust's unique features and how to use them effectively.".to_string(),
//         isbn: "978-1593278281".to_string(),
//         published_at: "2018-05-15".to_string(),
//         language: "English".to_string(),
//     }
// }

// fn get_example_genres() -> Vec<Genre> {
//     vec![
//         Genre {
//             name: "Programming".to_string(),
//         },
//         Genre {
//             name: "Technology".to_string(),
//         },
//         Genre {
//             name: "Computer Science".to_string(),
//         },
//     ]
// }

// fn get_example_authors() -> Vec<Author> {
//     vec![
//         Author {
//             first_name: "Steve".to_string(),
//             middle_name: "".to_string(),
//             last_name: "Klabnik".to_string(),
//             bio: "Steve Klabnik is a member of the Rust core team and has been involved in Rust documentation.".to_string(),
//             birth_date: "1985-02-02".to_string(),
//             death_date: "".to_string(),
//         },
//         Author {
//             first_name: "Carol".to_string(),
//             middle_name: "".to_string(),
//             last_name: "Nichols".to_string(),
//             bio: "Carol Nichols is a Rust developer and educator.".to_string(),
//             birth_date: "1984-05-08".to_string(),
//             death_date: "".to_string(),
//         },
//     ]
// }

async fn get(book_id: usize) -> anyhow::Result<Book> {
    const ENDPOINT: &'static str = "/api/book/books/";
    let endpoint = format!("{ENDPOINT}{book_id}/");
    let res: Book = send_get_request(&endpoint).await?;
    Ok(res)
}

#[component]
pub fn book_details(id: impl Fn() -> usize + Send + Sync + Copy + 'static) -> impl IntoView {
    let book_request = LocalResource::new(move || get(id()));
    let book_data = move || {
        let req = book_request.read();
        match &*req {
            None => None,
            Some(Ok(book)) => Some(book.clone()),
            Some(Err(err)) => {
                log::log!(Level::Error, "{err}");
                None
            }
        }
    };

    let book = move || book_data().unwrap_or_default();

    let genres = move || {
        book()
            .genres
            .into_iter()
            .map(|Genre { name }| name)
            .collect_view()
    };
    let authors = move || {
        book()
            .authors
            .into_iter()
            .map(|Author { name, .. }| name)
            .intersperse(", ".to_string())
            .collect_view()
    };

    view! {
        <div class="container-flex-row" style="padding: 0px;">
            <div>
                <div class="container-flex-row" style="padding: 0px;">
                    //image url
                    <img src="https://ecsmedia.pl/cdn-cgi/image/format=webp,width=544,height=544,/c/the-rust-programming-language-2nd-edition-b-iext138640655.jpg" alt="Description"  style="margin-top: 20px; margin-left:20px; padding-bottom:20px; height:500px;"></img>
                    <div class="text-side" style="margin-top: 20px;">
                        <div class="text-title" style="color: #FFFFFF; margin-left:0px; margin-top:10px;">{move || book().title}</div>
                        <div class="body-text" style="color: #cac1ce; margin-left:0px; margin-top:10px;">{move || authors()}</div>
                        <div class="body-text" style="color: #cac1ce; margin-left:0px; margin-top:10px;">"Published: "{move || book().published_at}</div>
                        <div class="categories-container" style="margin-top:10px;">
                            <div class="chips-container">
                                {move || genres().into_iter()
                                    .map(|genre| view! {
                                        <span class="chip">{genre}</span>
                                    })
                                .collect_view()}
                            </div>
                        </div>

                    </div>
                </div>
                <div class="test-book-description" style = "max-width: 800px; word-wrap: break-word; overflow-wrap: break-word; margin-left:20px;">
                    {move || book().description}
                </div>
                <ReviewInput book_id=id/>

            </div>
            <div class="divider"></div>
            <div style="flex-grow: 1; margin-right:20px;">
               <div class="text-title" style="color: #FFFFFF; margin-left:0px; margin-top:30px;">"Reviews"</div>
               <ReviewList book_id=Signal::derive(move || id())/>
            </div>
        </div>

    }
}
