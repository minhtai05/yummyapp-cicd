import unittest
from yummy_app import YummyApp


class TestEasyLevel(unittest.TestCase):
    """Bon ca kiem thu co ban trong de bai."""

    def setUp(self):
        self.app = YummyApp()

    def test_calculate_total_for_single_item(self):
        self.assertEqual(
            self.app.calculate_order_total({"pho": 2}), 100000
        )

    def test_calculate_total_for_multiple_items(self):
        self.assertEqual(
            self.app.calculate_order_total({"pho": 1, "bun": 1}), 95000
        )

    def test_calculate_total_for_empty_cart(self):
        self.assertEqual(self.app.calculate_order_total({}), 0.0)

    def test_calculate_total_with_zero_quantity(self):
        self.assertEqual(self.app.calculate_order_total({"pho": 0}), 0.0)


if __name__ == "__main__":
    unittest.main()
