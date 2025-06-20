use super::book_list::{Author, Book, Genre};
use crate::components::{ReviewInput, ReviewList, send_get_request};
use leptos::prelude::*;
use log::Level;

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

    let rerun= RwSignal::new(false);

    view! {
        <div class="container-flex-row" style="padding: 0px;">
            <div>
                <div class="container-flex-row" style="padding: 0px;">
                    //image url
                    <img src={move || book().cover_image} alt="Description"  style="margin-top: 20px; margin-left:20px; padding-bottom:20px; height:500px;"></img>
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
                <ReviewInput book_id=id refetch=rerun />

            </div>
            <div class="divider"></div>
            <div style="flex-grow: 1; margin-right:20px;">
               <div class="text-title" style="color: #FFFFFF; margin-left:0px; margin-top:30px;">"Reviews"</div>
               <ReviewList book_id=Signal::derive(move || id()) refetch=rerun/>
            </div>
        </div>

    }
}
