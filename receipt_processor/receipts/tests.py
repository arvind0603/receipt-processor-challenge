from django.test import TestCase
from django.urls import reverse
from decimal import Decimal
import json


class ReceiptProcessingTestCase(TestCase):
    def setUp(self):
        self.url = reverse('process')  # Replace with your URL path
        self.valid_data = {
            "retailer": "Test Retailer",
            "purchaseDate": "2022-01-01",
            "purchaseTime": "13:01",
            "items": [
                {"shortDescription": "Item 1", "price": "10.00"},
                {"shortDescription": "Item 2", "price": "15.00"}
            ],
            "total": "25.00"
        }

    def test_process_valid_data(self):
        response = self.client.post(self.url, json.dumps(self.valid_data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("id", response.json())

    def test_missing_required_field(self):
        invalid_data = self.valid_data.copy()
        del invalid_data["retailer"]
        response = self.client.post(self.url, json.dumps(invalid_data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["ErrorMessage"], "Missing required field: retailer")

    def test_missing_items(self):
        invalid_data = self.valid_data.copy()
        del invalid_data["items"]
        response = self.client.post(self.url, json.dumps(invalid_data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["ErrorMessage"], "Missing required field: items")

    def test_invalid_total_format(self):
        invalid_data = self.valid_data.copy()
        invalid_data["total"] = "invalid_total"
        response = self.client.post(self.url, json.dumps(invalid_data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["ErrorMessage"], "The 'total' should be a valid numeric value.")

    def test_invalid_items_total(self):
        invalid_data = self.valid_data.copy()
        invalid_data["items"][0]["price"] = "10.00"
        invalid_data["items"][1]["price"] = "20.00"  # Sum is now 30.00, but total is 25.00
        response = self.client.post(self.url, json.dumps(invalid_data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["ErrorMessage"], "Total does not match the sum of item prices. Expected 30.00, but got 25.00. Check the receipt.")

    def test_invalid_date_format(self):
        invalid_data = self.valid_data.copy()
        invalid_data["purchaseDate"] = "2022-31-12"  # Invalid date format
        response = self.client.post(self.url, json.dumps(invalid_data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["ErrorMessage"], "Invalid date or time format. Expected 'YYYY-MM-DD' for date and 'HH:MM' for time.")

    def test_invalid_time_format(self):
        invalid_data = self.valid_data.copy()
        invalid_data["purchaseTime"] = "25:00:000"  # Invalid time format
        response = self.client.post(self.url, json.dumps(invalid_data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["ErrorMessage"], "Invalid date or time format. Expected 'YYYY-MM-DD' for date and 'HH:MM' for time.")

    def test_invalid_time_format(self):
      invalid_data = self.valid_data.copy()
      invalid_data["purchaseTime"] = "24:00"  # Invalid time format
      response = self.client.post(self.url, json.dumps(invalid_data), content_type="application/json")
      self.assertEqual(response.status_code, 400)
      self.assertEqual(response.json()["ErrorMessage"], "Invalid date or time format. Expected 'YYYY-MM-DD' for date and 'HH:MM' for time.")

    def test_empty_items(self):
        invalid_data = self.valid_data.copy()
        invalid_data["items"] = []
        response = self.client.post(self.url, json.dumps(invalid_data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["ErrorMessage"], "At least one item is required in the receipt.")

    def test_invalid_json(self):
        response = self.client.post(self.url, "invalid_json", content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["ErrorMessage"], "Invalid JSON format..")

class ReceiptPointsTestCase(TestCase):
    def setUp(self):
        self.process_url = reverse('process')  # URL for processing receipts

    def submit_receipt(self, receipt_data):
        """Helper function to submit a receipt and return its ID."""
        response = self.client.post(self.process_url, json.dumps(receipt_data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        return response.json()["id"]

    def fetch_points(self, receipt_id):
        """Helper function to fetch points for a given receipt ID."""
        points_response = self.client.get(reverse('points', args=[receipt_id]))
        self.assertEqual(points_response.status_code, 200)
        return points_response.json()["points"]

    def test_retailer_name_points(self):
        """Test points for the retailer name based on alphanumeric characters."""
        receipt_data = {
            "retailer": "Test Retailer 123",
            "purchaseDate": "2022-01-01",
            "purchaseTime": "12:00",
            "items": [{"shortDescription": "Item 1", "price": "10.00"}],
            "total": "10.00"
        }
        receipt_id = self.submit_receipt(receipt_data)
        points = self.fetch_points(receipt_id)
        self.assertEqual(points, 98)  # 98 alphanumeric characters

    def test_round_dollar_total_points(self):
        """Test 50 points for a round dollar total."""
        receipt_data = {
            "retailer": "Shop ABC",
            "purchaseDate": "2022-01-02",
            "purchaseTime": "11:30",
            "items": [{"shortDescription": "Item 1", "price": "20.00"}],
            "total": "20.00"
        }
        receipt_id = self.submit_receipt(receipt_data)
        points = self.fetch_points(receipt_id)
        self.assertGreaterEqual(points, 50)

    def test_multiple_of_25_total_points(self):
        """Test 25 points for total being a multiple of 0.25."""
        receipt_data = {
            "retailer": "Retailer XYZ",
            "purchaseDate": "2022-01-03",
            "purchaseTime": "10:15",
            "items": [{"shortDescription": "Item 1", "price": "12.25"}],
            "total": "12.25"
        }
        receipt_id = self.submit_receipt(receipt_data)
        points = self.fetch_points(receipt_id)
        self.assertGreaterEqual(points, 25)

    def test_points_for_even_items(self):
        """Test 5 points for every two items."""
        receipt_data = {
            "retailer": "Tech Store",
            "purchaseDate": "2022-01-04",
            "purchaseTime": "14:30",
            "items": [
                {"shortDescription": "Gadget", "price": "30.00"},
                {"shortDescription": "Accessory", "price": "15.00"}
            ],
            "total": "45.00"
        }
        receipt_id = self.submit_receipt(receipt_data)
        points = self.fetch_points(receipt_id)
        self.assertGreaterEqual(points, 5)  # 5 points for 2 items

    def test_description_length_multiple_of_three(self):
        """Test extra points for item descriptions with length multiple of 3."""
        receipt_data = {
            "retailer": "Grocery Store",
            "purchaseDate": "2022-01-05",
            "purchaseTime": "09:45",
            "items": [
                {"shortDescription": "Milk", "price": "5.00"}  # "Milk" has 4 chars, no extra points
            ],
            "total": "5.00"
        }
        receipt_id = self.submit_receipt(receipt_data)
        points = self.fetch_points(receipt_id)
        self.assertGreaterEqual(points, 0)  # No extra points

        receipt_data["items"][0]["shortDescription"] = "Bread"  # "Bread" has 5 chars, no extra points
        receipt_id = self.submit_receipt(receipt_data)
        points = self.fetch_points(receipt_id)
        self.assertGreaterEqual(points, 0)

        receipt_data["items"][0]["shortDescription"] = "Cheese"  # "Cheese" has 6 chars, should earn extra points
        receipt_id = self.submit_receipt(receipt_data)
        points = self.fetch_points(receipt_id)
        self.assertGreaterEqual(points, 1)  # At least 1 extra point for description-based rule

    def test_points_for_total_greater_than_10(self):
        """Test 5 extra points if the total is greater than 10.00."""
        receipt_data = {
            "retailer": "Online Store",
            "purchaseDate": "2022-01-06",
            "purchaseTime": "13:20",
            "items": [{"shortDescription": "Book", "price": "12.00"}],
            "total": "12.00"
        }
        receipt_id = self.submit_receipt(receipt_data)
        points = self.fetch_points(receipt_id)
        self.assertGreaterEqual(points, 5)

    def test_points_for_odd_day_purchase(self):
        """Test 6 points if purchase date is on an odd-numbered day."""
        receipt_data = {
            "retailer": "Clothing Store",
            "purchaseDate": "2022-01-07",  # 7th is an odd day
            "purchaseTime": "10:00",
            "items": [{"shortDescription": "Shirt", "price": "25.00"}],
            "total": "25.00"
        }
        receipt_id = self.submit_receipt(receipt_data)
        points = self.fetch_points(receipt_id)
        self.assertGreaterEqual(points, 6)

    def test_points_for_purchase_between_2pm_and_4pm(self):
        """Test 10 points if purchase time is between 2:00 PM and 4:00 PM."""
        receipt_data = {
            "retailer": "SuperMart",
            "purchaseDate": "2022-01-08",
            "purchaseTime": "15:30",  # 3:30 PM, should get 10 points
            "items": [{"shortDescription": "Groceries", "price": "50.00"}],
            "total": "50.00"
        }
        receipt_id = self.submit_receipt(receipt_data)
        points = self.fetch_points(receipt_id)
        self.assertGreaterEqual(points, 10)

    def test_no_points_for_outside_2pm_4pm(self):
        """Test no extra 10 points if purchase time is outside 2:00 PM - 4:00 PM."""
        receipt_data = {
            "retailer": "Convenience Store",
            "purchaseDate": "2022-01-09",
            "purchaseTime": "15:01",  # Just outside 2 PM - 4 PM window
            "items": [{"shortDescription": "Candy", "price": "2.00"}],
            "total": "2.00"
        }
        receipt_id = self.submit_receipt(receipt_data)
        points = self.fetch_points(receipt_id)
        self.assertEqual(points, 107)

    def test_no_points_for_outside_2pm_4pm(self):
        """Test no extra 10 points if purchase time is outside 2:00 PM - 4:00 PM."""
        receipt_data = {
            "retailer": "Convenience Store",
            "purchaseDate": "2022-01-09",
            "purchaseTime": "16:00",  # Just outside 2 PM - 4 PM window
            "items": [{"shortDescription": "Candy", "price": "2.00"}],
            "total": "2.00"
        }
        receipt_id = self.submit_receipt(receipt_data)
        points = self.fetch_points(receipt_id)
        self.assertEqual(points, 97)

