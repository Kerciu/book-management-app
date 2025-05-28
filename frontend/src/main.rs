#![feature(iter_intersperse)]

use leptos::prelude::*;
use leptos::*;
use leptos_meta::*;
use leptos_router::{components::*, path};
use web_sys::*;

mod auth;
mod components;
mod pages;
use crate::pages::{
    about::AboutPage, account::AccountPage, book::BookPage, home::HomePage, list::ListPage,
};
use crate::pages::{not_found::NotFound, sign::SignPage};
use components::*;

/// TODO: Replace with env String
const BACKEND: &'static str = "http://localhost:8000";

#[component]
pub fn App() -> impl IntoView {
    //provide_meta_context();

    let (cat_name, set_cat_name) = signal(String::new());

    view! {
        <Router>
            <Routes fallback=|| view! { <NotFound/> }>
                <Route path=path!("/") view=HomePage />
                <Route path=path!("/about") view=AboutPage />
                <Route path=path!("/books/list") view=ListPage />
                <Route path=path!("/books/details") view=BookPage />
                <Route path=path!("/account") view=AccountPage />
                <Route path=path!("/sign") view=SignPage />
            </Routes>
        </Router>
    }

    // view! {
    //     <Router>
    //         <Routes fallback=|| view! { NotFound }>
    //             <Route path=path!("/") view=HomePage />
    //             <Route path=path!("/about") view=AboutPage />
    //             <Route path=path!("/books/list") view=ListPage />
    //             <Route path=path!("/books/details") view=BookPage />
    //             <Route path=path!("/account") view=AccountPage />
    //
    //         </Routes>
    //     </Router>
    // }
}

fn main() {
    // better error logging
    console_log::init_with_level(log::Level::Trace).unwrap();
    console_error_panic_hook::set_once();

    // sets up app
    leptos::mount::mount_to_body(|| view! { <App/> });
}
