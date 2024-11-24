import tkinter as tk
from tkinter import ttk
from setup_tournament import SetupTournament
from resultEntry import ResultEntry
from match_schedule import MatchSchedulePage
from standings import Standings
from Database import Database


class Dashboard:
    def __init__(self,root):
        root.title("Sports Schedule & Standings Tracker")
        root.geometry("850x700")

        # Create a Notebook widget
        notebook = ttk.Notebook(root)

        db = Database()

        # Tabs for the application
        tab1 = tk.Frame(notebook, bg="white")
        tab2 = tk.Frame(notebook, bg="white")
        tab3 = tk.Frame(notebook, bg="white")
        tab4 = tk.Frame(notebook, bg="white")
        tab5 = tk.Frame(notebook, bg="white")

        notebook.add(tab1, text="Tournament Setup")
        notebook.add(tab2, text="Match Schedule")
        notebook.add(tab3, text="Results Entry")
        notebook.add(tab4, text="Leaderboard")
        notebook.add(tab5, text="Reports")

        notebook.pack(fill="both", expand=True)

        def open_setup_tournament():
            new_window = tk.Toplevel(root)  # Create a new top-level window
            SetupTournament(new_window, db)  # Pass the new window and database instance to SetupTournament
        def open_match_schedule():
            new_window = tk.Toplevel(root)
            MatchSchedulePage(new_window, db)
        # Function to open the Results Entry page in a new window
        def open_results_entry():
            new_window = tk.Toplevel(root)  # Create a new top-level window
            ResultEntry(new_window, db)  # Pass the new window and database instance to ResultEntry
        def open_standings():
            new_window = tk.Toplevel(root)
            Standings(new_window, db)

        # Create the homepage
        homepage = tk.Frame(root)
        homepage.pack(fill="both", expand=True)
        bg_image = tk.PhotoImage(file='download.png')
        root.bg_image = bg_image  # Prevent garbage collection by saving a reference
        bg_label = tk.Label(homepage, image=bg_image)
        bg_label.place(relwidth=1, relheight=1)

        # Title (with contrasting color for readability)
        title = tk.Label(
            homepage,
            text="Sports Schedule & Standings Tracker",
            font=("Arial Rounded MT Bold", 24, "bold"),
            bg="#D4EBF8",
            fg="black"
        )
        title.pack(pady=50)

        info_label = tk.Label(
            homepage,
            text="Welcome to the Sports \nSchedule & Standings Tracker!\n"
                 "Use the buttons to create tournaments,\n manage schedules,\n enter results, view leaderboards,\n and generate reports.",
            font=("Britannic Bold", 14),
            bg='#FEF9D9',
            fg="black",
            width=35,
            height=10,
            justify='center'
        )
        info_label.pack(pady=10)

        # Buttons on the homepage
        button_texts = [
            ("Create Tournament", 0, "black", open_setup_tournament),
            ("Match Schedule", 1, "black", open_match_schedule),
            ("Results Entry", 2, "black", open_results_entry),
            ("Leaderboard", 3, "black", open_standings),
            ("Reports", 4, "black", None),
        ]

        for text, index, color,function in button_texts:
            tk.Button(
                homepage,
                text=text,
                font=("Helvetica", 14),
                bg=color,
                fg="white",
                width=30,
                command=function,
                justify='center'
            ).pack(pady=10)







# Run the dashboard
if __name__ == "__main__":
    root = tk.Tk()
    dash = Dashboard(root)
    root.mainloop()

