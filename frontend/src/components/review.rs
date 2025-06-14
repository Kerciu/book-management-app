use leptos::prelude::*;
use log::Level;
use serde::Deserialize;

use crate::components::{send_delete_request, send_get_request, send_post_request};

#[allow(dead_code, reason="Faithful representation of endpoint data")]
#[derive(Deserialize, Clone, Debug)]
pub struct Review {
    id: usize,
    user: String,
    rating: usize,
    text: String,
    has_spoilers: bool,
    is_public: bool,
    likes_count: usize,
    comments_count: usize,
    has_liked: bool,
    created_at: String,
    updated_at: String
}

impl Review {
    pub fn id(&self) -> usize {
        self.id
    }
}

#[allow(dead_code, reason="Faithful representation of endpoint data")]
#[derive(Deserialize, Clone, Debug)]
pub struct CommentResponse {
    count: usize,
    next: Option<String>,
    previous: Option<String>,
    results: Vec<Comment>,
}

#[allow(dead_code, reason="Faithful representation of endpoint data")]
#[derive(Deserialize, Clone, Debug)]
pub struct Comment {
    id: usize,
    user: String,
    review: usize,
    text: String,
    created_at: String,
    updated_at: String,
    can_edit: bool
}

async fn get_comments(review_id: usize) -> anyhow::Result<CommentResponse> {
    let endpoint = format!("/api/review/reviews/{review_id}/comments/");
    send_get_request(&endpoint).await
}

async fn like_review(book_id: usize, review_id: usize) {
    // TODO: Error Handling
    let _ = send_post_request("", &format!("/api/review/reviews/{book_id}/reviews/{review_id}/like/")).await;
}

async fn dislike_review(book_id: usize, review_id: usize) {
    // TODO: Error Handling
    let _ = send_delete_request(&format!("/api/review/reviews/{book_id}/reviews/{review_id}/like/")).await;
}

#[component]
pub fn comment(data: impl Fn() -> Comment + 'static) -> impl IntoView {
    view! {}
}

#[component]
pub fn review(data: impl Fn() -> Review + 'static) -> impl IntoView {
    let res = LocalResource::new(move || get_comments(data().id));
    let res = move || match &*res.read() {
        Some(Ok(data)) => Some(data.clone()),
        Some(Err(err)) => {
            log::log!(Level::Error, "{err}");
            None
        }
        None => None
    };

    let comments = move || res().map(|CommentResponse {results, ..}| results).unwrap_or_default();

    view! {}
}