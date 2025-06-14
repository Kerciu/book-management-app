use leptos::prelude::*;
use serde::Serialize;

use crate::components::{handle_request, send_post_request};

#[derive(Serialize, Default, Debug, Clone)]
struct ReviewPostRequest {
    rating: Option<usize>,
    text: String,
    has_spoilers: bool,
    is_public: bool
}

async fn post((book_id, data): (usize, ReviewPostRequest)) -> anyhow::Result<()> {
    let endpoint = format!("/api/review/reviews/{book_id}/reviews/");
    let res = send_post_request(data, &endpoint).await?;
    if res.ok() {
        return Ok(());
    } else {
        return Err(anyhow::anyhow!(res.status_text()));
    }
}

#[component]
pub fn review_input(book_id: impl Fn() -> usize + 'static) -> impl IntoView {
    let text = RwSignal::new(String::new());
    let rating = RwSignal::new(0);
    let has_spoilers = RwSignal::new(false);
    let is_public = RwSignal::new(false);

    let request =  move || ReviewPostRequest {
        text: text(),
        rating: Some(rating()).filter(|val| (1..=5).contains(val)),
        has_spoilers: has_spoilers(),
        is_public: is_public()
    };

    let send_request = handle_request(&post);

    view! {
        <button on:click=move |_| rating(1)>"1"</button>
        <button on:click=move |_| rating(2)>"2"</button>
        <button on:click=move |_| rating(3)>"3"</button>
        <button on:click=move |_| rating(4)>"4"</button>
        <button on:click=move |_| rating(5)>"5"</button>
        <input type="checkbox" bind:value=has_spoilers id="spoilers"/>
        <label for="spoilers">"Has spoilers?"</label>
        <input type="checkbox" bind:value=is_public id="public"/>
        <label for="public">"Is public?"</label>
        <textarea bind:value=text />
        <button on:click=move |_| { send_request.dispatch((book_id(), request())); }>"Submit"</button>
    }
}