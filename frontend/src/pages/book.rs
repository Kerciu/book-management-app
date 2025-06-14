use crate::components::BookDetails;
use leptos::html::*;
use leptos::prelude::*;
use leptos::*;
use leptos_router::hooks::*;

#[component]
pub fn BookPage() -> impl IntoView {
    let navigate = use_navigate();
    let account_nav = navigate.clone();
    let list_nav = navigate.clone();

    let id = move || use_params_map().read().get("id");

    let id = Memo::new(move |_| match id() {
        None => -1_isize as usize,
        Some(s) => match s.parse::<usize>() {
            Ok(num) => num,
            Err(_) => -1_isize as usize,
        },
    });

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
        <BookDetails id=move || id()/>

    }
}
