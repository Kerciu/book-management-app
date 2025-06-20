#![feature(iter_intersperse)]

use leptos::prelude::*;
use leptos_router::{components::*, path};

#[allow(unused_imports, reason="Fixes trunk error")]
use web_sys::*;

mod auth;
mod components;
mod pages;
use crate::pages::{
    about::AboutPage, account::AccountPage, book::BookPage, home::HomePage, main_page::MainPage, sign::SignPage,
};
use components::*;

/// TODO: Replace with env String
const BACKEND: &'static str = "http://localhost:8000";

#[component]
pub fn App() -> impl IntoView {
    //provide_meta_context();

    view! {
        <Router>
            <Routes fallback=|| view! { NotFound }>
                <Route path=path!("/github_auth") view=GithubAuthHandler />
                <Route path=path!("/google_auth") view=GoogleAuthHandler />
                <Route path=path!("/") view=HomePage />
                <Route path=path!("/about") view=AboutPage />
                <Route path=path!("/main") view=MainPage />
                <Route path=path!("/books/details/:id") view=BookPage />
                <Route path=path!("/account") view=AccountPage />
                <Route path=path!("/sign") view=SignPage />
                <Route path=path!("/verify_email") view=EmailVerificationForm />
                <Route path=path!("/books/select_collection/:id") view=ShelfSelect />
                <Route path=path!("/books/collections") view=ShelvesList />
            </Routes>
        </Router>
    }
}


fn main() {
    // better error logging
    console_log::init_with_level(log::Level::Trace).unwrap();
    console_error_panic_hook::set_once();

    // sets up app
    leptos::mount::mount_to_body(|| view! { <App/> });
}
