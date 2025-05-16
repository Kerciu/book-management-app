use leptos::prelude::*;


struct Friend {
    id: usize,
    name: String,
}

#[component]
fn friend_info(friend: Friend) -> impl IntoView {
    let Friend {
        id,
        name
    } = friend;
    view! {
        <div style="border-bottom: 1px solid #eee;">
            <div class="container-flex-row" style="padding:0px; padding-bottom:10px; padding-top:20px;">
                <div class="text-title" style="color: #FFFFFF; margin-left:0px; font-size: 36px; margin-top:0px;">{name}</div>
                <button class="button-basic" style="width: auto; font-size: 14px;">"Share book"</button>
                <button class="button-basic" style="width: auto; font-size: 14px;">"View collection"</button>
            </div>
        </div>
    }
}

fn get_example_friend() -> Friend {
        Friend {
            id: 1,
            name: "John Pork".to_string(),
        }
    }

#[component]
pub fn friend_list() -> impl IntoView {
    let friend_temp = get_example_friend();

    view! {
        <div class="container-flex-row" style="padding:0px;">
            <input type="text" placeholder="Search" style="margin-left:0px; border-radius: 16px; height:19px; margin-top:0px;"/>
            <button class="button-pop" style="width: auto;">"Add"</button>
            <button class="button-pop" style="width: auto;">"Delete"</button>
        </div>
        <FriendInfo friend=friend_temp />
    }
}
