use leptos::prelude::*;
use serde::Serialize;
use web_sys::window;

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

    let reload = move |ev: leptos::ev::MouseEvent| {
        if let Some(win) = window() {
            win.location().reload().unwrap();
        }
    };

    view! {
        <div style="display: flex;   flex-direction: row; align-items:center; margin-left:20px;">
            <div class="rating" style="align-items: center;">
                <input value="5" name="rating" id="star5" type="radio"
                    on:change=move |_| rating(5)></input>
                <label for="star5"></label>
                <input value="4" name="rating" id="star4" type="radio"
                    on:change=move |_| rating(4)></input>
                <label for="star4"></label>
                <input value="3" name="rating" id="star3" type="radio"
                    on:change=move |_| rating(3)></input>
                <label for="star3"></label>
                <input value="2" name="rating" id="star2" type="radio"
                    on:change=move |_| rating(2)></input>
                <label for="star2"></label>
                <input value="1" name="rating" id="star1" type="radio"
                    on:change=move |_| rating(1)></input>
                <label for="star1"></label>
            </div>
            <label for="spoilers" style="display: flex; align-items: center;  margin-left:20px; margin-top:5px;">"Has spoilers:"</label>
            <label class="container-checkbox" style="margin-top:5px; margin-left:10px;">
                <input type="checkbox"
                    bind:value=has_spoilers id="spoilers"></input>
                <div class="checkmark"></div>
            </label>
            <label for="public" style="display: flex; align-items: center;  margin-left:20px; margin-top:5px;">"Is public:"</label>
            <label class="container-checkbox" style="margin-top:5px; margin-left:10px;">
                <input type="checkbox"
                    bind:value=is_public id="public"></input>
                <div class="checkmark"></div>
            </label>
            <button class="btn-small" style="margin-left:10px; text-align: start; width:fit-content;  margin-top: 5px; margin-left:20px;" on:click=move |ev| { 
                send_request.dispatch((book_id(), request())); 
                reload(ev);
            }>"Submit"</button>
        </div>
        <div style="display: flex;   flex-direction: row; align-items:center; margin-left:20px; padding-bottom:100px;">
            <textarea placeholder="Write comment..." 
                class="styled-textarea"
                style="width:800px; margin-top:20px; resize: vertical; min-height: 40px; overflow-wrap: break-word;"
                oninput="this.style.height = ''; this.style.height = this.scrollHeight + 'px'"
                bind:value=text>
            </textarea>
        </div>
    }
}