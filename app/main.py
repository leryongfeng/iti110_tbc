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
    inferred, results = infer_image.do_infer_image(pil_image)

    serve = image_util.serve_pil_image(inferred)

    return serve

@app.post('/calibrate')
def do_calibrate():
    if 'file' not in request.files:
        flash('No file part')
        return {"error": "Request must contain a file"}, 415

    f = request.files['file']
    pil_image = Image.open(f)
    inferred, results = infer_image.do_infer_image(pil_image)

    calculate_price.do_calibrate(request, results)

    return 'Calibration done', 200
