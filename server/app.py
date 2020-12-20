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
# import cascade_tab_net
import traceback

from craft_pytorch import pipeline as p
from craft_pytorch import crop_words as c
from recognition import craft_recog as recog

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

        # save result

        # final_result_directory = os.path.join(path, 'final_result')
        # if not os.path.exists(final_result_directory):
        #     os.makedirs(final_result_directory)
        # result_path = os.path.join(final_result_directory, file_name)
        # f.save(result_path)
        # raw_path = '/home/thanhnc/ICT/ProductListDemo/server/raw_image/Screenshot_from_2020-12-20_10-01-30.png'
        # cascade_tab_net.show_result(raw_path)
        result_image = image_reader.get_encoded_img(raw_path, file_extension)
        return jsonify({
            "result_image": "data:image/" + file_extension + ";base64," + result_image
        }), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({
            'error': str(e)
        }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
