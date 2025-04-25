try:
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("Note: Graphing disabled (install matplotlib for charts)")

from datetime import datetime

class ReportGenerator:
    def __init__(self, transactions):
        self.transactions = transactions

    def show_graph(self):
        if not HAS_MATPLOTLIB:
            print("Graphing unavailable - install matplotlib first")
            return
        
        # Group transactions by category and sum amounts
        categories = {}
        for t in self.transactions:
            category = t[2]
            amount = t[1]
            if category in categories:
                categories[category] += amount
            else:
                categories[category] = amount

        # Prepare data for plotting
        labels = list(categories.keys())
        values = list(categories.values())

        # Create a new figure
        plt.figure()
        
        # Create a bar chart (or pie chart)
        plt.bar(labels, values)
        plt.title("Expense Distribution by Category")
        plt.xlabel("Category")
        plt.ylabel("Amount")
        
        # Rotate x-labels for better readability
        plt.xticks(rotation=45)
        
        # Adjust layout
        plt.tight_layout()
        
        # Show the plot
        plt.show()

    def generate_text_report(self, start_date=None, end_date=None):
        report = "\n=== Financial Report ===\n"
        if start_date and end_date:
            report += f"Period: {start_date} to {end_date}\n"
        
        total = sum(t[1] for t in self.transactions)
        report += f"Total transactions: {len(self.transactions)}\n"
        report += f"Net balance: {total:.2f}\n\n"
        
        report += "By Category:\n"
        categories = {}
        for t in self.transactions:
            category = t[2]
            amount = t[1]
            if category in categories:
                categories[category] += amount
            else:
                categories[category] = amount
        
        for category, amount in categories.items():
            report += f"{category}: {amount:.2f}\n"
        
        return report