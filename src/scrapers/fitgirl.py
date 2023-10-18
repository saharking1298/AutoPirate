from utils.scraper_utils import filter_search_results
from bs4 import BeautifulSoup
import urllib.parse


class FitgirlScraper:
    """
    This is a scraper for the following website: "https://fitgirl-repacks.site"
    """
    def __init__(self):
        self._url = "https://fitgirl-repacks.site/"
        self.load_selectors = {
            "searchPage": "h1",
            "gamePage": "img.alignleft"
        }

    def get_search_url(self, query: str) -> str:
        return self._url + "?" + urllib.parse.urlencode({"s": query})

    def get_search_results(self, page_content: str, search_query: str):
        soup = BeautifulSoup(page_content, "html.parser")
        headings = soup.select("h1.entry-title>a")
        meta_tags = soup.select("span.cat-links>a")
        results = {}
        for i in range(len(headings)):
            if "Lossless Repack" in meta_tags[i].text:
                results[headings[i].text] = headings[i]["href"]
        results = filter_search_results(search_query, results)
        return results

    def get_download_link(self, page_content: str) -> str:
        soup = BeautifulSoup(page_content, "html.parser")
        links = soup.select("div.entry-content li>a")
        for link in links:
            if link.text == "magnet":
                return link["href"]
