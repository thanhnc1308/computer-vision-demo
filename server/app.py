from flask import Flask, request, Response, jsonify, send_file
from flask_cors import CORS, cross_origin
import numpy as np
import cv2
from werkzeug.utils import secure_filename
import os

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
        # save raw image
        path = os.getcwd()
        raw_image_directory = path + '/raw_image/'
        if not os.path.exists(raw_image_directory):
            os.makedirs(raw_image_directory)

        f = request.files.get('file')
        f.save(raw_image_directory + secure_filename(f.filename))

        # process image
        # convert string of image data to uint8
        # nparr = np.fromstring(f, np.uint8)
        # decode image
        # img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # save result
        final_result_directory = path + '/final_result/'
        if not os.path.exists(final_result_directory):
            os.makedirs(final_result_directory)
        f.save(final_result_directory + secure_filename(f.filename))
        result_path = os.path.join(final_result_directory,f.filename)
        result_img = cv2.imread(result_path)
        if result_img is not None:
            return send_file(result_img.filename, mimetype='image/png')
        return {
            'message': 'ok'
        }
    except Exception as e:
        print(e)
        return Response(response={'message': 'error'}, status=200, mimetype="application/json")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
