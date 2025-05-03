use leptos::prelude::*;

/// TODO: Replace with env String
const BACKEND: &'static str = "http://localhost:8000";

#[component]
fn App() -> impl IntoView {
    view! {}
}

fn main() {
    // better error logging
    console_log::init_with_level(log::Level::Trace).unwrap();
    console_error_panic_hook::set_once();

    // sets up app
    leptos::mount::mount_to_body(App);
}
