import sqlite3


class Database:
    def __init__(self):
        self.conn = sqlite3.connect("sports_tracker.db")
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tournaments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                sport TEXT NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS teams (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tournament_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                FOREIGN KEY (tournament_id) REFERENCES tournaments(id)
            )
        ''')
        self.conn.commit()

    def insert_tournament(self, name, sport):
        self.cursor.execute("INSERT INTO tournaments (name, sport) VALUES (?, ?)", (name, sport))
        self.conn.commit()

    def get_current_tournament_id(self):
        self.cursor.execute("SELECT last_insert_rowid()")
        return self.cursor.fetchone()[0]

    def add_team(self, tournament_id, team_name):
        self.cursor.execute("INSERT INTO teams (tournament_id, name) VALUES (?, ?)", (tournament_id, team_name))
        self.conn.commit()

    def close(self):
        self.conn.close()
