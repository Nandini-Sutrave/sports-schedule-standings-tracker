import tkinter as tk
from tkinter import ttk
from Database import Database
import sqlite3


class MatchSchedulePage:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        self.create_page()

    def create_page(self):
        # Frame for Match Schedule Page
        self.frame = tk.Frame(self.root, bg="white")
        self.frame.pack(fill="both", expand=True)

        # Title
        title = tk.Label(
            self.frame,
            text="Match Schedule",
            font=("TimesNewRoman", 20, "bold"),
            bg="sky blue",
            fg="black"
        )
        title.pack(pady=20)

        # Dropdown for Tournaments
        tournament_label = tk.Label(self.frame, text="Select Tournament:", font=("Helvetica", 14), bg="white")
        tournament_label.pack(pady=5)

        self.tournament_combo = ttk.Combobox(self.frame, state="readonly", width=50)
        self.tournament_combo.pack(pady=10)
        self.populate_tournaments()

        # Button to load teams
        load_teams_button = tk.Button(
            self.frame,
            text="Load Teams",
            font=("Helvetica", 12),
            bg="blue",
            fg="white",
            command=self.load_teams
        )
        load_teams_button.pack(pady=10)

        # Teams Listbox
        self.teams_listbox = tk.Listbox(self.frame, width=60, height=10)
        self.teams_listbox.pack(pady=10)

        # Button to Generate Match Schedule
        generate_schedule_button = tk.Button(
            self.frame,
            text="Generate Match Schedule",
            font=("Helvetica", 12),
            bg="green",
            fg="white",
            command=self.generate_match_schedule
        )
        generate_schedule_button.pack(pady=20)

    def populate_tournaments(self):
        """Fetch and populate tournaments in the dropdown."""
        self.db.cursor.execute("SELECT id, name FROM tournaments")
        tournaments = self.db.cursor.fetchall()
        self.tournament_combo['values'] = [f"{t[1]} (ID: {t[0]})" for t in tournaments]

    def load_teams(self):
        """Load teams for the selected tournament."""
        selected = self.tournament_combo.get()
        if not selected:
            tk.messagebox.showerror("Error", "Please select a tournament!")
            return

        # Extract Tournament ID
        tournament_id = int(selected.split("(ID: ")[1][:-1])

        # Fetch teams
        self.db.cursor.execute("SELECT name FROM teams WHERE tournament_id = ?", (tournament_id,))
        teams = self.db.cursor.fetchall()

        # Display in Listbox
        self.teams_listbox.delete(0, tk.END)
        for team in teams:
            self.teams_listbox.insert(tk.END, team[0])

    def generate_match_schedule(self):
        """Generate and display match schedule."""
        teams = self.teams_listbox.get(0, tk.END)
        if len(teams) < 2:
            tk.messagebox.showerror("Error", "At least two teams are required to generate a match schedule!")
            return

        # Simple round-robin schedule
        schedule = []
        for i in range(len(teams)):
            for j in range(i + 1, len(teams)):
                schedule.append((teams[i], teams[j]))

        # Display the schedule
        schedule_window = tk.Toplevel(self.root)
        schedule_window.title("Match Schedule")
        schedule_window.geometry("500x500")

        schedule_label = tk.Label(
            schedule_window, text="Generated Match Schedule", font=("Helvetica", 16, "bold")
        )
        schedule_label.pack(pady=10)

        schedule_listbox = tk.Listbox(schedule_window, width=50, height=20)
        schedule_listbox.pack(pady=10)

        for match in schedule:
            schedule_listbox.insert(tk.END, f"{match[0]} vs {match[1]}")

        # Save Schedule Option (if desired)
        save_button = tk.Button(
            schedule_window, text="Save Schedule", bg="green", fg="white", command=lambda: self.save_schedule(schedule)
        )
        save_button.pack(pady=10)

    def save_schedule(self, schedule):
        """Save the generated schedule into the database."""
        selected = self.tournament_combo.get()
        tournament_id = int(selected.split("(ID: ")[1][:-1])

        self.db.cursor.execute("CREATE TABLE IF NOT EXISTS matches (id INTEGER PRIMARY KEY AUTOINCREMENT, tournament_id INTEGER, team1 TEXT, team2 TEXT, FOREIGN KEY (tournament_id) REFERENCES tournaments(id))")
        for match in schedule:
            self.db.cursor.execute(
                "INSERT INTO matches (tournament_id, team1, team2) VALUES (?, ?, ?)",
                (tournament_id, match[0], match[1]),
            )
        self.db.conn.commit()
        tk.messagebox.showinfo("Success", "Match schedule saved successfully!")


# Example Usage

