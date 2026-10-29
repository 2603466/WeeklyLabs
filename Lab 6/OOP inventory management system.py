class Product:
    def __init__(self, product_id, name, price, stock):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

    def update_stock(self, quantity):
        self.__stock = quantity

    def display_information(self):
        print(
            "ID:", self.__product_id,
            "| Name:", self.__name,
            "| Price: $", self.__price,
            "| Stock:", self.__stock
        )

    def get_name(self):
        return self.__name

class Inventory:
    def __init__(self):
        self.__products = []

    def add_product(self, product):
        self.__products.append(product)

    def search_product(self, search_name):
        for product in self.__products:
            if product.get_name().lower() == search_name.lower():
                return product

        return None

    def display_all(self):
        if len(self.__products) == 0:
            print("Inventory is empty.")
            return

        print("\n--- Inventory ---")

        for product in self.__products:
            product.display_information()
