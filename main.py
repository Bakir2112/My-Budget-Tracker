from transaction import Transaction
from database_manager import DatabaseManager
from report_generator import ReportGenerator
import sys
from datetime import datetime

class BudgetApp:
    def __init__(self):
        self.db = DatabaseManager()

    def show_menu(self):
        while True:
            print("\n=== Budget Tracker Menu ===")
            print("1. Add Transaction")
            print("2. View All Transactions")
            print("3. Edit Transaction")
            print("4. Delete Transaction")
            print("5. View Transactions by Category")
            print("6. View Transactions by Date Range")
            print("7. Generate Report")
            print("8. Show Current Balance")
            print("9. Exit")
            
            choice = input("Choose an option: ")
            
            if choice == "1":
                self.add_transaction()
            elif choice == "2":
                self.view_transactions()
            elif choice == "3":
                self.edit_transaction()
            elif choice == "4":
                self.delete_transaction()
            elif choice == "5":
                self.view_transactions_by_category()
            elif choice == "6":
                self.view_transactions_by_date_range()
            elif choice == "7":
                self.generate_report()
            elif choice == "8":
                self.show_balance()
            elif choice == "9":
                print("Goodbye!")
                self.db.close()
                sys.exit()
            else:
                print("Invalid choice. Please try again.")

    def add_transaction(self):
        print("\n=== Add New Transaction ===")
        try:
            amount = float(input("Enter amount (positive for income, negative for expense): "))
            print("Available categories:", ", ".join(self.db.get_categories()))
            category = input("Enter category: ")
            date = input("Enter date (YYYY-MM-DD, leave blank for today): ")
            if not date:
                date = datetime.now().strftime("%Y-%m-%d")
            description = input("Enter description (optional): ")
            
            transaction = Transaction(amount, category, date, description)
            
            if transaction.is_valid():
                transaction_id = self.db.add_transaction(transaction)
                print(f"\nTransaction added successfully! ID: {transaction_id}")
            else:
                print("\nError: Invalid transaction data. Please check amount, category and date.")
        except ValueError:
            print("\nError: Amount must be a number")

    def view_transactions(self, transactions=None):
        if transactions is None:
            transactions = self.db.get_all_transactions()
        
        if not transactions:
            print("\nNo transactions found.")
            return
        
        print("\n=== All Transactions ===")
        print("{:<5} {:<10} {:<15} {:<12} {:<30}".format(
            "ID", "Amount", "Category", "Date", "Description"))
        print("-" * 72)
        for t in transactions:
            print("{:<5} {:<10.2f} {:<15} {:<12} {:<30}".format(
                t[0], t[1], t[2], t[3], t[4] if t[4] else ""))

    def edit_transaction(self):
        self.view_transactions()
        try:
            transaction_id = int(input("\nEnter ID of transaction to edit: "))
            transactions = self.db.get_all_transactions()
            ids = [t[0] for t in transactions]
            
            if transaction_id not in ids:
                print("Invalid transaction ID")
                return
            
            print("\nLeave field blank to keep current value")
            amount = input("Enter new amount: ")
            category = input("Enter new category: ")
            date = input("Enter new date (YYYY-MM-DD): ")
            description = input("Enter new description: ")
            
            # Get current values
            current = next(t for t in transactions if t[0] == transaction_id)
            current_transaction = Transaction(
                current[1], current[2], current[3], current[4])
            
            # Update only changed fields
            if amount:
                current_transaction.update(amount=float(amount))
            if category:
                current_transaction.update(category=category)
            if date:
                current_transaction.update(date=date)
            if description:
                current_transaction.update(description=description)
            
            if current_transaction.is_valid():
                if self.db.update_transaction(transaction_id, current_transaction):
                    print("Transaction updated successfully!")
                else:
                    print("Failed to update transaction")
            else:
                print("Error: Invalid transaction data")
        except ValueError:
            print("Error: Invalid input")

    def delete_transaction(self):
        self.view_transactions()
        try:
            transaction_id = int(input("\nEnter ID of transaction to delete: "))
            if self.db.delete_transaction(transaction_id):
                print("Transaction deleted successfully!")
            else:
                print("Failed to delete transaction (ID not found)")
        except ValueError:
            print("Error: Invalid transaction ID")

    def view_transactions_by_category(self):
        categories = self.db.get_categories()
        if not categories:
            print("No categories found. Add transactions first.")
            return
        
        print("\nAvailable categories:")
        for i, category in enumerate(categories, 1):
            print(f"{i}. {category}")
        
        try:
            choice = int(input("Select category number: "))
            if 1 <= choice <= len(categories):
                selected_category = categories[choice-1]
                transactions = self.db.get_transactions_by_category(selected_category)
                print(f"\n=== Transactions in category: {selected_category} ===")
                self.view_transactions(transactions)
            else:
                print("Invalid category number")
        except ValueError:
            print("Error: Please enter a number")

    def view_transactions_by_date_range(self):
        print("\nEnter date range (YYYY-MM-DD)")
        start_date = input("Start date: ")
        end_date = input("End date: ")
        
        try:
            # Validate dates
            datetime.strptime(start_date, "%Y-%m-%d")
            datetime.strptime(end_date, "%Y-%m-%d")
            
            transactions = self.db.get_transactions_by_date_range(start_date, end_date)
            print(f"\n=== Transactions from {start_date} to {end_date} ===")
            self.view_transactions(transactions)
        except ValueError:
            print("Error: Invalid date format. Use YYYY-MM-DD")

    def generate_report(self):
        transactions = self.db.get_all_transactions()
        if not transactions:
            print("No transactions to generate report")
            return
        
        rg = ReportGenerator(transactions)
        
        print("\n=== Report Options ===")
        print("1. Show graphical report")
        print("2. Show text report")
        print("3. Both")
        
        choice = input("Choose report type: ")
        
        if choice == "1":
            rg.show_graph()
        elif choice == "2":
            print(rg.generate_text_report())
        elif choice == "3":
            print(rg.generate_text_report())
            rg.show_graph()
        else:
            print("Invalid choice")

    def show_balance(self):
        balance = self.db.get_balance()
        if balance >= 0:
            print(f"\nCurrent balance: {balance:.2f} (Positive)")
        else:
            print(f"\nCurrent balance: {balance:.2f} (Negative)")

if __name__ == "__main__":
    app = BudgetApp()
    app.show_menu()