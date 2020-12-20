# Installation and run

- python3 -m venv .venv
- source .venv/bin/activate //env\Scripts\activate
- pip3 install -r requirements.txt
- flask run
<!-- python -m flask run -->
- FLASK_APP=app.py FLASK_ENV=development flask run

# Library
- pip3 freeze > requirements.txt
- pip3 install flask
- pip3 install flask-cors
- pip3 install opencv-python
- python3 -c "import cv2"
- pip3 install jsonpickle
- pip3 install Pillow

# Install CascadeTabNet
- pip3 install torch==1.4.0+cu100 torchvision==0.5.0+cu100 -f https://download.pytorch.org/whl/torch_stable.html
- pip3 install mmcv terminaltables
- git clone --branch v1.2.0 'https://github.com/open-mmlab/mmdetection.git'
- cd "mmdetection"
- pip3 install -r "./requirements/optional.txt"
- python3 setup.py install
- python3 setup.py develop
- pip3 install -r {"requirements.txt"}
<!-- - pip3 install pillow==6.2.1 -->
- pip3 install mmcv==0.4.3
- git clone https://github.com/DevashishPrasad/CascadeTabNet.git
- download model and copy to folder models
- gdown "https://drive.google.com/u/0/uc?id=1-QieHkR1Q7CXuBu4fp3rYrvDG9j26eFT"
- change directory of file in cascade_tab_net.py
