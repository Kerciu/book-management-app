use crate::components::{BookList, FriendList};
use leptos::html::*;
use leptos::prelude::*;
use leptos::*;
use leptos_router::hooks::*;

#[component]
pub fn ListPage() -> impl IntoView {
    let navigate = use_navigate();
    let account_nav = navigate.clone();
    let book_nav_temp = navigate.clone();
    view! {
        <header>
            <div class="spacer"></div>
            <button class="button-login" style="margin-top: 0px;" on:click=move |_| {
                account_nav("/account", Default::default());
                }>"Account"
            </button>
        </header>
        <div class="container-books-list-page" style ="padding-top:0px;">
            <div style="padding-right: 20vw;">
                <div class="text-title-list-page">"Books"</div>
                <BookList/>
                // book example
                // <div class="book-display" on:click=move |_| {
                //     book_nav_temp("/books/details", Default::default());
                //     }>
                //     <div class="container-flex" style="padding: 0px;">
                //         //image url
                //         <img src="https://ecsmedia.pl/cdn-cgi/image/format=webp,width=544,height=544,/c/the-rust-programming-language-2nd-edition-b-iext138640655.jpg" alt="Description" class="image-side" style="margin-top: 20px; padding-bottom:20px;"></img>
                //         <div class="text-side" style="margin-top: 20px;">
                //             <div class="text-title" style="color: #eadfe7; margin-left:0px;">{book.title.clone()}</div>
                //             <div class="body-text" style="color: #cfc3cd; margin-left:0px;">{format!("by {}", book.author)}</div>
                //             <div class="body-text" style="color: #cfc3cd; margin-left:0px;">{format!("Published: {}", book.published_at)}</div>
                //             <div class="body-text" style="color: #eadfe7; margin-left:0px; font-size: 20px; margin-top:10px;">
                //                 //description
                //                 "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."
                //             </div>
                //             <div class="categories-container" style="margin-top:10px;">
                //                 <div class="chips-container">
                //                     {book.categories.into_iter()
                //                         .map(|category| view! {
                //                             <span class="chip">{category}</span>
                //                         })
                //                         .collect_view()}
                //                 </div>
                //             </div>
                //         </div>
                //     </div>
                // </div>
                //book example
            </div>

            <div class="divider"></div>

            <div style="width: fit-content; padding-left: 20px;">
                <div class="text-title-list-page">"Friends"</div>
                <FriendList/>
            </div>
        </div>
    }
}

