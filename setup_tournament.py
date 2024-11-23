import tkinter as tk
from tournament import Tournament
from Database import *


class SetupTournament:
    def __init__(self, master, db):
        self.master = master
        self.db = db
        self.master.title("Setup Tournament")
        self.master.geometry("750x800")

        header = tk.Label(self.master, text="Choose Sport", font=("Arial", 20))
        header.pack(pady=20)

        cricket_button = tk.Button(
            self.master, text="Cricket", width=20, bg="lightgreen", font=("Arial", 14),
            command=lambda: self.open_tournament_page("Cricket")
        )
        cricket_button.pack(pady=10)

        football_button = tk.Button(
            self.master, text="Football", width=20, bg="lightblue", font=("Arial", 14),
            command=lambda: self.open_tournament_page("Football")
        )
        football_button.pack(pady=10)

    def open_tournament_page(self, sport):
        new_window = tk.Toplevel(self.master)
        Tournament(new_window, self.db, sport)
        #self.master.destroy()


