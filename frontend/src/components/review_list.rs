use leptos::prelude::*;
use log::Level;
use serde::Deserialize;

use crate::components::{review::Review, send_get_request};

#[allow(dead_code, reason = "Faithful representation of endpoint data")]
#[derive(Deserialize, Clone, Debug)]
struct ReviewResponse {
    count: usize,
    next: Option<String>,
    previous: Option<String>,
    results: Vec<Review>,
}

async fn get(book_id: usize) -> anyhow::Result<ReviewResponse> {
    let endpoint = format!("/api/review/reviews/{book_id}/reviews/");
    send_get_request(&endpoint).await
}

#[component]
pub fn review_list(book_id: Signal<usize>, refetch: RwSignal<bool>) -> impl IntoView {
    let response_handle = LocalResource::new(move || get(book_id()));
    let response = move || match &*response_handle.read() {
        Some(Ok(res)) => Some(res.clone()),
        Some(Err(err)) => {
            log::log!(Level::Error, "{err}");
            None
        }
        None => None,
    };
    let reviews = move || {
        response()
            .map(|ReviewResponse { results, .. }| results)
            .unwrap_or_default()
    };
    Effect::new(move || {
        if refetch() {
            refetch(false);
            response_handle.refetch();
        }
    });

    view! {
        <For
          each=move || reviews().into_iter()
        key=|review| review.id()
        children=move |review| view! {
                                        <Review
                                            book_id=Signal::derive(move || book_id())
                                            data=Signal::derive(move || review.clone())
                                            refetch_handle=Signal::derive(move || refetch(true))
                                        />
                                    }
       />


    }
}
