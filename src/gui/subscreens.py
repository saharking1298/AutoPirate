from typing import Callable
import customtkinter as ctk


class GameSearchScreen(ctk.CTkFrame):
    def __init__(self, master: ctk.CTk, event_handler: Callable, fg_color: str):
        # Initializing frame
        super().__init__(master, fg_color=fg_color)
        self.event_handler = event_handler
        self.geometry = "300x400"

        # Adding UI elements
        self.search_label = ctk.CTkLabel(self, text="Search for a particular game:")
        self.search_label.pack()

        self.search_entry = ctk.CTkEntry(self, width=250, placeholder_text="Search for a game...")
        self.search_entry.bind("<Return>", self.on_game_search)
        self.search_entry.pack(pady=10)

        self.search_button = ctk.CTkButton(self, text="Search", command=self.on_game_search)
        self.search_button.pack(pady=10)

    def on_game_search(self, event=None) -> None:
        query = self.search_entry.get().strip()
        if len(query) > 0:
            self.event_handler("onGameSearch", query)
            self.search_entry.delete(0, ctk.END)


class ResultSelectionScreen(ctk.CTkFrame):
    def __init__(self, master: ctk.CTk, event_handler: Callable, fg_color: str):
        # Initializing frame
        super().__init__(master, fg_color=fg_color)
        self.event_handler = event_handler
        self.geometry = "700x500"

        # Adding UI elements
        self.default_label_text = "Searching Fitgirl Repacks..."
        self.text_label = ctk.CTkLabel(self, text=self.default_label_text)
        self.text_label.pack()

        self.button_container = ctk.CTkFrame(self, fg_color=fg_color)
        self.button_container.pack()

    def reset(self):
        # Clearing button container frame
        for widget in self.button_container.winfo_children():
            widget.destroy()

        # Reverting labels
        self.text_label.configure(text=self.default_label_text)

    def render_search_results(self, results: dict) -> None:
        # Setting label text
        label_text = self.default_label_text + f"\nFound {len(results) - 1} results:"
        self.text_label.configure(text=label_text)

        # Displaying search results
        for (game_title, game_page_url) in results.items():
            command = lambda url=game_page_url: self.on_game_pick(url)
            button = ctk.CTkButton(self.button_container, text=game_title, width=680, command=command)
            button.pack(pady=5)

        self.update()

    def on_game_pick(self, game_page_url: str):
        self.reset()
        self.event_handler("onGamePick", game_page_url)
