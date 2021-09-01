import numpy as np
import cv2
import requests
from position import position_correction
# def position_correction(detection_Objects,file_name):

#     x_min_sort(detection_Objects)
#     for d_object in detection_Objects:
#         if(float(d_object[5]) > 0):
#             print(d_object[0],end=' ')

#     # with open(file_name+'.txt', 'w') as file:
#     #     for d_object in detection_Objects:
#     #         if(float(d_object[5]) > 0):
#     #             file.write(d_object[0])
# def x_min_sort(detection_Objects):
# for i in range(len(detection_Objects) - 1):
#     for j in range(len(detection_Objects) - i - 1):
#         if(detection_Objects[j][1] > detection_Objects[j+1][1]):
#             detection_Objects[j], detection_Objects[j+1] = detection_Objects[j+1], detection_Objects[j]


def yolov3_detection(image_path):
    confidenceThreshold = 0.5
    NMSThreshold = 0.3
    # modelConfiguration = 'cfg/yolov4-HWC.cfg'
    # modelWeights = 'weight/yolov4-HWC_last.weights'
    # labelsPath = 'data/HWC.names'

    modelConfiguration = 'cfg/yolov4-obj.cfg'
    modelWeights = 'weight/yolov4-obj_15600.weights'
    labelsPath = 'data/HWC.names'

    labels = open(labelsPath).read().strip().split('\n')

    np.random.seed(10)
    COLORS = np.random.randint(0, 255, size=(len(labels), 3), dtype="uint8")

    net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeights)

    #image = cv2.imread('yolov3/images/good.jpeg')
    image = cv2.imread(image_path)
    (H, W) = image.shape[:2]

    # Determine output layer names
    layerName = net.getLayerNames()
    layerName = [layerName[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    blob = cv2.dnn.blobFromImage(
        image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    layersOutputs = net.forward(layerName)

    boxes = []
    confidences = []
    classIDs = []

    for output in layersOutputs:
        for detection in output:
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]
            if confidence > confidenceThreshold:
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY,  width, height) = box.astype('int')
                x = int(centerX - (width/2))
                y = int(centerY - (height/2))

                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)

    # Apply Non Maxima Suppression
    detectionNMS = cv2.dnn.NMSBoxes(
        boxes, confidences, confidenceThreshold, NMSThreshold)

    detection_Objects = []
    if(len(detectionNMS) > 0):
        detection_Objects = []
        file_name = image_path.split('.')[0]
        # with open(file_name+'.txt', 'w') as file:
        for i in detectionNMS.flatten():
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])

            color = [int(c) for c in COLORS[classIDs[i]]]
            cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
            text = '{}: {:.4f}'.format(labels[classIDs[i]], confidences[i])
            cv2.putText(image, text, (x, y - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            # print("{}: {}%".format(
            #     labels[classIDs[i]], confidences[i]*100))
            x_centroid = (x + (x + w))/2
            detection_Objects.append(
                [labels[classIDs[i]], x, y, w, h, x_centroid, confidences[i]*100])
            # sort the list
            # for i in range(len(detection_Objects)-1):
            #     for j in range(len(detection_Objects) - 1):
            #         if(detection_Objects[j][1] > detection_Objects[j+1][1]):
            #             detection_Objects[j], detection_Objects[j+1] = detection_Objects[j+1], detection_Objects[j]
            # for d_object in detection_Objects:
            #     if(float(d_object[2]) > 0):
            #         file.write(d_object[0])
        position_correction(detection_Objects, file_name)
        # print(detection_Objects)

    cv2.imshow('Image', image)
    cv2.waitKey(0)
    return 'ok from yolo_detection_image~'


yolov3_detection('images/S__9388035.jpg')
print(end='\n')
