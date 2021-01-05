import cv2
import numpy as np
import glob
import random
import os

def yolo_v4():
    # Load Yolo
    modelConfiguration = "yolov4_testing.cfg"
    modelWeights = "yolov4_training_last.weights"
    net = cv2.dnn.readNet(modelConfiguration,modelWeights)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    # Name custom object
    classes = []
    with open("classes.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]
    # Images path
    png_path = glob.glob('raw_image/*.png')
    images_path = list(filter(lambda x: ('te' not in x), png_path))
    print(images_path)

    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    colors = np.random.uniform(0, 255, size=(len(classes), 3))

    # Insert here the path of your images
    #random.shuffle(images_path)
    # loop through all the images
    count = 0
    for img_path in images_path:
        # Loading image
        print(img_path)
        img = cv2.imread(img_path)
        img = cv2.resize(img, None, fx=0.5, fy=0.5)
        height, width, channels = img.shape

        # Detecting objects
        blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

        net.setInput(blob)
        outs = net.forward(output_layers)

        # Showing informations on the screen
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.3:
                    # Object detected
                    print(class_id)
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        #print(indexes)
        font = cv2.FONT_HERSHEY_PLAIN
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                color = colors[class_ids[i]]
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                cv2.putText(img, label, (x, y + 30), font, 3, color, 2)


        # cv2.imshow("Image", img)
        path = os.getcwd()
        yolo_directory = os.path.join(path, 'yolo')
        if not os.path.exists(yolo_directory):
            os.makedirs(yolo_directory)
        print(img)
        cv2.imwrite(os.path.join(yolo_directory, 'yolo_result.png'), img)
        count += 1
        # key = cv2.waitKey(0)

    # cv2.destroyAllWindows()

# yolo_v4()