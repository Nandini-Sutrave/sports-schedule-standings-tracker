import tkinter as tk
from tkinter import messagebox


class Tournament:
    def __init__(self, master, db, sport):
        self.master = master
        self.db = db
        self.sport = sport
        self.master.title("Create Tournament")
        self.master.geometry("500x400")

        self.tournament_name = tk.StringVar()

        # Header
        header = tk.Label(self.master, text=f"Setup {sport} Tournament", font=("Arial", 20), fg="green")
        header.pack(pady=20)

        # Tournament Name Input
        name_label = tk.Label(self.master, text="Tournament Name:", font=("Arial", 14))
        name_label.pack(pady=5)
        name_entry = tk.Entry(self.master, textvariable=self.tournament_name, width=30, font=("Arial", 12))
        name_entry.pack(pady=5)

        # Add Team Section
        team_label = tk.Label(self.master, text="Add Teams:", font=("Arial", 14))
        team_label.pack(pady=10)

        self.team_name_var = tk.StringVar()
        team_entry = tk.Entry(self.master, textvariable=self.team_name_var, width=30, font=("Arial", 12))
        team_entry.pack(pady=5)

        add_team_button = tk.Button(
            self.master, text="Add Team", bg="orange", command=self.add_team, font=("Arial", 12)
        )
        add_team_button.pack(pady=5)

        # Teams List
        self.team_listbox = tk.Listbox(self.master, width=40, height=10, font=("Arial", 12))
        self.team_listbox.pack(pady=10)

        # Create Tournament Button
        create_button = tk.Button(
            self.master, text="Create Tournament", bg="green", fg="white",
            font=("Arial", 14), command=self.create_tournament
        )
        create_button.pack(pady=10)

        # Internal Storage for Teams
        self.teams = []

    def add_team(self):
        team_name = self.team_name_var.get()
        if not team_name:
            messagebox.showerror("Error", "Please enter a team name!")
            return
        if team_name in self.teams:
            messagebox.showerror("Error", "Team already added!")
            return

        self.teams.append(team_name)
        self.team_listbox.insert(tk.END, team_name)
        self.team_name_var.set("")  # Clear entry after adding team

    def create_tournament(self):
        tournament_name = self.tournament_name.get()
        if not tournament_name or not self.teams:
            messagebox.showerror("Error", "Please provide a tournament name and add at least one team!")
            return

        try:
            # Save tournament in database
            self.db.insert_tournament(tournament_name, self.sport)
            tournament_id = self.db.get_current_tournament_id()

            # Save teams in database
            for team in self.teams:
                self.db.add_team(tournament_id, team)

            messagebox.showinfo("Success", f"Tournament '{tournament_name}' created successfully!")
            self.master.destroy()
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
