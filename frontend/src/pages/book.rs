use crate::components::BookDetails;
use leptos::html::*;
use leptos::prelude::*;
use leptos::*;
use leptos_router::hooks::*;

#[component]
pub fn BookPage() -> impl IntoView {
    let navigate = use_navigate();
    let account_nav = navigate.clone();
    let main_nav = navigate.clone();

    let id = move || use_params_map().read().get("id");

    let id = Memo::new(move |_| match id() {
        None => -1_isize as usize,
        Some(s) => match s.parse::<usize>() {
            Ok(num) => num,
            Err(_) => -1_isize as usize,
        },
    });

    view! {
        <header style="display: flex; align-items: center; justify-content: space-between; padding: 1rem;">
            
            <nav style="display: flex; justify-content: start; flex: 1;">
                
                <button class="nav-btn" on:click=move |_| {
                        main_nav("/main", Default::default());
                    }
                >
                    "Back"
                </button>
            </nav>
            
            //<div style="display: flex; justify-content: flex-end; flex: 1;">
            //    <button 
            //        class="button-login" 
             //       on:click=move |_| {
            //            account_nav("/account", Default::default());
            //        }
            //    >
            //        "Account"
            //    </button>
            //</div>
        </header>
        <BookDetails id=move || id()/>

    }
}
