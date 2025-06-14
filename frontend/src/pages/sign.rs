use leptos::prelude::*;
use leptos_router::hooks::*;
use crate::components::{LoginForm, RegistractionForm};
#[component]
pub fn SignPage() -> impl IntoView {
    let (show_sign_up, set_show_sign_up) = signal(true);
    
    let query = use_query_map();
    let show = move || {
        query.with(|q| q
            .get("show_sign_up")
            .map(|s| s == "true")
            .unwrap_or(true))
    };
    Effect::new(move |_| {
        set_show_sign_up.set(show());
    });
    let box_style_left = move || {
        if show_sign_up() {
            "background: linear-gradient(to left, #d6b5dc, #ad7db6);"
        } else {
            "background: #2b083b;"
        }
    };
    let box_style_right = move || {
        if show_sign_up() {
            "background: #2b083b;"

        } else {
            "background: linear-gradient(to left, #d6b5dc, #ad7db6);"
        }
    };

    view! { 
        <div class="container">
            <div class="centered-box">
                <div class="container-flex" style="padding: 0px;">
                    <div class="box-left" style=box_style_left> 
                        <Show when=move || show_sign_up.get() fallback=move || 
                            view! {
                                <div class="title-text-sign" style="color:rgb(255, 255, 255); margin-left:0px; margin-top:184px;">"Sign in"</div>
                                <div class="container-flex" style="padding: 0px; align-items: center; justify-content: center;">
                                    <div class="social-container">
                                        <a href="#" class="social"><i class="fab fa-github"></i></a>
                                        <a href="#" class="social"><i class="fab fa-google"></i></a>
                                    </div>
                                </div>
                                <div class="body-text" style="color: #cac2ce; text-align: center; margin-top: 4px;">"or use your account"</div>
                                <LoginForm/>
                            }
                        >
                            <div class="title-text-sign">"Welcome Back!"</div>
                            <div class="body-text" style="color: #2b083b; text-align: center; margin-top: 20px;">"To keep connected with us please login"</div>
                            <div class="body-text" style="color: #2b083b; text-align: center; margin-top: 2px;">"with your personal info"</div>
                            <div class="container-flex" style="place-items: center; justify-content: center;">
                                <button class="button-ghost" on:click=move |_| set_show_sign_up(false)>"Sign in"</button>
                            </div>
                        </Show>
                    </div>
                    <div class="box-right" style=box_style_right>
                        <Show when=move || show_sign_up.get() fallback=move || 
                            view! {
                                <div class="title-text-sign">"Hello, Friend"</div>
                                <div class="body-text" style="color: #2b083b; text-align: center; margin-top: 20px;">"Enter your personal details and start"</div>
                                <div class="body-text" style="color: #2b083b; text-align: center; margin-top: 2px;">"jorney with us"</div>
                                <div class="container-flex" style="place-items: center; justify-content: center;">
                                    <button class="button-ghost" on:click=move |_| set_show_sign_up(true)>"Sign up"</button>
                                </div>
                            }
                        >   
                            <div class="title-text-sign" style="color:rgb(255, 255, 255); margin-left:0px; margin-top:12px;">"Sign up"</div>
                                <div class="container-flex" style="padding: 0px; align-items: center; justify-content: center;">
                                    <div class="social-container">
                                        <a href="#" class="social"><i class="fab fa-github"></i></a>
                                        <a href="#" class="social"><i class="fab fa-google"></i></a>
                                    </div>
                                </div>
                                <div class="body-text" style="color: #cac2ce; text-align: center; margin-top: 4px;">"or use your email for registration"</div>
                            <RegistractionForm/>
                        </Show>
                    </div>
                </div>
            </div>
        </div>
    }
}