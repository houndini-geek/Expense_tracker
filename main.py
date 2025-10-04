from flask import Flask , render_template,  redirect, url_for, request # type: ignore

from rich.traceback import Traceback
from rich.console import Console

console = Console()

from db import connect_to_db
app = Flask(__name__, template_folder="templates")




# Retrieve and display data from the database on the homepage
from typing import Dict, Any

def expense_data() -> Dict[str, Any]:
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
        if conn:
            conn.close()

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


def get_filter( # type: ignore
    filter_type=None, # type: ignore
    sort_type=None, # type: ignore
    amount=None, # type: ignore
    category=None, # type: ignore
    min_amount=None, # type: ignore
    max_amount=None, # type: ignore
    date_=None, # type: ignore
    order_by: str = "date"  # "date" or "amount"
):
    try:
        conn = connect_to_db()
        cursor = conn.cursor() # type: ignore

        # Start query
        query = "SELECT * FROM expenses WHERE 1=1"
        params = []

        # Type filter
        if filter_type is not None and filter_type != "":
            query += " AND LOWER(type) = LOWER(?)"
            params.append(filter_type) # type: ignore

        # Category filter
        if category is not None and category != "":
            query += " AND LOWER(category) = LOWER(?)"
            params.append(category) # type: ignore

        # Exact amount or compare
        if amount is not None and not (min_amount and max_amount):
            if sort_type == 'smaller-than':
                query += " AND amount <= ?"
            elif sort_type == 'greater-than':
                query += " AND amount >= ?"
            else:  # exact
                query += " AND amount = ?"
            params.append(amount) # type: ignore

        # Between range
        if min_amount is not None and max_amount is not None:
            query += " AND amount BETWEEN ? AND ?"
            params.extend([min_amount, max_amount]) # type: ignore

        # Exact date
        if date_ is not None and date_ != "":
            query += " AND expense_date = ?"
            params.append(date_) # type: ignore

        # Sorting
        if order_by == "amount":
            query += " ORDER BY amount DESC"
        else:  # default by date
            query += " ORDER BY expense_date DESC"

        console.print('DEBUG SQL:', query)
        console.print('DEBUG PARAMS:', params)
      
        cursor.execute(query, tuple(params)) # type: ignore
        rows = cursor.fetchall() # type: ignore

        # Parse into dicts
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
        ]

        cursor.close() # type: ignore
        conn.close() # type: ignore

        return {"expenses": expenses} # type: ignore

    except Exception:
        console.print(Traceback(show_locals=True))
        return {"expenses": []} # type: ignore


@app.route('/',methods=['GET']) # type: ignore
def home_page():
    
    filter_type = request.args.get('filter')
    sort_type = request.args.get('sort')
    amount = request.args.get('amount')
    category = request.args.get('category')
    min_amount = request.args.get('min_amount')
    max_amount = request.args.get('max_amount')
    date_ = request.args.get('date')
    
    # Convert to float if not None and not empty
    amount_float = float(amount) if amount not in (None, "") else None
    min_amount_float = float(min_amount) if min_amount not in (None, "") else None
    max_amount_float = float(max_amount) if max_amount not in (None, "") else None

    transactions = None

    if filter_type and sort_type and amount:
        transactions = get_filter( # type: ignore
            filter_type,
            sort_type,
            amount_float,
            category,
            min_amount_float,
            max_amount_float,
            date_
            ) # type: ignore

    data = expense_data()  

    return render_template(
        'index.html',
        expenses=transactions['expenses'] if transactions else data['expenses'],
        categories=data["categories"],
        summary=data["summary"] # type: ignore
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