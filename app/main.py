from flask import Flask, flash, request, redirect, jsonify
from PIL import Image
from flask_httpauth import HTTPDigestAuth
from modules import image_util, infer_image, calculate_price
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow all origins

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

@app.route('/start_transaction', methods=['POST'])
def start_transaction():
    try:
        transaction_number = calculate_price.start_transaction()

        return jsonify({
            "transaction_number": transaction_number,
            "items": [],
            "total": 0.00,
            "status": "success"
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.post('/get_transaction')
def get_transaction():
    try:
        data = request.get_json()  # Fix: Ensure we parse JSON
        transaction_number = data.get("transaction_number")

        if not transaction_number:
            return jsonify({"error": "Missing transaction_number"}), 400

        items = calculate_price.list_items(transaction_number)
        total = calculate_price.calculate_total(transaction_number)

        return jsonify({
            "items": items,
            "transaction_number": transaction_number,
            "total": total,
            "status": "success"
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/complete_transaction', methods=['POST'])
def complete_transaction():
    try:
        data = request.get_json()  # Fix: Ensure we parse JSON
        transaction_number = data.get("transaction_number")

        if not transaction_number:
            return jsonify({"error": "Missing transaction_number"}), 400

        total, items = calculate_price.complete_transaction(transaction_number)

        return jsonify({
            "message": f"${total:.2f} received for transaction {transaction_number}",
            "items": items,
            "transaction_number": transaction_number,
            "total": total,
            "status": "success"
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/transact_image', methods=['POST'])
def transact_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image file found"}), 400

    file = request.files['image']
    if not file:
        return jsonify({"error": "Missing file"}), 400

    try:
        transaction_number = request.form.get("transaction_number")  # Use `form.get()` for FormData
        if not transaction_number:
            return jsonify({"error": "Missing transaction_number"}), 400

        pil_image = Image.open(file)
        inferred_image, bounding_boxes = infer_image.do_object_detection(pil_image)

        status, message = calculate_price.do_transact_results(bounding_boxes, transaction_number)

        serve = image_util.serve_pil_image(inferred_image)

        # Process image and transaction_number...
        return serve
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/calibrate', methods=['POST'])
def do_calibrate():
    try:
        if 'image' not in request.files:
            # No image file, so we assume it's a manual calibration
            calculate_price.do_manual_calibrate(request)
            return jsonify({"message": "Manual Calibration done"}), 200

        # Process image-based calibration
        f = request.files['image']
        pil_image = Image.open(f)

        # Perform object detection
        inferred_image, bounding_boxes = infer_image.do_object_detection(pil_image)

        # Call existing calibration function
        calculate_price.do_calibrate(request, bounding_boxes)

        serve = image_util.serve_pil_image(inferred_image)

        return serve
    except Exception as e:
        return jsonify({"error": str(e)}), 400
