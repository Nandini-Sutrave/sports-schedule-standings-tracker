import tkinter as tk
from tkinter import ttk, messagebox
from Database import Database


class ResultEntry:
    def __init__(self, master, db):
        self.master = master
        self.db = db
        self.master.title("Results Entry")
        self.master.geometry("850x700")

        # Background frame
        results_frame = tk.Frame(self.master)
        results_frame.pack(fill="both", expand=True)
        bg_image = tk.PhotoImage(file='download.png')
        self.master.bg_image = bg_image  # Prevent garbage collection by saving a reference
        bg_label = tk.Label(results_frame, image=bg_image)
        bg_label.place(relwidth=1, relheight=1)

        # Title
        title = tk.Label(results_frame, text="Results Entry", font=("Arial", 18, "bold"), bg="white", fg="black")
        title.pack(pady=10)

        # Tournament selection
        tk.Label(results_frame, text="Select Tournament:", font=("Arial", 14), bg="white").pack(pady=5)
        self.tournament_dropdown = ttk.Combobox(results_frame, font=("Arial", 14), state="readonly")
        self.tournament_dropdown.pack(pady=5)

        self.matches_tree = ttk.Treeview(results_frame, columns=("Match ID", "Team 1", "Team 2"),
                                         show="headings", height=10)
        self.matches_tree.heading("Match ID", text="Match ID")
        self.matches_tree.heading("Team 1", text="Team 1")
        self.matches_tree.heading("Team 2", text="Team 2")
        self.matches_tree.pack(fill="both", expand=True, padx=20, pady=20)

        # Match ID Dropdown
        tk.Label(results_frame, text="Select Match ID:", font=("Arial", 14), bg="white").pack(pady=5)
        self.match_id_dropdown = ttk.Combobox(results_frame, font=("Arial", 14), state="readonly")
        self.match_id_dropdown.pack(pady=5)

        # Winner Dropdown
        tk.Label(results_frame, text="Select Winner:", font=("Arial", 14), bg="white").pack(pady=5)
        self.winner_dropdown = ttk.Combobox(results_frame, font=("Arial", 14), state="readonly")
        self.winner_dropdown.pack(pady=5)

        # Manual Entry Section
        entry_frame = tk.Frame(results_frame, bg="white")
        entry_frame.pack(pady=20)

        tk.Label(entry_frame, text="Team 1 Score:", font=("Arial", 14), bg="white").grid(row=0, column=0, padx=10, pady=5)
        self.team1_score_entry = tk.Entry(entry_frame, font=("Arial", 14))
        self.team1_score_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(entry_frame, text="Team 2 Score:", font=("Arial", 14), bg="white").grid(row=1, column=0, padx=10, pady=5)
        self.team2_score_entry = tk.Entry(entry_frame, font=("Arial", 14))
        self.team2_score_entry.grid(row=1, column=1, padx=10, pady=5)

        # Submit Button
        tk.Button(entry_frame, text="Submit", font=("Arial", 14), bg="green", fg="white",
                  command=self.submit_result).grid(row=2, column=0, columnspan=2, pady=10)

        # Populate dropdowns and setup bindings
        self.populate_tournament_dropdown()
        self.tournament_dropdown.bind("<<ComboboxSelected>>", self.load_matches)
        self.match_id_dropdown.bind("<<ComboboxSelected>>", self.populate_winner_dropdown)

    def populate_tournament_dropdown(self):
        """Populate tournament dropdown from the database."""
        tournaments = self.db.get_tournaments()
        self.tournament_dropdown["values"] = [f"{t[0]}: {t[1]}" for t in tournaments]

    def load_matches(self, event):
        """Load matches for the selected tournament."""
        selected_tournament = self.tournament_dropdown.get()
        if selected_tournament:
            tournament_id = int(selected_tournament.split(":")[0])
            matches = self.db.get_matches(tournament_id)
            self.match_id_dropdown["values"] = [f"{match[0]}" for match in matches]
            self.matches = {match[0]: (match[1], match[2]) for match in matches}
            self.matches_tree.delete(*self.matches_tree.get_children())  # Clear existing matches
            for match in matches:
                self.matches_tree.insert("", "end", values=(match[0], match[1], match[2]))

    def populate_winner_dropdown(self, event):
        """Populate the winner dropdown with team names from the selected match."""
        selected_match_id = self.match_id_dropdown.get()
        if selected_match_id:
            team1, team2 = self.matches[int(selected_match_id)]
            self.winner_dropdown["values"] = [team1, team2, "Tie"]

    def submit_result(self):
        """Submit match results."""

        tour_id = self.tournament_dropdown.get().split(":")[0]
        match_id = self.match_id_dropdown.get()
        team_1, team_2 = self.matches[int(match_id)]
        print(team_1,team_2)
        score_team1 = self.team1_score_entry.get()
        score_team2 = self.team2_score_entry.get()
        winner = self.winner_dropdown.get()

        # Validate inputs
        if not match_id or not score_team1.isdigit() or not score_team2.isdigit() or not winner:
            messagebox.showerror("Error", "Please fill in all fields with valid data.")
            return

        # Update the database
        self.db.insert_match_result(int(tour_id),team_1,team_2,int(match_id), int(score_team1), int(score_team2), winner)
        messagebox.showinfo("Success", "Match results saved successfully!")
        self.load_matches(None)  # Refresh the matches


