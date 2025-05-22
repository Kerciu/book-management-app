use leptos::*;
use leptos::prelude::*;
use leptos::html::*;
use leptos_router::hooks::*;
use crate::components::BookDetails;
#[component]
pub fn BookPage() -> impl IntoView {
    let navigate = use_navigate();
    let account_nav = navigate.clone();
    let list_nav = navigate.clone();
    view! {
        <header>
            <button class="button-pop-ghost" style="margin-top: 0px;" on:click=move |_| {
                list_nav("/books/list", Default::default());
                }>"Book List"</button>
            <div class="spacer"></div>
            <button class="button-login" style="margin-top: 0px;" on:click=move |_| {
                account_nav("/account", Default::default());
                }>"Account"
            </button>
        </header>
        <BookDetails/>
        
    }
}