use leptos::prelude::*;


struct Friend {
    id: usize,
    name: String,
    collection_num: usize
}

#[component]
fn friend_info(friend: Friend) -> impl IntoView {
    let Friend {
        id,
        name,
        collection_num
    } = friend;
    let initials = name.split_whitespace()
        .take(2)
        .map(|word| word.chars().take(1).collect::<String>()) 
        .collect::<Vec<_>>()
        .join("");
    view! {
        <div class="friend-card" style ="margin-left: 20px; margin-right: 20px;">
            <div style="display: flex;   flex-direction: row; ">
                <div class="friend-avatar">{initials}</div>
                <div class="friend-info">
                    <h4 style="text-align: start; margin-top: 0px; margin-left:10px;">{name}</h4>
                    <p style="text-align: start; margin-left:10px;">{collection_num} books</p>
                </div>
            
            </div>
            <div class="friend-actions">
                    <button class="btn-small">"View Collection"</button>
                    <button class="btn-small btn-danger">"Remove"</button>
            </div>
        </div>
    }
}

fn get_example_friend() -> Friend {
        Friend {
            id: 1,
            name: "John Pork".to_string(),
            collection_num: 127
        }
    }

#[component]
pub fn friend_list() -> impl IntoView {



    view! {
        <div class="controls">
            <input type="text" placeholder="Search friends..." class="search-input" style="align-items: center; margin-top: 0px;"/>
            <input type="text" placeholder="Add friend by username..." class="search-input" style="align-items: center; margin-top: 0px;"/>
            <button  class="btn-primary" style="align-items: center;">"Add Friend"</button>
        </div>
        <div class="friends-grid">
            //temp solution for testing
            <FriendInfo friend=get_example_friend() />
            <FriendInfo friend=get_example_friend() />
            <FriendInfo friend=get_example_friend() />
            <FriendInfo friend=get_example_friend() />
            <FriendInfo friend=get_example_friend() />
            <FriendInfo friend=get_example_friend() />
            <FriendInfo friend=get_example_friend() />
            <FriendInfo friend=get_example_friend() />
            <FriendInfo friend=get_example_friend() />

        </div>
    }
}
