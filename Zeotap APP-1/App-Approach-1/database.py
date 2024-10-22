import sqlite3

class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.create_table()

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def create_table(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rules (
                id INTEGER PRIMARY KEY,
                rule_string TEXT,
                ast TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def insert_rule(self, rule_string, ast):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO rules (rule_string, ast) VALUES (?, ?)', (rule_string, ast))
        conn.commit()
        conn.close()

    def get_rules(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM rules')
        rules = cursor.fetchall()
        conn.close()
        return rules

class RuleNode:
    def __init__(self, type, left=None, right=None, value=None):
        self.type = type
        self.left = left
        self.right = right
        self.value = value