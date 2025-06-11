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
                <div class="text-title" style="color: #FFFFFF; margin-left:0px; font-size: 30px; margin-top:0px;">{name}</div>
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
        <div class="controls">
            <input type="text" placeholder="Search friends..." class="search-input" style="align-items: center; margin-top: 0px;"/>
            <input type="text" placeholder="Add friend by username..." class="search-input" style="align-items: center; margin-top: 0px;"/>
            <button  class="btn-primary" style="align-items: center;">"Add Friend"</button>
        </div>
        <FriendInfo friend=friend_temp />
    }
}
