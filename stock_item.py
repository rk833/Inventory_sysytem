class StockItem:
    _stock_category = 'Car accessories'

    def __init__(self, stock_code, quantity, price):
        self.__stock_code = stock_code
        self.__quantity = quantity
        self.__price = price


    def get_stock_code(self):
        return self.__stock_code  

    def get_quantity(self):
        return self.__quantity

    def increase_stock(self, amount):
        if amount < 1:
            print("The error was: Increased item must be greater than or equal to one")
        elif self.__quantity + amount > 100:
            print("The error was: Stock cannot exceed 100 units")
        else:
            self.__quantity += amount

    def sell_stock(self, amount):
        if amount < 1:
            print("The error was: Sold amount must be greater than or equal to one")
            return False
        elif amount <= self.__quantity:
            self.__quantity -= amount
            return True
        else:
            return False

    def get_price(self):
        return self.__price

    def set_price(self, price):
        self.__price = price

    def get_stock_name(self):
        return "Unknown Stock Name"

    def get_stock_description(self):
        return "Unknown Stock Description"

    def get_vat(self):
        return 17.5

    def get_price_with_vat(self):
        return self.__price * (1 + self.get_vat() / 100)

    def __str__(self):
        return (f"Stock Category: {self._stock_category}\n"
                f"Stock Type: {self.get_stock_name()}\n"
                f"Description: {self.get_stock_description()}\n"
                f"StockCode: {self.__stock_code}\n"
                f"PriceWithoutVAT: {self.__price:.2f}\n"
                f"PriceWithVAT: {self.get_price_with_vat():.2f}\n"
                f"Total unit in stock: {self.__quantity}")
