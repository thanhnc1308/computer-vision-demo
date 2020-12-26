from flask import Flask, request, Response, jsonify, send_file, current_app, send_from_directory
from flask_cors import CORS, cross_origin
import numpy as np
import cv2
from werkzeug.utils import secure_filename
import os
from os import listdir
from os.path import isfile, join
import io
import base64
from PIL import Image
import image_reader
import time
# import cascade_tab_net
import traceback
import uuid

from craft_pytorch import pipeline as p
from craft_pytorch import crop_words as c
from recognition import craft_recog as recog
from craft_pytorch.CropWords import CVTextPosition2Points as finalPrint

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['UPLOAD_FOLDER'] = ''

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
        # file_name = secure_filename(request.form.get('file_name'))
        file_name = 'te.png'
        file_extension = request.form.get('file_extension')
        # CHANGE FOR WINDOWS
        os.system("sh clean.sh")
        # save raw image
        print("app.py | upload")
        path = os.getcwd()
        raw_image_directory = os.path.join(path, 'raw_image')
        if not os.path.exists(raw_image_directory):
            os.makedirs(raw_image_directory)
        f = request.files.get('file')
        raw_path = os.path.join(raw_image_directory, file_name)
        f.save(raw_path)

        # process image
        p.pipeline()
        c.crop_words()
        recog.craft_recog()
        finalPrint.finalPrint()

        # save result

        final_result_directory = os.path.join(path, 'final_result')
        if not os.path.exists(final_result_directory):
            os.makedirs(final_result_directory)
        result_path = os.path.join(final_result_directory, file_name)

        # return result
        raw_image = image_reader.get_encoded_img(raw_path, file_extension)

        text_region_path = os.path.join(path, 'craft_pytorch/Results/res_te.jpg')
        text_region_image = image_reader.get_encoded_img(text_region_path, 'jpg')

        list_text_box_image = []
        list_text_box_image_path = os.path.join(path, 'craft_pytorch/CropWords')
        onlyfiles = [f for f in listdir(list_text_box_image_path) if isfile(join(list_text_box_image_path, f))]
        for img in onlyfiles:
            ext = str(img).split('.')[-1]
            if ext == 'jpg':
                text_box_image_path = os.path.join(list_text_box_image_path, img)
                text_box_image = image_reader.get_encoded_img(text_box_image_path, 'jpg')
                list_text_box_image.append({
                    "id": uuid.uuid4(),
                    "src": image_reader.get_return_img(text_box_image)
                })

        return jsonify({
            "raw_image": image_reader.get_return_img(raw_image, file_extension),
            "text_region_image": image_reader.get_return_img(text_region_image),
            "list_text_box_image": list_text_box_image
        }), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({
            'error': str(e)
        }), 200

@app.route('/download', methods=['GET', 'POST'])
@cross_origin()
def download(filename="ResultFile.txt"):
    uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, filename=filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
