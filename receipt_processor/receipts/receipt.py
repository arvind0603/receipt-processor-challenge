import math
import re
from datetime import time
from decimal import Decimal


class Receipt:
    def __init__(self, id, retailer, purchase_date, purchase_time, items, total):
        self._id = id 
        self._retailer = retailer
        self._purchase_date = purchase_date
        self._purchase_time = purchase_time
        self._items = items
        self._total = total
        self._points = self.calculate_points()

    def calculate_points(self):
            
        points = 0

        # One point for every alphanumeric character in the retailer name.
        points += len(re.findall("[a-zA-Z0-9]", self._retailer)) 

        #50 points if the total is a round dollar amount with no cents.
        if self._total % 1 == 0: 
            points += 50

        # 25 points if the total is a multiple of 0.25
        if self._total % Decimal('0.25') == 0: 
            points += 25

        # 5 points for every two items on the receipt.
        points += 5 * (len(self._items) // 2) 

        # If the trimmed length of the item description is a multiple of 3, multiply the price by 0.2 and round up to the nearest integer. The result is the number of points earned.
        for item in self._items: 
            if len(item["shortDescription"].strip()) % 3 == 0:  #trim item name
                points += math.ceil(float(item["price"]) * 0.2)

        # 6 points if the day in the purchase date is odd.
        if self._purchase_date.day % 2 == 1:
            points += 6

        # 10 points if the time of purchase is after 2:00pm and before 4:00pm.
        start_time = time(14, 0)  # 14:00 (2:00 PM)
        end_time = time(16, 0)    # 16:00 (4:00 PM)
        if start_time < self._purchase_time < end_time:            
            points += 10
            
        return points