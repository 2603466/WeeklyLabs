import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import inventory_debugged as app


class Lab9Tests(unittest.TestCase):
    def setUp(self):
        self.supplier = app.Supplier("SP001", "Ryan", "Ryan@gmail.com")

    def make_product(self, price=250.0, stock=10):
        return app.ProductFactory.create(
            "physical", "P001", "Desk", price, stock,
            self.supplier, weight=2.5
        )

    # Strategy pattern
    def test_discount_strategies(self):
        self.assertEqual(app.NoDiscount().apply(250), 250)
        self.assertAlmostEqual(app.PercentageDiscount(10).apply(250), 225)
        self.assertAlmostEqual(app.BulkDiscount(200, 20).apply(250), 230)
        self.assertAlmostEqual(app.BulkDiscount(300, 20).apply(250), 250)
        self.assertAlmostEqual(app.StudentDiscount().apply(250), 237.5)

    def test_order_uses_and_changes_discount(self):
        order = app.Order("O001", app.BulkDiscount(200, 20))
        order.add_order_line(self.make_product(), 1)
        self.assertAlmostEqual(order.calculate_total(), 230)

        order.set_discount(app.PercentageDiscount(10))
        self.assertAlmostEqual(order.calculate_total(), 225)

        order.set_discount(app.NoDiscount())
        self.assertAlmostEqual(order.calculate_total(), 250)

    def test_new_strategy_without_changing_order(self):
        class FixedSevenOff(app.DiscountStrategy):
            def apply(self, total: float) -> float:
                return total - 7

        order = app.Order("O002", FixedSevenOff())
        order.add_order_line(self.make_product(), 1)
        self.assertAlmostEqual(order.calculate_total(), 243)

    # Factory pattern
    def test_factory_creates_physical_product(self):
        product = self.make_product()
        self.assertIsInstance(product, app.PhysicalProduct)
        self.assertEqual(product.get_id(), "P001")
        self.assertIs(product.get_supplier(), self.supplier)

    def test_factory_creates_digital_product(self):
        product = app.ProductFactory.create(
            "digital", "D001", "Photo Editor", 49.90, 100,
            self.supplier, download_size=500
        )
        self.assertIsInstance(product, app.DigitalProduct)
        self.assertEqual(product.get_download_size(), 500)

    def test_factory_rejects_unknown_type(self):
        with self.assertRaisesRegex(ValueError, "Unknown product type"):
            app.ProductFactory.create(
                "service", "S001", "Installation", 30.0, 5,
                self.supplier
            )

    # Validation
    def test_rejects_invalid_prices(self):
        for price in (0, -10):
            with self.subTest(price=price):
                with self.assertRaises(ValueError):
                    self.make_product(price=price)

    def test_rejects_negative_initial_stock(self):
        with self.assertRaises(ValueError):
            self.make_product(stock=-1)

    def test_rejects_negative_stock_update(self):
        product = self.make_product()
        with self.assertRaises(ValueError):
            product.update_stock(-1)
        self.assertEqual(product.get_stock(), 10)

    def test_rejects_invalid_orderline_quantity(self):
        product = self.make_product()
        for quantity in (0, -2):
            with self.subTest(quantity=quantity):
                with self.assertRaises(ValueError):
                    app.OrderLine(product, quantity)

    # User input and exception handling
    def test_price_input_retries_until_valid(self):
        output = io.StringIO()
        with patch("builtins.input", side_effect=["abc", "-5", "12.50"]):
            with redirect_stdout(output):
                price = app.get_positive_float("Enter product price: ")
        self.assertEqual(price, 12.5)
        self.assertIn("Please enter a valid number", output.getvalue())
        self.assertIn("Please enter a number greater than zero", output.getvalue())

    def test_csv_loads_valid_rows_and_skips_invalid_rows(self):
        csv_data = (
            "product_type,product_id,name,price,stock_quantity\n"
            "physical,P001,Desk Lamp,25.00,10\n"
            "digital,D001,Photo Editor,49.90,100\n"
            "service,S001,Installation,30.00,5\n"
            "physical,P002,Office Chair,abc,3\n"
            "physical,P003,Monitor Stand,39.50,7\n"
        )
        with tempfile.TemporaryDirectory() as folder:
            csv_path = Path(folder) / "products.csv"
            csv_path.write_text(csv_data, encoding="utf-8")
            inventory = app.Inventory()
            output = io.StringIO()
            with redirect_stdout(output):
                app.load_products(str(csv_path), inventory, self.supplier)

        self.assertEqual(len(inventory.get_products()), 3)
        self.assertIsNotNone(inventory.find_product("P001"))
        self.assertIsNotNone(inventory.find_product("D001"))
        self.assertIsNotNone(inventory.find_product("P003"))
        self.assertIsNone(inventory.find_product("S001"))
        self.assertIn("Skipping row 4", output.getvalue())
        self.assertIn("Skipping row 5", output.getvalue())
        self.assertIn("3 products loaded.", output.getvalue())
        self.assertIn("Load attempt finished.", output.getvalue())

    def test_csv_missing_file_is_handled(self):
        with tempfile.TemporaryDirectory() as folder:
            missing = str(Path(folder) / "missing.csv")
            inventory = app.Inventory()
            output = io.StringIO()
            with redirect_stdout(output):
                app.load_products(missing, inventory, self.supplier)

        self.assertEqual(len(inventory.get_products()), 0)
        self.assertIn("Products file not found:", output.getvalue())
        self.assertIn("Load attempt finished.", output.getvalue())

    # Polymorphism / previous functionality
    def test_both_product_types_work_in_inventory(self):
        inventory = app.Inventory()
        physical = self.make_product()
        digital = app.ProductFactory.create(
            "digital", "D001", "Photo Editor", 49.90, 100,
            self.supplier, download_size=500
        )
        inventory.add_product(physical)
        inventory.add_product(digital)
        self.assertIs(inventory.find_product("P001"), physical)
        self.assertIs(inventory.find_product("D001"), digital)
        self.assertIn("shipping", physical.get_fulfilment_info())
        self.assertIn("digitally", digital.get_fulfilment_info())


if __name__ == "__main__":
    unittest.main()
