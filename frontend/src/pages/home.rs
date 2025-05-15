use leptos::*;
use leptos::html::*;
#[component]
pub fn HomePage() -> impl IntoView {
    view! {
                <main>
                    <header>
                        <div class="spacer"></div>
                        <button class="button-login" style="margin-top: 0px;">"Log in"</button>
                    </header>
                    <div class="home-page-welcome-text" >"Welcome in BookUp"</div>
                    <div class="container-flex">
                        <div class="text-lines">"Start using BookUp"</div>
                        <div class="text-lines-bold">"BookUp is an innovative app for managing your book collection, allowing you to add, rate, review, and share books with friends"</div>
                        <div class="text-lines">"Join now!"</div>
                        <button class="button-pop">"Sign up"</button>
                    </div>
                    <div style="display: flex; gap: 0px; align-items: center; margin-left: 20px; margin-right: 20px; margin-top: 80px;">
                        <img src="https://static.wixstatic.com/media/117514_dc6b7bd47a3e42df8ab688dd92fe65c5~mv2.png" style="width: 25vw; height: 316px; object-fit: cover;"></img>
                        <img src="https://static.wixstatic.com/media/117514_104f3b1d8fa54b85844945832ca0ec49~mv2.png" style="width: 75vw; height: 316px; object-fit: cover;"></img>
                    </div>
                    <div class="white-section">
                        <div style="height:60px"></div>
                        <div class="container-flex">
                            <div class="text-side">
                                <div class="title-text-home-page">"About BookUp"</div>
                                <div class="body-text">"BookUp is an app designed for book enthusiasts. Our platform makes it easy to add books to your personal collection, rate them, write reviews, and share recommendations with friends. With BookUp, you can discover new titles and share your favorite reads with others."</div>
                                <button class="button-pop-reverse" onclick="window.location.href='about'">"Learn more about us!"</button>
                            </div>
                            
                            <img src="https://static.wixstatic.com/media/117514_947e901d593448e98241dfe06415d791~mv2.png" alt="Description" class="image-side"></img>
                        </div>
                        <div class="text-title">"Our features"</div>
                        <div class="container-flex">
                            <div>
                              <img src="https://static.wixstatic.com/media/117514_2210c99136a548e882210b1319375561~mv2.png" style="width: auto; height: 260px; object-fit: cover;"></img>
                              <div class="title-text-home-page">"Add books"</div>
                              <div class="body-text">"Add your favorite books to your personal collection in BookUp and always have easy access to them."</div>
                            </div>
                            <div>
                              <img src="https://static.wixstatic.com/media/117514_37fcd62e9aaf4e66952fcc110b120cb2~mv2.png" style="width: auto; height: 260px; object-fit: cover;"></img>
                              <div class="title-text-home-page">"Rate and review"</div>
                              <div class="body-text">"Rate the books you've read, write reviews, and share your thoughts with fellow literature lovers."</div>
                            </div>
                            <div>
                              <img src="https://static.wixstatic.com/media/117514_4fe1b1c971104a02a1a85ab189c79d55~mv2.png" style="width: auto; height: 260px; object-fit: cover;"></img>
                              <div class="title-text-home-page">"Social Features"</div>
                              <div class="body-text">"Create a book-loving community where literature enthusiasts can exchange recommendations, opinions, and reading inspirations."</div>
                            </div>
                            <div>
                              <img src="https://images.pexels.com/photos/8450123/pexels-photo-8450123.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1" style="width: auto; height: 260px; object-fit: cover;"></img>
                              <div class="title-text-home-page">"Sort and filter"</div>
                              <div class="body-text">"Sort and filter books just the way you want to find the ones that suit you best."</div>
                            </div>
                        </div>

                    </div>

                    <footer style="margin-left: 20px;">
                        <p>"© 2025 BookUp"</p>
                    </footer>
                </main>
    }
}