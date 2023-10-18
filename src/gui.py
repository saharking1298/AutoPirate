import customtkinter as ctk
import webbrowser
from gui.enums import AppearanceMode
from gui.subscreens import GameSearchScreen, ResultSelectionScreen
from utils.webdrivers import initialize_browser, Browser
from utils import Logger
from scrapers import FitgirlScraper

BROWSER = Browser.CHROME


class App(ctk.CTk):
    def __init__(self, appearance_mode: AppearanceMode = AppearanceMode.SYSTEM, browser_headless: bool = True):
        # Initializing window
        super().__init__()
        self.fg_color = self.cget("fg_color")
        self.events = {
            "onGameSearch": self.on_game_search,
            "onGamePick": self.on_game_pick,
        }

        # Setting window properties
        ctk.set_appearance_mode(appearance_mode.value)
        self.title("AutoPirate")
        self.geometry("300x400")
        self.resizable(False, True)

        # Adding UI elements
        self.heading = ctk.CTkLabel(self, text="AutoPirate", font=(None, 30))
        self.heading.pack(pady=5)

        # Initializing web driver and scraper
        self.browser = initialize_browser(BROWSER, headless=browser_headless)
        self.scraper = FitgirlScraper()

        # Adding frames
        self.current_screen = None
        self.game_search_screen = GameSearchScreen(self, self.event_handler, self.fg_color)
        self.result_selection_screen = ResultSelectionScreen(self, self.event_handler, self.fg_color)
        self.show_screen(self.game_search_screen)

    def event_handler(self, event: str, *args, **kwargs):
        if event not in self.events:
            raise ValueError("Event doesn't exist: " + event)
        return self.events[event](*args, **kwargs)
    
    def show_screen(self, screen: ctk.CTkFrame):
        # Hiding current screen
        if isinstance(self.current_screen, ctk.CTkFrame):
            self.current_screen.pack_forget()

        # Resizing app window according to the new screen
        if hasattr(screen, "geometry"):
            self.geometry(screen.geometry)

        # Setting current screen and showing it
        self.current_screen = screen
        self.current_screen.pack()
        self.update()

    def on_game_search(self, query: str):
        # Showing search results screen
        self.show_screen(self.result_selection_screen)
        Logger.log(f'Searching "{query}" on Fitgirl Repacks...')

        # Getting search results
        search_page_url = self.scraper.get_search_url(query)
        search_page_content = self.browser.get_page_content(search_page_url, self.scraper.load_selectors["searchPage"])
        search_results = self.scraper.get_search_results(search_page_content, query)
        search_results["None of the above"] = None
        Logger.log(f"Found {len(search_results) - 1} results!")
        self.result_selection_screen.render_search_results(search_results)

    def on_game_pick(self, game_page_url: str):
        # Showing search screen
        self.show_screen(self.game_search_screen)

        Logger.log("Inspecting game page on: ", game_page_url)
        if type(game_page_url) is str:
            # Getting download link
            game_page_content = self.browser.get_page_content(game_page_url, self.scraper.load_selectors["gamePage"])
            download_link = self.scraper.get_download_link(game_page_content)
            # Opening download link on browser
            Logger.log("Found download link: " + download_link)
            webbrowser.open(download_link)


def main():
    Logger.log("Starting application...")
    app = App(AppearanceMode.DARK)
    app.mainloop()


if __name__ == '__main__':
    main()
