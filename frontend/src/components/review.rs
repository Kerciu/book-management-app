use leptos::prelude::*;
use log::Level;
use serde::Deserialize;

use crate::components::{handle_request, send_delete_request, send_get_request, send_post_request};

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

#[derive(Clone, Debug)]
struct LikeData {
    book_id: usize,
    review_id: usize,
    refetch_handle: Signal<()>
}

async fn get_comments(review_id: usize) -> anyhow::Result<CommentResponse> {
    let endpoint = format!("/api/review/reviews/{review_id}/comments/");
    send_get_request(&endpoint).await
}

async fn like_review(LikeData { book_id, review_id , refetch_handle}: LikeData) {
    // TODO: Error Handling
    let _ = send_post_request("", &format!("/api/review/reviews/{book_id}/reviews/{review_id}/like/")).await;
    let _ = refetch_handle();
}

async fn dislike_review(LikeData { book_id, review_id, refetch_handle }: LikeData) {
    // TODO: Error Handling
    let _ = send_delete_request(&format!("/api/review/reviews/{book_id}/reviews/{review_id}/like/")).await;
    let _ = refetch_handle();
}

#[component]
pub fn comment(data: Signal<Comment>) -> impl IntoView {
    let initials = move || data().user.split_whitespace()
        .take(2)
         .map(|word| word.chars().take(1).collect::<String>()) 
         .collect::<Vec<_>>()
        .join("");

    view! {
        <div style="padding-top:20px; padding-left:40px; padding-right:20px; border-bottom: 2px solid #8B5A96;">
            //user
            <div style="display: flex;   flex-direction: row; align-items:center;">
                <div class="friend-avatar">{move || initials()}</div>
                <div style="width:fit-content;">
                    //user name
                    <h4 style="text-align: start; margin-top: 0px; margin-left:10px; font-size: 20px;  margin-bottom: 0px;">{move || data().user}</h4>
                    <button class="btn-small" style="margin-left:10px; text-align: start; width:fit-content;  margin-top: 3px;">"View Collection"</button>
                </div>
            </div>
            //comment
            <div class="test-book-description" style = "max-width: 100%; word-wrap: break-word; overflow-wrap: break-word; margin-left:0px; text-align: start; padding-bottom:10px; fonr-size:16px;">
                {move || data().text}
            </div>
        </div>
    }
}

#[component]
pub fn review(book_id: Signal<usize>, data: Signal<Review>, refetch_handle: Signal<()>) -> impl IntoView {

    let name = move || data().user;
    let rating = move || data().rating;
    let text = move || data().text;
    let likes = move || data().likes_count;
    let review_id = move || data().id;

    let do_like = handle_request(&like_review);
    let do_dislike = handle_request(&dislike_review);

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

    let initials = move || name().split_whitespace()
        .take(2)
        .map(|word| word.chars().take(1).collect::<String>()) 
        .collect::<Vec<_>>()
        .join("");

    view! {
        <div class="book-card" style="margin-top:10px; width=max-content; padding-bottom:20px;">
             <div style="display: flex;   flex-direction: row; align-items:center;">
                <div class="friend-avatar">{move || initials()}</div>
                <div style="width:fit-content;">
                    //user name
                    <h4 style="text-align: start; margin-top: 0px; margin-left:10px; font-size: 20px;  margin-bottom: 0px;">{move || name()}</h4>
                    <button class="btn-small" style="margin-left:10px; text-align: start; width:fit-content;  margin-top: 3px;">"View Collection"</button>
                </div>
                //rating
                <div class="text-title" style= "font-size: 32px; color: #FFFFFF; place-items: start center;  margin-top: 0px;">
                    {move || rating()}"/5"
                </div>
            </div>
            //review text
            <div class="test-book-description" style = "max-width: 100%; word-wrap: break-word; overflow-wrap: break-word; margin-left:0px; text-align: start;">
                {move || text()}
            </div>
            //Likes
            <div>
                <button on:click=move |_| { do_like.dispatch(LikeData { book_id: book_id(), review_id: review_id(), refetch_handle }); }>"+"</button>
                {move || likes()}
                <button on:click=move |_| { do_dislike.dispatch(LikeData { book_id: book_id(), review_id: review_id(), refetch_handle }); }>"-"</button>

            </div>
            //Coments section
            //Write comment
            <div style="display: flex;   flex-direction: row; align-items:center; margin-left:0px;">
                <textarea placeholder="Write comment..." 
                    class="styled-textarea"
                    style="width:60%; margin-top:20px; resize: vertical; min-height: 40px; overflow-wrap: break-word;"
                    oninput="this.style.height = ''; this.style.height = this.scrollHeight + 'px'">
                </textarea>
                <button class="btn-small" style="margin-left:10px; text-align: start; width:fit-content;  margin-top: 0px;">"Write"</button>
            </div>
            //Coments
            <For
                each=move || comments().into_iter()
                key=|comment| comment.id
                children=move |comment| view! { <Comment data=Signal::derive(move || comment.clone()) /> }
            />
        </div>
    }
}