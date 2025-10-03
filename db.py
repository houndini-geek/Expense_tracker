import sqlite3


def connect_to_db():
    try:
        conn = sqlite3.connect('broke_no_more.db')
        cursor = conn.cursor()
        print("Connected to the database successfully")
        cursor.execute("""
                 CREATE TABLE IF NOT EXISTS expenses (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 type TEXT NOT NULL,
                 amount REAL NOT NULL,
                 category TEXT,
                 description TEXT,
                 expense_date DATE,
                 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                 updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                                    );
                """)
        conn.commit()
        print("Expenses table is ready.")
        # cursor.execute('drop table expenses')
        # conn.commit()

        # # Add some test data | about 10 entries | random Expense and Income data
        # Uncomment the following lines to insert test data into the database.
        # cursor.execute("INSERT INTO expenses (type, amount, category, description, expense_date) VALUES ('Expense', 100.0, 'Food', 'Lunch at restaurant', '2023-10-01')")
        # cursor.execute("INSERT INTO expenses (type, amount, category, description, expense_date) VALUES ('Income', 500.0, 'Salary', 'Monthly salary', '2023-10-01')")
        # cursor.execute("INSERT INTO expenses (type, amount, category, description, expense_date) VALUES ('Expense', 50.0, 'Transport', 'Taxi fare', '2023-10-02')")
        # cursor.execute("INSERT INTO expenses (type, amount, category, description, expense_date   ) VALUES ('Expense', 200.0, 'Entertainment', 'Concert tickets', '2023-10-03')")
        # cursor.execute("INSERT INTO expenses (type, amount, category, description, expense_date               ) VALUES ('Income', 300.0, 'Freelance', 'Freelance project payment', '2023-10-04')")
        # cursor.execute("INSERT INTO expenses (type, amount, category, description, expense_date               ) VALUES ('Expense', 150.0, 'Utilities', 'Electricity bill', '2023-10-05')")
        # cursor.execute("INSERT INTO expenses (type, amount, category, description, expense_date               ) VALUES ('Expense', 80.0, 'Groceries', 'Weekly grocery shopping', '2023-10-06')")
        # cursor.execute("INSERT INTO expenses (type, amount, category, description, expense_date               ) VALUES ('Income', 600.0, 'Investment', 'Dividend from stocks', '2023-10-07')")
        # cursor.execute("INSERT INTO expenses (type, amount, category, description, expense_date               ) VALUES ('Expense', 120.0, 'Health', 'Doctor appointment', '2023-10-08')")
        # cursor.execute("INSERT INTO expenses (type, amount, category, description, expense_date               ) VALUES ('Expense', 90.0, 'Clothing', 'New shoes', '2023-10-09')")
        # conn.commit()
        # print("Test data inserted successfully.")
      
        ##########################################################################################

        return conn
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


