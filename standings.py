import tkinter as tk
from tkinter import ttk, messagebox

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
        try:
            tournaments = self.db.get_tournaments()
            if tournaments:
                self.tournaments = {f"{t[1]} ({t[2]})": t for t in tournaments}  # Map display text to data
                self.tournament_dropdown["values"] = list(self.tournaments.keys())
            else:
                messagebox.showinfo("Info", "No tournaments found in the database.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch tournaments: {str(e)}")

    def display_standings(self):
        selected_tournament = self.tournament_dropdown.get()
        if not selected_tournament:
            messagebox.showwarning("Warning", "Please select a tournament.")
            return

        tournament_id, _, sport = self.tournaments[selected_tournament]

        try:
            # Fetch standings based on the sport
            standings = self.db.get_standings(tournament_id, sport)

            # Update Treeview columns dynamically
            self.update_tree_columns(sport)
            for row in self.tree.get_children():
                self.tree.delete(row)

            if standings:
                for data in standings:
                    self.tree.insert("", "end", values=data)
            else:
                self.tree.insert("", "end", values=("No data available",) * len(self.tree["columns"]))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to display standings: {str(e)}")

    def update_tree_columns(self, sport):
        # Define sport-specific columns
        if sport == "Cricket":
            columns = ("Tournament ID", "Team Name", "Wins", "Losses", "Net Run Rate", "Points")
        elif sport == "Football":
            columns = ("Tournament ID", "Team Name", "Wins", "Losses", "Goal Difference", "Points")
        else:
            columns = ("Tournament ID", "Team Name", "Wins", "Losses", "Points")  # Default case

        # Clear existing columns and rows
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = columns

        # Update column headings
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")
