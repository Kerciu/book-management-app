use leptos::prelude::*;
use log::Level;
use serde::{Deserialize, Serialize};

use crate::components::{handle_request, send_get_request};

#[derive(Serialize, Clone, Debug, Default)]
struct CategoryRequest {
    name: String,
}

#[derive(Deserialize, Clone, Debug, Default)]
struct Category {
    id: usize,
    name: String,
}

#[derive(Deserialize, Clone, Debug, Default)]
struct CategoryResponse {
    count: usize,
    next: Option<String>,
    previous: Option<String>,
    results: Vec<Category>,
}

async fn get(request: CategoryRequest) -> anyhow::Result<Vec<CategoryResponse>> {
    const ENDPOINT: &str = "/api/book/genres/";
    let endpoint = format!("{ENDPOINT}?name={}", request.name);
    let mut res: CategoryResponse = send_get_request(&endpoint).await?;
    let mut ret = vec![res];

    while let Some(ref endpoint) = ret.last().unwrap().next {
        res = send_get_request(endpoint).await?;
        ret.push(res);
    }

    Ok(ret)
}

#[component]
pub fn category_select_list(selected: WriteSignal<String>) -> impl IntoView {
    let send_request = handle_request(&get);

    let response = move || {
        if let Some(Ok(res)) = &*send_request.value().read() {
            Some(res.clone())
        } else {
            None
        }
    };

    let category_list = move || {
        let Some(arr) = response() else {
            return Default::default();
        };

        arr.into_iter()
            .map(|res| res.results)
            .flatten()
            .collect::<Vec<_>>()
    };

    let category_select_buttons = move || {
        category_list()
            .into_iter()
            .map(|cat| {
                view! {
                    <button on:click=move |_| { selected(cat.name.clone()) }>
                        {cat.name.clone()}
                    </button>
                    <br/>
                }
            })
            .collect_view()
    };

    view! {
        <input on:input:target=move |ev| {
            send_request.dispatch(CategoryRequest { name: ev.target().value() });
        } />
        <br/>
        "--------"
        <br/>
        {category_select_buttons}
    }
}
