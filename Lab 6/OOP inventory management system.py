
import json
import os

INVENTORY_FILE = "inventory.json"


# Section 2.3 - Product Class
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

    def get_id(self):
        return self.__product_id

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock


# Section 2.6 - Inventory Class
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

    def get_products(self):
        return self.__products.copy()


# File Handling
def load_inventory():
    inventory = Inventory()

    if os.path.exists(INVENTORY_FILE):
        with open(INVENTORY_FILE, "r") as file:
            saved_products = json.load(file)

        for product in saved_products:
            new_product = Product(
                product["id"],
                product["name"],
                product["price"],
                product["stock"]
            )

            inventory.add_product(new_product)

        print("Inventory successfully loaded.")
        return inventory

    else:
        print("No inventory file found.")
        return inventory


def save_inventory(inventory):
    products = []

    for product in inventory.get_products():
        products.append({
            "id": product.get_id(),
            "name": product.get_name(),
            "price": product.get_price(),
            "stock": product.get_stock()
        })

    with open(INVENTORY_FILE, "w") as file:
        json.dump(products, file, indent=4)

    print("Inventory successfully saved.")


# Week 5 Functions - Refactored
def search_product(inventory):
    search_name = input("Enter product name to search: ")

    product = inventory.search_product(search_name)

    if product is not None:
        print("Product found:")
        product.display_information()
        return product

    print("Product not found.")
    return None


def add_product(inventory):
    product_id = input("Enter product ID: ")
    name = input("Enter product name: ")
    price = float(input("Enter product price: "))
    stock = int(input("Enter stock quantity: "))

    product = Product(product_id, name, price, stock)

    inventory.add_product(product)

    print("Product successfully added.")


def update_stock(inventory):
    search_name = input("Enter product name: ")

    product = inventory.search_product(search_name)

    if product is not None:
        new_stock = int(input("Enter new stock quantity: "))
        product.update_stock(new_stock)

        print("Stock successfully updated.")
        return

    print("Product not found.")


def display_all(inventory):
    inventory.display_all()


# Main Program
def main():
    inventory = load_inventory()

    while True:

        print("\n--- Inventory Menu ---")
        print("1. Display All Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Save Inventory")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            display_all(inventory)

        elif choice == "2":
            add_product(inventory)

        elif choice == "3":
            update_stock(inventory)

        elif choice == "4":
            search_product(inventory)

        elif choice == "5":
            save_inventory(inventory)

        elif choice == "6":
            save_inventory(inventory)
            print("Program exited.")
            break

        else:
            print("Invalid option. Please try again.")


main()