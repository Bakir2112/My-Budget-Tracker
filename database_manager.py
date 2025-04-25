import sqlite3
from datetime import datetime
from transaction import Transaction

class DatabaseManager:
    def __init__(self, db_name='data/budget.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS transactions
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         amount REAL NOT NULL,
                         category TEXT NOT NULL,
                         date TEXT NOT NULL,
                         description TEXT)''')
        self.conn.commit()

    def add_transaction(self, transaction):
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO transactions 
                          (amount, category, date, description)
                          VALUES (?, ?, ?, ?)''',
                       (transaction.amount, transaction.category, 
                        transaction.date, transaction.description))
        self.conn.commit()
        return cursor.lastrowid

    def get_all_transactions(self):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT id, amount, category, date, description 
                          FROM transactions ORDER BY date DESC''')
        return cursor.fetchall()

    def get_transactions_by_date_range(self, start_date, end_date):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT id, amount, category, date, description 
                          FROM transactions 
                          WHERE date BETWEEN ? AND ?
                          ORDER BY date DESC''',
                       (start_date, end_date))
        return cursor.fetchall()

    def get_transactions_by_category(self, category):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT id, amount, category, date, description 
                          FROM transactions 
                          WHERE category = ?
                          ORDER BY date DESC''',
                       (category,))
        return cursor.fetchall()

    def update_transaction(self, transaction_id, transaction):
        cursor = self.conn.cursor()
        cursor.execute('''UPDATE transactions 
                          SET amount = ?, category = ?, date = ?, description = ?
                          WHERE id = ?''',
                       (transaction.amount, transaction.category, 
                        transaction.date, transaction.description, transaction_id))
        self.conn.commit()
        return cursor.rowcount > 0

    def delete_transaction(self, transaction_id):
        cursor = self.conn.cursor()
        cursor.execute('''DELETE FROM transactions WHERE id = ?''',
                       (transaction_id,))
        self.conn.commit()
        return cursor.rowcount > 0

    def get_categories(self):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT DISTINCT category FROM transactions''')
        return [row[0] for row in cursor.fetchall()]

    def get_balance(self):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT SUM(amount) FROM transactions''')
        result = cursor.fetchone()[0]
        return result if result is not None else 0.0

    def close(self):
        self.conn.close()