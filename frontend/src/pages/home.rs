use leptos::*;
use leptos::html::*;
#[component]
pub fn HomePage() -> impl IntoView {
    view! {
                <main>
                    <div class="home-page-welcome-text" >"Witaj w BookUp"</div>
                    <div class="container-flex">
                        <div class="text-lines">"Zacznij korzystać z BookUp"</div>
                        <div class="text-lines-bold">"BookUp to innowacyjna aplikacja do zarządzania kolekcją książek, która umożliwia dodawanie, ocenianie, recenzowanie i dzielenie się książkami z przyjaciółmi"</div>
                        <div class="text-lines">"Dołącz już dziś!"</div>
                        <button class="button-pop">"Dołącz teraz"</button>
                    </div>
                    <div style="display: flex; gap: 0px; align-items: center; margin-left: 20px; margin-right: 20px; margin-top: 80px;">
                        <img src="https://static.wixstatic.com/media/117514_dc6b7bd47a3e42df8ab688dd92fe65c5~mv2.png" style="width: 25vw; height: 316px; object-fit: cover;"></img>
                        <img src="https://static.wixstatic.com/media/117514_104f3b1d8fa54b85844945832ca0ec49~mv2.png" style="width: 75vw; height: 316px; object-fit: cover;"></img>
                    </div>
                    <div class="white-section">
                        <div style="height:60px"></div>
                        <div class="container-flex">
                            <div class="text-side">
                                <div class="title-text-home-page">"Informacje"</div>
                                <div class="body-text">"BookUp to aplikacja stworzona z myślą o pasjonatach książek. Nasza platforma umożliwia łatwe dodawanie książek do własnej kolekcji, ich ocenę, pisanie recenzji oraz udostępnianie rekomendacji z przyjaciółmi. Dzięki BookUp możesz odkrywać nowe tytuły i dzielić się swoimi ulubionymi lekturami z innymi."</div>
                                <button class="button-pop-reverse">"Dowiedź się więcej"</button>
                            </div>
                            
                            <img src="https://static.wixstatic.com/media/117514_947e901d593448e98241dfe06415d791~mv2.png" alt="Description" class="image-side"></img>
                        </div>
                        <div class="text-title">"Nasze usługi"</div>
                        <div class="container-flex">
                            <div>
                              <img ssrc="https://static.wixstatic.com/media/117514_2210c99136a548e882210b1319375561~mv2.png" style="width: auto; height: 295px; object-fit: cover;"></img>
                              <div class="title-text-home-page">"Dodawanie Książek"</div>
                              <div class="body-text">"Dodawaj swoje ulubione książki do personalnej kolekcji w BookUp i miej do nich zawsze łatwy dostęp."</div>
                            </div>
                        </div>

                    </div>

                    <footer>
                        <p>"© 2025 BookUp"</p>
                    </footer>
                </main>
    }
}