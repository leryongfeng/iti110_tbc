import json
from decimal import Decimal, ROUND_HALF_UP

from app.modules import config_parser
import time

config_file="resource/app.conf"
details_dict, logger = config_parser.get_config(config_file)

# testing
#config_file = "../resource/app.conf"
#details_dict, logger = config_parser.get_config(config_file)

size_calibration = dict()
price_lookup = dict()
transactions = dict()

def do_calibrate(request, inference_results):
    for result in inference_results:
        label = result['label']
        size = int(result['size']) # size in pixel area
        obj = json.loads(request.form[label]) # input object of label
        #val = obj['size'] # size of object in calibration image
        #input_size = int(val)
        conversion_rate = 1 / size
        # update calibration values
        size_calibration[label] = conversion_rate
        price_lookup[label] = float(obj['price'])

    print(size_calibration)
    print(price_lookup)

def do_manual_calibrate(request):
    for key in request.keys():
        price_lookup[key] = float(request.get(key)['price'])
        size_calibration[key] = float(request.get(key)['size'])

def start_transaction():
    transaction_number = round(time.time() * 1000) # use current timestamp in ms as transaction number
    transactions[f"{transaction_number}"] = list()

    return transaction_number

def list_items(transaction_number):
    if transaction_number not in transactions.keys():
        raise ValueError("Transaction number not found")

    return transactions[transaction_number]

def calculate_total(transaction_number):
    item_list = list_items(transaction_number)
    total = 0.0

    for item in item_list:
        item_name = item['item_name']
        item_price = item['item_price']
        total = total + item_price

    return total

def complete_transaction(transaction_number):
    total = calculate_total(transaction_number)

    # do transaction. should return error if no transaction received [Currently simulating]
    logger.info(f"Transaction completed. Total received: {total}")
    return total, transactions.pop(transaction_number)

def round_monetary(value):
    amount = Decimal(value)
    rounded_amount = amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return float(rounded_amount)

# bounding_boxes.append({"bbox": (x1, y1, x2, y2), "label": label_name, "classified_label": class_name, "confidence": conf.item(), "size": (x2 - x1) * (y2 - y1)})
def do_calculate_price(bounding_box):
    item_name = bounding_box['label']
    item_size = bounding_box['size']

    if item_name not in price_lookup.keys() or item_name not in size_calibration.keys():
        return item_name, -1.0, 422

    item_price_conversion = price_lookup[item_name]
    item_size_conversion = size_calibration[item_name]

    item_price = round_monetary(item_price_conversion * item_size_conversion * item_size)

    return item_name, item_price, 200

def do_transact_results(bounding_boxes, transaction_number):
    list_items(transaction_number)

    logger.info(f"Transact for {transaction_number}")
    temp_item_list = list()
    for bounding_box in bounding_boxes:
        classified_label = bounding_box['classified_label']
        if classified_label == "damaged":
            logger.info(f"Stop current transact for {transaction_number}. Damaged items found. Please remove before continuing.")
            return 417, "Damaged items found. Please remove before continuing."

        item_name, item_price, response = do_calculate_price(bounding_box)
        if response != 200:
            return response, "Invalid input. Please try again."

        val = {"item_name": item_name, "item_price": item_price}
        temp_item_list.append(val)
        logger.info(f"Calculated item: {val}")

    logger.info(f"Completed current transact for {transaction_number}.")
    transactions[transaction_number].extend(temp_item_list)

    return 200, "Completed current transact"

if __name__ == "__main__":
    print('something')