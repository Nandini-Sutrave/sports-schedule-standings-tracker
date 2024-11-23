import tkinter as tk
from tkinter import ttk, messagebox
from Database import Database

class ResultEntry:
    def __init__(self,master,db):
        self.master = master
        self.master.title("Create Tournament")
        self.master.geometry("850x700")

        results_frame = tk.Frame(self.master)
        results_frame.pack(fill="both", expand=True)
        bg_image = tk.PhotoImage(file='download.png')
        self.master.bg_image = bg_image  # Prevent garbage collection by saving a reference
        bg_label = tk.Label(results_frame, image=bg_image)
        bg_label.place(relwidth=1, relheight=1)

        title = tk.Label(results_frame, text="Results Entry", font=("Arial", 18, "bold"), bg="white", fg="black")
        title.pack(pady=10)

        # Treeview to display matches
        matches_tree = ttk.Treeview(results_frame, columns=("Match ID", "Team 1", "Team 2", "Score 1", "Score 2"),
                                    show="headings")
        matches_tree.heading("Match ID", text="Match ID")
        matches_tree.heading("Team 1", text="Team 1")
        matches_tree.heading("Team 2", text="Team 2")
        matches_tree.heading("Score 1", text="Score 1")
        matches_tree.heading("Score 2", text="Score 2")
        matches_tree.pack(fill="both", expand=True, padx=20, pady=20)

        entry_frame = tk.Frame(results_frame, bg="white")
        entry_frame.pack(pady=20)

        tk.Label(entry_frame, text="Match ID:", font=("Arial", 14), bg="white").grid(row=0, column=0, padx=10, pady=5)
        match_id_entry = tk.Entry(entry_frame, font=("Arial", 14))
        match_id_entry.grid(row=0, column=1, padx=10, pady=5)
        tk.Label(entry_frame, text="Team 1 Score:", font=("Arial", 14), bg="white").grid(row=1, column=0, padx=10,
                                                                                         pady=5)
        team1_score_entry = tk.Entry(entry_frame, font=("Arial", 14))
        team1_score_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(entry_frame, text="Team 2 Score:", font=("Arial", 14), bg="white").grid(row=2, column=0, padx=10,
                                                                                         pady=5)
        team2_score_entry = tk.Entry(entry_frame, font=("Arial", 14))
        team2_score_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(entry_frame, text="Winner:", font=("Arial", 14), bg="white").grid(row=3, column=0, padx=10, pady=5)
        winner_dropdown = ttk.Combobox(entry_frame, font=("Arial", 14), state="readonly")
        winner_dropdown.grid(row=3, column=1, padx=10, pady=5)



        def populate_winner_dropdown(event):
            selected_item = matches_tree.focus()
            if selected_item:
                match_data = matches_tree.item(selected_item, "values")
                winner_dropdown["values"] = (match_data[1], match_data[2], "Tie")

        # Bind Treeview selection event to populate winner dropdown
        matches_tree.bind("<<TreeviewSelect>>", populate_winner_dropdown)

        # Submit button to save results
        def submit_result():
            match_id = match_id_entry.get()
            score_team1 = team1_score_entry.get()
            score_team2 = team2_score_entry.get()
            winner = winner_dropdown.get()

            # Validate inputs
            if not match_id or not score_team1.isdigit() or not score_team2.isdigit() or not winner:
                tk.messagebox.showerror("Error", "Please fill in all fields with valid data.")
                return

        tk.Button(entry_frame, text="Submit", font=("Arial", 14), bg="green", fg="white", command=submit_result).grid(
            row=4, column=0, columnspan=2, pady=10)








