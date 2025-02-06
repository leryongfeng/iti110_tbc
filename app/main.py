from flask import Flask, flash, request, redirect, jsonify
from PIL import Image
from flask_httpauth import HTTPDigestAuth
from modules import image_util, infer_image, calculate_price

app = Flask(__name__)

app.secret_key = 'your_secret_key_here'
auth = HTTPDigestAuth()

@app.post('/infer_image')
def do_infer_image():
    if 'file' not in request.files:
        flash('No file part')
        return {"error": "Request must contain a file"}, 415

    f = request.files['file']
    pil_image = Image.open(f)
    inferred, results = infer_image.do_object_detection(pil_image)

    serve = image_util.serve_pil_image(inferred)

    return serve

@app.post('/start_transaction')
def start_transaction():
    transaction_number = calculate_price.start_transaction()

    response = {
        "message": transaction_number,
        "status": "success"
    }
    return response

@app.post('/list_items')
def list_items():
    transaction_number = request.form["transaction_number"]
    list = calculate_price.list_items(transaction_number)
    response = {
        "message": list,
        "status": "success"
    }

    return response

@app.post('/calculate_total')
def calculate_total():
    transaction_number = request.form["transaction_number"]
    total = calculate_price.calculate_total(transaction_number)
    response = {
        "message": total,
        "status": "success"
    }
    return response

@app.post('/complete_transaction')
def complete_transaction():
    transaction_number = request.form["transaction_number"]
    total, items = calculate_price.complete_transaction(transaction_number)
    response = {
        "message": f"${total:.2f} received for transaction {transaction_number}",
        "items": items,
        "transaction_number": transaction_number,
        "total": total,
        "status": "success"
    }
    return response

@app.post('/transact_image')
def transact_image():
    if 'file' not in request.files:
        flash('No file part')
        return {"error": "Request must contain a file"}, 415

    f = request.files['file']
    pil_image = Image.open(f)
    inferred_image, bounding_boxes = infer_image.do_object_detection(pil_image)

    transaction_number = request.form["transaction_number"]
    status, message = calculate_price.do_transact_results(bounding_boxes, transaction_number)

    serve = image_util.serve_pil_image(inferred_image)
    response = {
        "message": message,
        "status": ( "success" if (status == 200) else "fail")
    }

    return serve, status, response

@app.post('/calibrate')
def do_calibrate():
    if 'file' not in request.files:
        #flash('No file part')
        #return {"error": "Request must contain a file"}, 415

        calculate_price.do_manual_calibrate(request)
        return 'Manual Calibration done', 200

    f = request.files['file']
    pil_image = Image.open(f)
    inferred, results = infer_image.do_object_detection(pil_image)

    calculate_price.do_calibrate(request, results)

    return 'Calibration done', 200
