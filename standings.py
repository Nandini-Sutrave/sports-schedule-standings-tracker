import tkinter as tk
from tkinter import ttk

class Standings:
    def __init__(self, master, db):
        self.master = master
        self.db = db
        self.master.title("Tournament Standings")
        self.master.geometry("800x600")

        # Dropdown for selecting a tournament
        self.tournament_label = tk.Label(master, text="Select Tournament:", font=("Arial", 14))
        self.tournament_label.pack(pady=10)

        self.tournament_dropdown = ttk.Combobox(master, state="readonly", width=40)
        self.tournament_dropdown.pack(pady=5)
        self.populate_tournaments()

        # Button to display standings
        self.show_button = tk.Button(master, text="Show Standings", command=self.display_standings)
        self.show_button.pack(pady=10)

        # Treeview to display standings
        self.tree = ttk.Treeview(master, show="headings", height=15)
        self.tree.pack(fill="both", expand=True, pady=10)

    def populate_tournaments(self):
        tournaments = self.db.get_tournaments()
        self.tournaments = {f"{t[1]} ({t[2]})": t for t in tournaments}  # Map display text to data
        self.tournament_dropdown["values"] = list(self.tournaments.keys())

    def display_standings(self):
        selected_tournament = self.tournament_dropdown.get()
        if not selected_tournament:
            return

        tournament_id, _, sport = self.tournaments[selected_tournament]

        # Fetch standings based on the sport
        standings = self.db.get_standings(tournament_id, sport)

        # Update Treeview columns dynamically
        self.update_tree_columns(sport)
        for row in self.tree.get_children():
            self.tree.delete(row)
        for data in standings:
            self.tree.insert("", "end", values=data)

    def update_tree_columns(self, sport):
        self.tree.delete(*self.tree.get_children())  # Clear existing rows
        if sport == "Cricket":
            columns = ("Tournament ID", "Team Name", "Wins", "Losses", "Net Run Rate", "Points")
        elif sport == "Football":
            columns = ("Tournament ID", "Team Name", "Wins", "Losses", "Goal Difference", "Points")

        self.tree["columns"] = columns
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")
