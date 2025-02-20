from decimal import ConversionSyntax, Decimal, InvalidOperation
import json
import uuid
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from receipts.receipt import Receipt
from django.core.exceptions import ObjectDoesNotExist

# In-memory storage
receipts = {}

@csrf_exempt
def process(request):  

    try:
        # Check if the request content type is JSON
        if request.content_type != 'application/json':
            return error_response(error_message="Invalid content type. Expected 'application/json'.", status=400)

        # Parse the request body
        body_data = json.loads(request.body.decode('utf-8'))
        
        # Check for missing required fields in the request body
        required_fields = ['retailer', 'purchaseDate', 'purchaseTime', 'items', 'total']
        for field in required_fields:
            if field not in body_data:
                return error_response(error_message=f"Missing required field: {field}", status=400)
            
        if not body_data.get("items"):
            return error_response(error_message= "At least one item is required in the receipt.", status=400)

        try:
            purchase_date = datetime.strptime(body_data['purchaseDate'], "%Y-%m-%d").date()
            purchase_time = datetime.strptime(body_data['purchaseTime'], "%H:%M").time()
        except ValueError as e:
            raise ValueError("Invalid date or time format. Expected 'YYYY-MM-DD' for date and 'HH:MM' for time.")
        
        item_sum = sum(Decimal(item['price']) for item in body_data['items'])
    
        # Validate if the sum of items matches the total
        if item_sum != Decimal(body_data['total']):
            raise ValueError(f"Total does not match the sum of item prices. Expected {item_sum}, but got {body_data['total']}. Check the receipt.")
        
        body_data = json.loads(request.body)

        receipt_id = str(uuid.uuid4())
        receipt = Receipt(
            id = receipt_id,
            retailer = body_data['retailer'],
            purchase_date = purchase_date,  
            purchase_time = purchase_time,
            items = body_data['items'],
            total = Decimal(body_data['total']).quantize(Decimal('0.01'))
        )
        receipts[receipt._id] = receipt._points
        return JsonResponse({"id": receipt._id}, status=200)
    
    except json.JSONDecodeError:
            return error_response(error_message="Invalid JSON format..", status=400)
    except ValueError as e:
        return error_response(error_message=str(e), status=400)
    except InvalidOperation as e:
            return error_response("The 'total' should be a valid numeric value.", status=400)
    except Exception as e:
        return error_response(error_message=f"An unexpected error occurred: {str(e)}", status=500)

def error_response(error_message=None, status=500):
    return JsonResponse({"ErrorMessage": error_message}, status=status)

def points(req, id):
    try:
        # Try to get the points using the receipt id
        if str(id) in receipts:
            points = receipts[str(id)]
            return JsonResponse({"points": points})
        else:
            raise ObjectDoesNotExist("Receipt not found")
    
    except ObjectDoesNotExist:
        return error_response(error_message="Receipt not found", status=404)
    
    except Exception as e:
        return error_response(error_message=f"An unexpected error occurred: {str(e)}", status=500)
