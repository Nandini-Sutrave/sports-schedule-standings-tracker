import tkinter as tk
from tournament import Tournament
from Database import *


class SetupTournament:
    def __init__(self, master, db):
        self.master = master
        self.db = db
        self.master.title("Setup Tournament")
        self.master.geometry("550x500")

        # Main frame
        self.tournament_frame = tk.Frame(self.master)
        self.tournament_frame.pack(fill="both", expand=True)

        # Set the background image
        self.bg_image = tk.PhotoImage(file='match.png')  # Save as an attribute to prevent garbage collection
        bg_label = tk.Label(self.tournament_frame, image=self.bg_image)
        bg_label.place(relwidth=1, relheight=1)  # Fill the entire frame

        header = tk.Label(self.tournament_frame, text="Choose Sport", font=("Arial", 20))
        header.pack(pady=20)

        cricket_button = tk.Button(
            self.tournament_frame, text="Cricket", width=20, bg="black",fg="white", font=("Arial", 14),
            command=lambda: self.open_tournament_page("Cricket")
        )
        cricket_button.pack(pady=10)

        football_button = tk.Button(
            self.tournament_frame, text="Football", width=20, bg="black",fg="white", font=("Arial", 14),
            command=lambda: self.open_tournament_page("Football")
        )
        football_button.pack(pady=10)

    def open_tournament_page(self, sport):
        new_window = tk.Toplevel(self.master)
        Tournament(new_window, self.db, sport)
        #self.master.destroy()


