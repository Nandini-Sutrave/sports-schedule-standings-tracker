import tkinter as tk
from tkinter import ttk
from setup_tournament import SetupTournament
from Database import Database



# Function to navigate to specific tabs
def navigate_to_tab(notebook, tab_index):
    notebook.select(tab_index)


# Function to create the main dashboard
def create_dashboard():
    # Create the main window
    root = tk.Tk()
    root.title("Sports Schedule & Standings Tracker")
    root.geometry("850x700")

    db = Database()

    # Create a Notebook widget
    notebook = ttk.Notebook(root)

    # Tabs for the application
    tab1 = tk.Frame(notebook, bg="white")
    tab2 = tk.Frame(notebook, bg="white")
    tab3 = tk.Frame(notebook, bg="white")
    tab4 = tk.Frame(notebook, bg="white")
    tab5 = tk.Frame(notebook, bg="white")

    # Adding tabs to the notebook
    notebook.add(tab1, text="Tournament Setup")
    notebook.add(tab2, text="Match Schedule")
    notebook.add(tab3, text="Results Entry")
    notebook.add(tab4, text="Leaderboard")
    notebook.add(tab5, text="Reports")

    # Adding Notebook but hiding it initially
    notebook.pack(fill="both", expand=True)
    notebook.pack_forget()

    # Create the homepage
    homepage = tk.Frame(root)
    homepage.pack(fill="both", expand=True)
    bg_image = tk.PhotoImage(file="download.png")
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
        ("Create Tournament", 0, "black"),
        ("Match Schedule", 1, "black"),
        ("Results Entry", 2, "black"),
        ("Leaderboard", 3, "black"),
        ("Reports", 4, "black"),
    ]

    for text, index, color in button_texts:
        tk.Button(
            homepage,
            text=text,
            font=("Helvetica", 14),
            bg=color,
            fg="white",
            width=30,
            command=lambda idx=index: navigate_to_tab(notebook, idx),
            justify='center'
        ).pack(pady=10)

    # Create a database instance
    db = Database()

    def open_setup_tournament():
        # Open SetupTournament in a new Toplevel window
        new_window = tk.Toplevel(root)
        SetupTournament(new_window, db)

    tk.Button(
        homepage,
        text="Create Tournament",
        font=("Helvetica", 14),
        bg="green",
        fg="white",
        width=30,
        command=open_setup_tournament
    ).pack(pady=10)

    # Start the main loop
    root.mainloop()


# Run the dashboard
if __name__ == "__main__":
    create_dashboard()
