from flask import Flask, request, Response, jsonify, send_file
from flask_cors import CORS, cross_origin
import numpy as np
import cv2
from werkzeug.utils import secure_filename
import os
import io
import base64
from PIL import Image

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

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder, filename))
        if img is not None:
            images.append(img)
    return images

def get_encoded_img(image_path):
    img = Image.open(image_path, mode='r')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    my_encoded_img = base64.encodebytes(img_byte_arr.getvalue()).decode('ascii')
    return my_encoded_img

@app.route("/upload", methods=["POST"])
@cross_origin()
def upload():
    try:
        # get request data
        file_name = secure_filename(request.form.get('file_name'))
        file_extension = request.form.get('file_extension')

        # save raw image
        path = os.getcwd()
        print(path)
        raw_image_directory = os.path.join(path, 'raw_image')
        print(raw_image_directory)
        if not os.path.exists(raw_image_directory):
            os.makedirs(raw_image_directory)
        f = request.files.get('file')
        raw_path = os.path.join(raw_image_directory, file_name)
        print(raw_path)
        f.save(raw_path)

        # process image

        # save result
        final_result_directory = os.path.join(path, 'final_result')
        print(final_result_directory)
        if not os.path.exists(final_result_directory):
            os.makedirs(final_result_directory)
        result_path = os.path.join(final_result_directory, file_name)
        f.save(result_path)
        result_image = get_encoded_img(raw_path)
        return jsonify({
            "result_image": "data:image/" + file_extension + ";base64," + result_image
        })
    except Exception as e:
        print('Exception: ')
        print(e)
        return jsonify({
            'error': str(e)
        })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
