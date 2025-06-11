use crate::components::{BookList, FriendList};
use leptos::html::*;
use leptos::prelude::*;
use leptos::*;
use leptos_router::hooks::*;

#[component]
pub fn MainPage() -> impl IntoView {
    let navigate = use_navigate();
    let account_nav = navigate.clone();
    let book_nav_temp = navigate.clone();
    let (show_recommendations, set_recommendations) = signal(true);
    let (show_books, set_books) = signal(false);
    let (show_my_books, set_my_books) = signal(false);
    let button_style_rec = move || {
        if show_recommendations() {
            "nav-btn active"

        } else {
            "nav-btn"
        }
    };
    let button_style_book_list = move || {
        if show_books() {
            "nav-btn active"

        } else {
            "nav-btn"
        }
    };
    let button_style_books = move || {
        if show_my_books() {
            "nav-btn active"

        } else {
            "nav-btn"
        }
    };
    let button_style_friends = move || {
        if !show_books() && !show_recommendations() && !show_my_books() {
            "nav-btn active"

        } else {
            "nav-btn"
        }
    };
    view! {
        <header style="display: flex; align-items: center; justify-content: space-between; padding: 1rem;">
            <div class="text-title" style="margin-top: 0px; flex: 1;">"BookUp"</div>
            
            <nav style="display: flex; justify-content: center; flex: 1;">
                
                <button class=button_style_rec on:click=move |_| {
                        set_books(false); 
                        set_my_books(false);
                        set_recommendations(true);
                    }
                >
                    "Recommendations"
                </button>
                <button class=button_style_books on:click=move |_| {
                        set_books(true); 
                        set_my_books(false);
                        set_recommendations(false);
                    }
                >
                    "Book List"
                </button>
                <button class=button_style_books on:click=move |_| {
                        set_books(false); 
                        set_my_books(true);
                        set_recommendations(false);
                    }
                >
                    "My Books"
                </button>
                <button  class=button_style_friends on:click=move |_| {
                        set_books(false); 
                        set_my_books(false);
                        set_recommendations(false);
                    }
                >
                    "Friends"
                </button>
            </nav>
            
            <div style="display: flex; justify-content: flex-end; flex: 1;">
                <button 
                    class="button-login" 
                    on:click=move |_| {
                        account_nav("/account", Default::default());
                    }
                >
                    "Account"
                </button>
            </div>
        </header>
        <div class="section active">
            <Show when=move || !show_recommendations.get() fallback=move || 
                    //Recomendation section
                    view! {
                        <div class="section-header">
                            <h2>"Recommended for You"</h2>
                            <p>"Discover your next favorite book"</p>
                        </div>

                    }
            > 
                <Show when=move || !show_books.get() fallback=move || 
                    //Book List section
                    view! {
                        <div class="section-header">
                            <h2>"Book List"</h2>
                            <p>"Check the list of books to broaden your horizons"</p>
                            <BookList/>
                        </div>

                    }
                > 
                    <Show when=move || !show_my_books.get() fallback=move || 
                        //My books section
                        view! {
                            <div class="section-header">
                                <h2>"My Library"</h2>
                            </div>

                        }
                    > 
                        //Friends section
                        <div class="section-header">
                                <h2>"Friends"</h2>
                                <FriendList/>
                        </div>
                    </Show>
                </Show>
            </Show>
        </div>
    }
}
