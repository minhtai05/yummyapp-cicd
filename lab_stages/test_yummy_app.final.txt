import unittest
from unittest.mock import patch

import gps_service
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


class TestMediumLevel(unittest.TestCase):
    """TC01-TC04: mang va phien ban he dieu hanh."""

    def setUp(self):
        self.app = YummyApp()

    def test_apply_promo_online_valid(self):
        # Ma khoi tao dung thuoc tinh, khong goi HTTP API that.
        with patch.object(self.app, "network_status", "online"):
            self.assertAlmostEqual(
                self.app.apply_promo_code(100000, "GIAM10"), 90000
            )

    def test_apply_promo_offline_raises_connection_error(self):
        with patch.object(self.app, "network_status", "offline"):
            with self.assertRaisesRegex(
                ConnectionError, "Khong co ket noi mang de xac thuc ma"
            ):
                self.app.apply_promo_code(100000, "GIAM10")

    def test_special_promo_os15(self):
        with patch.object(self.app, "os_version", 15):
            self.assertAlmostEqual(
                self.app.apply_promo_code(100000, "NEW_OS_ONLY"), 80000
            )

    def test_special_promo_os14_raises_value_error(self):
        with patch.object(self.app, "os_version", 14):
            with self.assertRaisesRegex(
                ValueError, "Ma nay yeu cau HDH phien ban 15 tro len"
            ):
                self.app.apply_promo_code(100000, "NEW_OS_ONLY")


class TestHardLevel(unittest.TestCase):
    """TC05-TC07: dong the GPS tai namespace duoc ma nghiep vu su dung."""

    def setUp(self):
        self.app = YummyApp()

    @patch("yummy_app.gps_service.get_current_location")
    def test_nearby_restaurants_inside_service_area(self, mock_gps):
        mock_gps.return_value = (10.0, 105.0)
        self.assertEqual(
            self.app.get_nearby_restaurants(),
            ["Nha hang Pho Ly Quoc Su", "Bun cha Huong Lien"],
        )
        mock_gps.assert_called_once_with()

    @patch("yummy_app.gps_service.get_current_location")
    def test_nearby_restaurants_outside_service_area(self, mock_gps):
        mock_gps.return_value = (20.0, 110.0)
        self.assertEqual(self.app.get_nearby_restaurants(), [])
        mock_gps.assert_called_once_with()

    @patch("yummy_app.gps_service.get_current_location")
    def test_nearby_restaurants_when_gps_signal_lost(self, mock_gps):
        mock_gps.side_effect = gps_service.GPSSignalLostError("GPS lost")
        self.assertEqual(
            self.app.get_nearby_restaurants(), "Khong the xac dinh vi tri."
        )
        mock_gps.assert_called_once_with()


class TestAdditionalCases(unittest.TestCase):
    """Bo sung nhanh ma sai va cac bien gio hang chua co trong 7 ca."""

    def setUp(self):
        self.app = YummyApp()

    def test_invalid_promo_code_raises_value_error(self):
        with self.assertRaisesRegex(ValueError, "Ma khuyen mai khong hop le"):
            self.app.apply_promo_code(100000, "KHONG_TON_TAI")

    def test_unknown_item_is_ignored(self):
        self.assertEqual(
            self.app.calculate_order_total({"khong_co": 2, "com": 1}), 30000
        )

    def test_negative_quantity_is_ignored(self):
        self.assertEqual(
            self.app.calculate_order_total({"pho": -1, "bun": 2}), 90000
        )


if __name__ == "__main__":
    unittest.main()
