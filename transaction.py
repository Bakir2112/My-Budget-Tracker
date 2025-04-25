class Transaction:
    def __init__(self, amount, category, date, description=""):
        self.amount = amount
        self.category = category
        self.date = date
        self.description = description

    def update(self, amount=None, category=None, date=None, description=None):
        if amount is not None:
            self.amount = amount
        if category is not None:
            self.category = category
        if date is not None:
            self.date = date
        if description is not None:
            self.description = description

    def is_valid(self):
        try:
            float(self.amount)
            return (self.amount != "" and 
                    self.category != "" and 
                    self.date != "" and
                    len(self.date.split('-')) == 3)
        except ValueError:
            return False

    def __str__(self):
        return (f"Amount: {self.amount}, Category: {self.category}, "
                f"Date: {self.date}, Description: {self.description}")