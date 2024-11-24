import sqlite3


class Database:
    def __init__(self):
        # Initialize the connection and cursor
        self.conn = sqlite3.connect("sports_tracker.db")
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Create tables if they don't already exist
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
        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS match_result (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tournament_id INTEGER NOT NULL,
                    match_id INTEGER NOT NULL,
                    team1 TEXT NOT NULL,
                    team2 TEXT NOT NULL,
                    score1 INTEGER DEFAULT 0,
                    score2 INTEGER DEFAULT 0,
                    winner TEXT,
                    FOREIGN KEY (tournament_id) REFERENCES tournaments(id)
                )
            ''')
        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS standings_cricket (
                    team_id INTEGER PRIMARY KEY,
                    tournament_id INTEGER,
                    wins INTEGER DEFAULT 0,
                    losses INTEGER DEFAULT 0,
                    net_run_rate REAL DEFAULT 0,
                    points INTEGER DEFAULT 0,
                    FOREIGN KEY (team_id) REFERENCES teams(id),
                    FOREIGN KEY (tournament_id) REFERENCES tournaments(id)
                )
            ''')
        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS standings_football (
                    team_id INTEGER PRIMARY KEY,
                    tournament_id INTEGER,
                    wins INTEGER DEFAULT 0,
                    losses INTEGER DEFAULT 0,
                    goal_difference INTEGER DEFAULT 0,
                    points INTEGER DEFAULT 0,
                    FOREIGN KEY (team_id) REFERENCES teams(id),
                    FOREIGN KEY (tournament_id) REFERENCES tournaments(id)
                )
            ''')
        self.conn.commit()

        self.cursor.execute("PRAGMA table_info(match_result);")
        columns = self.cursor.fetchall()
        for column in columns:
            print(column)

    def insert_tournament(self, name, sport):
        # Insert a new tournament
        self.cursor.execute("INSERT INTO tournaments (name, sport) VALUES (?, ?)", (name, sport))
        self.conn.commit()
        return self.cursor.lastrowid  # Return the ID of the inserted tournament

    def get_current_tournament_id(self):
        # Fetch the ID of the most recently inserted tournament
        self.cursor.execute("SELECT id FROM tournaments ORDER BY id DESC LIMIT 1")
        result = self.cursor.fetchone()
        return result[0] if result else None

    def add_team(self, tournament_id, team_name):
        # Add a team to a specific tournament
        self.cursor.execute("INSERT INTO teams (tournament_id, name) VALUES (?, ?)", (tournament_id, team_name))
        self.conn.commit()

    def fetch_teams(self, tournament_id):
        # Fetch all teams for a given tournament
        self.cursor.execute("SELECT name FROM teams WHERE tournament_id = ?", (tournament_id,))
        return [row[0] for row in self.cursor.fetchall()]

    def fetch_tournaments(self):
        # Fetch all tournaments
        self.cursor.execute("SELECT id, name, sport FROM tournaments")
        return self.cursor.fetchall()

    def get_tournaments(self):
        self.cursor.execute("SELECT id, name, sport FROM tournaments")
        return self.cursor.fetchall()

    def get_standings(self, tournament_id, sport):
        if sport == "Cricket":
            query = '''
                SELECT tournament_id, name, wins, losses, net_run_rate, points
                FROM standings_cricket AS st
                JOIN teams AS tm ON team_id = id
                WHERE tournament_id = ?
            '''
        elif sport == "Football":
            query = '''
                SELECT tournament_id, name, wins, losses, goal_difference, points
                FROM standings_football AS st
                JOIN teams AS tm ON team_id = id
                WHERE tournament_id = ?
            '''
        self.cursor.execute(query, (tournament_id,))
        return self.cursor.fetchall()

    def get_matches(self, tournament_id):
        """Get all matches for a tournament."""
        self.cursor.execute("SELECT id, team1, team2 FROM matches WHERE tournament_id=?", (tournament_id,))
        return self.cursor.fetchall()

    def insert_match_result(self, tournament_id, team1, team2,match_id, score1, score2, winner):
        """Insert match result into the database."""
        # Insert the match results
        self.cursor.execute("""
                INSERT INTO match_result (tournament_id, team1, team2, match_id, score1, score2, winner)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (tournament_id, team1, team2, match_id, score1, score2, winner))
        self.conn.commit()

        # Update standings based on the sport
        self.cursor.execute("SELECT tournament_id, team1, team2 FROM match_result WHERE id=?", (match_id,))
        tournament_id, team1, team2 = self.cursor.fetchone()

        self.cursor.execute("SELECT sport FROM tournaments WHERE id=?", (tournament_id,))
        sport = self.cursor.fetchone()[0]

        if sport == "Cricket":
            self.update_cricket_standings(tournament_id, team1, team2, score1, score2, winner)
        elif sport == "Football":
            self.update_football_standings(tournament_id, team1, team2, score1, score2, winner)

    def update_cricket_standings(self, tournament_id, team1, team2, score1, score2, winner):
        """Update cricket standings based on match results."""
        # Calculate net run rates
        total_runs = score1 + score2
        nrr_team1 = score1 / total_runs if total_runs > 0 else 0
        nrr_team2 = score2 / total_runs if total_runs > 0 else 0

        # Update standings for Team 1
        self.cursor.execute("""
            UPDATE standings_cricket
            SET net_run_rate = net_run_rate + ?,
                wins = wins + CASE WHEN ? = ? THEN 1 ELSE 0 END,
                losses = losses + CASE WHEN ? != ? THEN 1 ELSE 0 END,
                points = points + CASE WHEN ? = ? THEN 2 ELSE 0 END
            WHERE tournament_id = ? AND team_id = (SELECT id FROM teams WHERE name = ?)
        """, (nrr_team1, team1, winner, team1, winner, team1, winner, tournament_id, team1))

        # Update standings for Team 2
        self.cursor.execute("""
            UPDATE standings_cricket
            SET net_run_rate = net_run_rate + ?,
                wins = wins + CASE WHEN ? = ? THEN 1 ELSE 0 END,
                losses = losses + CASE WHEN ? != ? THEN 1 ELSE 0 END,
                points = points + CASE WHEN ? = ? THEN 2 ELSE 0 END
            WHERE tournament_id = ? AND team_id = (SELECT id FROM teams WHERE name = ?)
        """, (nrr_team2, team2, winner, team2, winner, team2, winner, tournament_id, team2))

        # Handle the case for a tie (no winner)
        if winner == "Tie":
            self.cursor.execute("""
                UPDATE standings_cricket
                SET points = points + 1
                WHERE tournament_id = ? AND team_id IN (
                    SELECT id FROM teams WHERE name IN (?, ?)
                )
            """, (tournament_id, team1, team2))

        self.conn.commit()

    def update_football_standings(self, tournament_id, team1, team2, score1, score2, winner):
        """Update football standings based on match results."""
        goal_difference_team1 = score1 - score2
        goal_difference_team2 = score2 - score1

        # Update standings for Team 1
        self.cursor.execute("""
            UPDATE standings_football
            SET goal_difference = goal_difference + ?,
                wins = wins + CASE WHEN ? = ? THEN 1 ELSE 0 END,
                losses = losses + CASE WHEN ? != ? THEN 1 ELSE 0 END,
                points = points + CASE WHEN ? = ? THEN 3 ELSE 0 END + CASE WHEN ? = 'Tie' THEN 1 ELSE 0 END
            WHERE tournament_id = ? AND team_id = (SELECT id FROM teams WHERE name = ?)
        """, (goal_difference_team1, team1, winner, team1, winner, team1, winner, team1, winner, tournament_id, team1))

        # Update standings for Team 2
        self.cursor.execute("""
            UPDATE standings_football
            SET goal_difference = goal_difference + ?,
                wins = wins + CASE WHEN ? = ? THEN 1 ELSE 0 END,
                losses = losses + CASE WHEN ? != ? THEN 1 ELSE 0 END,
                points = points + CASE WHEN ? = ? THEN 3 ELSE 0 END + CASE WHEN ? = 'Tie' THEN 1 ELSE 0 END
            WHERE tournament_id = ? AND team_id = (SELECT id FROM teams WHERE name = ?)
        """, (goal_difference_team2, team2, winner, team2, winner, team2, winner, team2, winner, tournament_id, team2))

        # Handle the case for a tie (both teams get 1 point each)
        if winner == "Tie":
            self.cursor.execute("""
                UPDATE standings_football
                SET points = points + 1
                WHERE tournament_id = ? AND team_id IN (
                    SELECT id FROM teams WHERE name IN (?, ?)
                )
            """, (tournament_id, team1, team2))

        self.conn.commit()

    def close(self):
        # Close the database connection
        self.conn.close()
