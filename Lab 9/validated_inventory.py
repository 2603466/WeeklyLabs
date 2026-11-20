import json
import os
import csv
from abc import ABC, abstractmethod

INVENTORY_FILE = "inventory.json"


# Supplier Class
class Supplier:
    def __init__(self, supplier_id, supplier_name, supplier_contact_email):
        self.__supplier_id = supplier_id
        self.__supplier_name = supplier_name
        self.__contact_email = supplier_contact_email

    def display_information(self):
        print(
            "Supplier ID:", self.__supplier_id,
            "| Name:", self.__supplier_name,
            "| Email:", self.__contact_email
        )

    def get_id(self):
        return self.__supplier_id

    def get_name(self):
        return self.__supplier_name

    def get_contact_email(self):
        return self.__contact_email


# Abstract Product Class
class Product(ABC):

    def __init__(self, product_id, name, price, stock, supplier_info: Supplier):
        if price <= 0:
            raise ValueError("Product price must be greater than zero.")

        if stock < 0:
            raise ValueError("Stock quantity cannot be negative.")

def add_product(inventory):
    print("\nSelect Product Type:")
    print("1. Physical Product")
    print("2. Digital Product")

    product_type = input("Enter product type: ")

    if product_type not in ("1", "2"):
        print("Invalid product type.")
        return

    product_id = input("Enter product ID: ")
    name = input("Enter product name: ")
    price = get_positive_float("Enter product price: ")
    stock = get_nonnegative_int("Enter stock quantity: ")

    supplier_id = input("Enter supplier ID: ")
    supplier_name = input("Enter supplier name: ")
    supplier_contact_email = input("Enter supplier contact email: ")
    supplier_info = Supplier(supplier_id, supplier_name, supplier_contact_email)

    if product_type == "1":
        weight = get_nonnegative_float("Enter product weight (kg): ")
        product = ProductFactory.create(
            "physical", product_id, name, price, stock, supplier_info,
            weight=weight
        )

    elif product_type == "2":
        download_size = get_nonnegative_float("Enter download size (MB): ")
        product = ProductFactory.create(
            "digital", product_id, name, price, stock, supplier_info,
            download_size=download_size
        )
    inventory.add_product(product)

    print("Product successfully added.")

def update_stock(inventory):
    search_name = input("Enter product name: ")

    product = inventory.search_product(search_name)

    if product is not None:
        new_stock = get_nonnegative_int("Enter new stock quantity: ")
        product.update_stock(new_stock)

        print("Stock successfully updated.")
        return

    print("Product not found.")


def display_all(inventory):
    inventory.display_all()


def show_product_details(product: Product) -> None:
    product.display_information()
    print(product.get_fulfilment_info())


def demonstrate_polymorphism(inventory: Inventory) -> None:
    for product in inventory.get_products():
        product.display_information()
        print(product.get_fulfilment_info())


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


if __name__ == "__main__":
    main()


    self.__product_id = product_id
    self.__name = name
    self.__price = price
    self.__stock = stock
    self.__supplier: Supplier = supplier_info

    
def update_stock(self, quantity: int) -> None:
    if quantity < 0:
        raise ValueError("Stock quantity cannot be negative.")

    self.__stock = quantity


    def display_information(self):
        print(
            "ID:", self.__product_id,
            "| Name:", self.__name,
            "| Price: $", self.__price,
            "| Stock:", self.__stock
        )
        self.__supplier.display_information()

    def get_name(self):
        return self.__name

    def get_id(self):
        return self.__product_id

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    def get_supplier(self):
        return self.__supplier

    @abstractmethod
    def get_fulfilment_info(self):
        pass


# CanBeShipped Interface
class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self):
        pass


# PhysicalProduct Class
class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id, name, price, stock, weight, supplier_info: Supplier):
        super().__init__(product_id, name, price, stock, supplier_info)
        self.__weight = weight

    def display_information(self):
        super().display_information()
        print("Weight:", self.__weight, "kg")

    def get_fulfilment_info(self):
        return "This product requires physical shipping."

    def calculate_shipping_cost(self):
        return self.__weight * 5

    def get_weight(self):
        return self.__weight


# DigitalProduct Class
class DigitalProduct(Product):
    def __init__(self, product_id, name, price, stock, download_size, supplier_info: Supplier):
        super().__init__(product_id, name, price, stock, supplier_info)
        self.__download_size = download_size

    def display_information(self):
        super().display_information()
        print("Download Size:", self.__download_size, "MB")

    def get_fulfilment_info(self):
        return "This product is delivered digitally."

    def get_download_size(self):
        return self.__download_size

# ProductFactory Class
class ProductFactory:
    @staticmethod
    def create(product_type: str, product_id: str, name: str,
               price: float, stock_quantity: int, supplier: Supplier,
               weight: float = 0.0, download_size: float = 0.0) -> Product:

        if product_type == "physical":
            return PhysicalProduct(
                product_id, name, price, stock_quantity, weight, supplier
            )

        elif product_type == "digital":
            return DigitalProduct(
                product_id, name, price, stock_quantity, download_size, supplier
            )

        else:
            raise ValueError(f"Unknown product type: {product_type}")

# Inventory Class
class Inventory:
    def __init__(self):
        self.__products: list[Product] = []

    def add_product(self, product: Product) -> None:
        self.__products.append(product)

    def find_product(self, product_id: str) -> Product | None:
        for product in self.__products:
            if product.get_id().lower() == product_id.lower():
                return product

        return None

    def remove_product(self, product_id: str) -> None:
        product = self.find_product(product_id)

        if product is not None:
            self.__products.remove(product)

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

# OrderLine Class
class OrderLine:
    def __init__(self, product: Product, quantity: int):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")

        self.product: Product = product
        self.quantity: int = quantity

    def calculate_subtotal(self) -> float:
        return self.product.get_price() * self.quantity

# Discount Strategy
class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, total: float) -> float:
        pass


# No Discount
class NoDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        return total


# Percentage Discount
class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage: float):
        self.percentage = percentage

    def apply(self, total: float) -> float:
        return total * (1 - self.percentage / 100)


# Bulk Discount
class BulkDiscount(DiscountStrategy):
    def __init__(self, threshold: float, amount: float):
        self.threshold = threshold
        self.amount = amount

    def apply(self, total: float) -> float:
        if total >= self.threshold:
            return total - self.amount

        return total

# Student Discount
class StudentDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        return total * 0.95

# Order Class
class Order:
    def __init__(self, order_id: str, discount: DiscountStrategy = None):
        self.order_id: str = order_id
        self.__order_lines: list[OrderLine] = []

        if discount is None:
            self.discount = NoDiscount()
        else:
            self.discount = discount

    def add_order_line(self, product: Product, quantity: int) -> None:
        order_line = OrderLine(product, quantity)
        self.__order_lines.append(order_line)

    def calculate_total(self) -> float:
        total = 0.0

        for order_line in self.__order_lines:
            total += order_line.calculate_subtotal()

        return self.discount.apply(total)

    def set_discount(self, discount: DiscountStrategy) -> None:
        self.discount = discount

    def remove_order_line(self, product_id: str) -> None:
        for order_line in self.__order_lines:
            if order_line.product.get_id() == product_id:
                self.__order_lines.remove(order_line)
                return

    def get_order_lines(self) -> list[OrderLine]:
        return self.__order_lines.copy()

    def remove_order_line(self, product_id: str) -> None:
        for order_line in self.__order_lines:
            if order_line.product.get_id() == product_id:
                self.__order_lines.remove(order_line)
                return

    def get_order_lines(self) -> list[OrderLine]:
        return self.__order_lines.copy()


# File Handling
def load_inventory():
    inventory = Inventory()

    if os.path.exists(INVENTORY_FILE):
        with open(INVENTORY_FILE, "r") as file:
            saved_products = json.load(file)

        for product in saved_products:
            product_type = product.get("type", "physical")
            supplier_data = product.get("supplier") or {}
            supplier_info = Supplier(
                supplier_data.get("supplier_id", "Unknown"),
                supplier_data.get("name", "Unknown"),
                supplier_data.get("contact_email", "Unknown")
            )

            
            if product_type == "physical":
                new_product = ProductFactory.create(
                    "physical",
                    product["id"],
                    product["name"],
                    product["price"],
                    product["stock"],
                    supplier_info,
                    weight=product.get("weight", 0.0)
                )

                if "type" not in product:
                    print("Legacy product loaded with default weight:", product["name"])

            elif product_type == "digital":
                new_product = ProductFactory.create(
                    "digital",
                    product["id"],
                    product["name"],
                    product["price"],
                    product["stock"],
                    supplier_info,
                    download_size=product["download_size"]
                )

            else:
                print("Unknown product type:", product_type)
                continue

            inventory.add_product(new_product)

        print("Inventory successfully loaded.")
        return inventory

    else:
        print("No inventory file found.")
        return inventory


# Section 5.2 - CSV Loading
def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    loaded = 0

    try:
        file = open(path, newline="")

    except FileNotFoundError:
        print(f"Products file not found: {path}")

    else:
        with file:
            reader = csv.reader(file)
            next(reader, None)

            for row_number, row in enumerate(reader, start=2):
                try:
                    if len(row) != 5:
                        raise ValueError("Invalid number of columns.")

                    product_type = row[0].strip().lower()
                    product_id = row[1].strip()
                    name = row[2].strip()
                    price = float(row[3])
                    stock = int(row[4])

                    product = ProductFactory.create(
                        product_type,
                        product_id,
                        name,
                        price,
                        stock,
                        supplier
                    )

                    inventory.add_product(product)
                    loaded += 1

                except ValueError as error:
                    print(f"Skipping row {row_number}: {error}")

        print(f"{loaded} products loaded.")

    finally:
        print("Load attempt finished.")


def save_inventory(inventory):
    products = []

    for product in inventory.get_products():
        supplier = product.get_supplier()
        product_data = {
            "id": product.get_id(),
            "name": product.get_name(),
            "price": product.get_price(),
            "stock": product.get_stock(),
            "supplier": {
                "supplier_id": supplier.get_id(),
                "name": supplier.get_name(),
                "contact_email": supplier.get_contact_email()
            }
        }

        if isinstance(product, PhysicalProduct):
            product_data["type"] = "physical"
            product_data["weight"] = product.get_weight()

        elif isinstance(product, DigitalProduct):
            product_data["type"] = "digital"
            product_data["download_size"] = product.get_download_size()

        products.append(product_data)

    with open(INVENTORY_FILE, "w") as file:
        json.dump(products, file, indent=4)

    print("Inventory successfully saved.")


# User Interaction Functions
def search_product(inventory):
    search_name = input("Enter product name to search: ")

    product = inventory.search_product(search_name)

    if product is not None:
        print("Product found:")
        product.display_information()
        return product

    print("Product not found.")
    return None


# User Input Validation
def get_positive_float(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))

            if value <= 0:
                print("Please enter a number greater than zero.")
                continue

            return value

        except ValueError:
            print("Please enter a valid number, e.g. 12.50")


def get_nonnegative_int(prompt: str) -> int:
    while True:
        try:
            value = int(input(prompt))

            if value < 0:
                print("Stock quantity cannot be negative.")
                continue

            return value

        except ValueError:
            print("Please enter a valid whole number.")


def get_nonnegative_float(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))

            if value < 0:
                print("Please enter a number that is zero or greater.")
                continue

            return value

        except ValueError:
            print("Please enter a valid number.")

def add_product(inventory):
    print("\nSelect Product Type:")
    print("1. Physical Product")
    print("2. Digital Product")

    product_type = input("Enter product type: ")

    if product_type not in ("1", "2"):
        print("Invalid product type.")
        return

    product_id = input("Enter product ID: ")
    name = input("Enter product name: ")
    price = get_positive_float("Enter product price: ")
    stock = get_nonnegative_int("Enter stock quantity: ")

    supplier_id = input("Enter supplier ID: ")
    supplier_name = input("Enter supplier name: ")
    supplier_contact_email = input("Enter supplier contact email: ")
    supplier_info = Supplier(supplier_id, supplier_name, supplier_contact_email)

    if product_type == "1":
        weight = get_nonnegative_float("Enter product weight (kg): ")
        product = ProductFactory.create(
            "physical", product_id, name, price, stock, supplier_info,
            weight=weight
        )

    elif product_type == "2":
        download_size = get_nonnegative_float("Enter download size (MB): ")
        product = ProductFactory.create(
            "digital", product_id, name, price, stock, supplier_info,
            download_size=download_size
        )
    inventory.add_product(product)

    print("Product successfully added.")

def update_stock(inventory):
    search_name = input("Enter product name: ")

    product = inventory.search_product(search_name)

    if product is not None:
        new_stock = get_nonnegative_int("Enter new stock quantity: ")
        product.update_stock(new_stock)

        print("Stock successfully updated.")
        return

    print("Product not found.")


def display_all(inventory):
    inventory.display_all()


def show_product_details(product: Product) -> None:
    product.display_information()
    print(product.get_fulfilment_info())


def demonstrate_polymorphism(inventory: Inventory) -> None:
    for product in inventory.get_products():
        product.display_information()
        print(product.get_fulfilment_info())


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


if __name__ == "__main__":
    main()
