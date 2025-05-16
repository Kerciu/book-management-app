use leptos::prelude::*;

struct Book {
    id: usize,
    title: String,
    published_at: String,
    author: String,
    categories: Vec<String>,
}

fn get_example_book() -> Book {
        Book {
            id: 1,
            title: "The Rust Programming Language".to_string(),
            published_at: "2023-05-15".to_string(),
            author: "Steve Klabnik & Carol Nichols".to_string(),
            categories: vec![
                "Programming".to_string(),
                "Rust".to_string(),
                "Technology".to_string(),
            ],
        }
    }

#[component]
pub fn book_details() -> impl IntoView {
    let book = get_example_book();

    view! {
        <div class="container-flex-row" style="padding: 0px;">
            //image url
            <img src="https://ecsmedia.pl/cdn-cgi/image/format=webp,width=544,height=544,/c/the-rust-programming-language-2nd-edition-b-iext138640655.jpg" alt="Description"  style="margin-top: 20px; margin-left:20px; padding-bottom:20px; height:500px;"></img>
            <div class="text-side" style="margin-top: 20px;">
                <div class="text-title" style="color: #FFFFFF; margin-left:0px;">{book.title.clone()}</div>
                <div class="body-text" style="color: #cac1ce; margin-left:0px;">{format!("by {}", book.author)}</div>
                <div class="body-text" style="color: #cac1ce; margin-left:0px;">{format!("Published: {}", book.published_at)}</div>
                <div class="categories-container" style="margin-top:10px;">
                    <div class="chips-container">
                        {book.categories.into_iter()
                            .map(|category| view! { 
                                <span class="chip">{category}</span> 
                            })
                            .collect_view()}
                    </div>
                </div>
            </div>
        </div>
        <div class="test-book-description">
                    //description
                    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
        </div>
    }
}