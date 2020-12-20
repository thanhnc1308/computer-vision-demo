from flask import Flask, request, Response, jsonify, send_file
from flask_cors import CORS, cross_origin
import numpy as np
import cv2
from werkzeug.utils import secure_filename
import os
import io
import base64
from PIL import Image
import image_reader
import time

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route("/test", methods=["GET"])
@cross_origin()
def get_example():
    response = jsonify(message="Simple server is running")
    return response

@app.route("/upload", methods=["POST"])
@cross_origin()
def upload():
    try:
        # get request data
        file_name = secure_filename(request.form.get('file_name'))
        file_extension = request.form.get('file_extension')

        # save raw image
        path = os.getcwd()
        raw_image_directory = os.path.join(path, 'raw_image')
        if not os.path.exists(raw_image_directory):
            os.makedirs(raw_image_directory)
        f = request.files.get('file')
        raw_path = os.path.join(raw_image_directory, file_name)
        f.save(raw_path)

        # process image

        # save result
        final_result_directory = os.path.join(path, 'final_result')
        if not os.path.exists(final_result_directory):
            os.makedirs(final_result_directory)
        result_path = os.path.join(final_result_directory, file_name)
        f.save(result_path)
        # f.flush()
        # image_reader.wait_for_file(result_path)
        result_image = image_reader.get_encoded_img(result_path, file_extension)
        return jsonify({
            "result_image": "data:image/" + file_extension + ";base64," + result_image
        }), 200
    except Exception as e:
        print('Exception: ' + str(e))
        return jsonify({
            'error': str(e)
        }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
