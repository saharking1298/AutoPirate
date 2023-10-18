import webbrowser
from scrapers import FitgirlScraper
from utils import Logger
from utils.webdrivers import initialize_browser, Browser
from utils.textutils import user_confirmation_dialog, multiple_choice_menu


class App:
    def __init__(self, headless: bool = True):
        self.driver = initialize_browser(Browser.CHROME, headless)
        self.scraper = FitgirlScraper()

    def test(self):
        pass

    def mainloop(self):
        text = input("Search for a game: ")
        url = self.scraper.get_search_url(text)
        Logger.log(f'Searching "{text}" on Fitgirl Repacks...')
        content = self.driver.get_page_content(url, self.scraper.load_selectors["searchPage"])
        results = self.scraper.get_search_results(content, text)
        if len(results) > 0:
            results["None of the above"] = None
            url = multiple_choice_menu("Please choose a game to download:", results)
            if type(url) is str:
                Logger.log("Inspecting game page on: " + url)
                content = self.driver.get_page_content(url, self.scraper.load_selectors["gamePage"])
                url = self.scraper.get_download_link(content)
                Logger.log("Opening download link: " + url)
                webbrowser.open(url)
        else:
            Logger.log("No games found!")

    def run(self):
        if user_confirmation_dialog("Run test (y/n)? ", "no"):
            self.test()
        while True:
            self.mainloop()


def main():
    app = App()
    app.run()


if __name__ == '__main__':
    main()
