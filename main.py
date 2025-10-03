from flask import Flask , render_template,  redirect, url_for # type: ignore
# import requests
from db import connect_to_db
app = Flask(__name__, template_folder="templates")






# Retrieve and display data from the database on the homepage
def expense_data(): # type: ignore
    try:
        conn = connect_to_db()
        cursor = conn.cursor() # type: ignore

        # Get all rows
        cursor.execute("SELECT * FROM expenses") # type: ignore
        rows = cursor.fetchall() # type: ignore

        # Parse them into dicts
        expenses = [ # type: ignore
            {
                "id": row[0],
                "type": row[1],
                "amount": row[2],
                "category": row[3],
                "description": row[4],
                "date": row[5]
            }
            for row in rows # type: ignore
        ] # type: ignore

        # Totals
        cursor.execute("SELECT SUM(Amount) FROM expenses WHERE type = 'Income'") # type: ignore
        total_income = cursor.fetchone()[0] or 0 # type: ignore

        cursor.execute("SELECT SUM(Amount) FROM expenses WHERE type = 'Expense'") # type: ignore
        total_expense = cursor.fetchone()[0] or 0 # type: ignore

        balance = total_income - total_expense # type: ignore

        # Unique categories | Remove duplicates by converting to a set
        cat = cursor.execute("SELECT DISTINCT category FROM expenses") # type: ignore
        categories = [row[0] for row in cat.fetchall()] # type: ignore
        

        cursor.close() # type: ignore
        conn.close() # type: ignore

        # Return both in a structured way
        return {
            "expenses": expenses,
            "categories": categories,
            "summary": {
                "total_income": total_income,
                "total_expense": total_expense,
                "balance": balance
            }
        } # type: ignore

    except Exception as e:
        print(f"Failed to show records: {e}")
        return {"expenses": [], "categories": [], "summary": {"total_income": 0, "total_expense": 0, "balance": 0}} # type: ignore




@app.route('/')
def home_page():
    data = expense_data() # type: ignore
    return render_template(
        'index.html',
        expenses=data["expenses"],
        categories=data["categories"],
        summary=data["summary"]
    )



@app.route('/deleteTransaction/<int:id>', methods=['GET'])

def delete_transaction(id): # type: ignore
    try:
        conn = connect_to_db()
        cursor = conn.cursor() # type: ignore
        cursor.execute('DELETE FROM expenses WHERE id = ?',(id,)) # type: ignore
        conn.commit() # type: ignore
        print('Transaction deleted!')
    except:
        pass
    return redirect(url_for('home_page')) # type: ignore
    


if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5555,debug=True)