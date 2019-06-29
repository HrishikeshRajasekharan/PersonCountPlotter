import cv2 as cv
import numpy as np
import json
from datetime import datetime
from elasticsearch import Elasticsearch


confThreshold = 0.43
nmsThreshold = 0.40
inpWidth = 416
inpHeight = 416


classesFile = "coco.names"
classes = None
with open(classesFile,'rt') as f: 
    classes = f.read().rstrip('\n').split('\n')


countA = 0
countB = 0 


modelConf = 'yolov3.cfg'
modelWeights = 'yolov3.weights'


def postprocess(frame, outs):
    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]

    classIDs = []
    confidences = []
    boxes = []    

    for out in outs:
        for detection in out:
            
            scores = detection [5:]
            classID = np.argmax(scores)
            confidence = scores[classID]

            if confidence > confThreshold:
                centerX = int(detection[0] * frameWidth)
                centerY = int(detection[1] * frameHeight)

                width = int(detection[2]* frameWidth)
                height = int(detection[3]*frameHeight)

                left = int(centerX - width/2)
                top = int(centerY - height/2)

                classIDs.append(classID)
                confidences.append(float(confidence))
                boxes.append([left, top, width, height])
                
    indices = cv.dnn.NMSBoxes(boxes, confidences, confThreshold, nmsThreshold)
    for i in indices:
        i = i[0]
        box = boxes[i]
        left = box[0]
        top = box[1]
        width = box[2]
        height = box[3]
        
        takeCount(classIDs[i], confidences[i], left, top, width, height)
    
    
def takeCount(classId, conf, left, top, width, height):
    global countA, countB    
    x = left + width/2    
    
    if classes:
        assert (classId < len(classes)) 
        
    if classes[classId] == 'person':        
        if x <= 1200:
            countA = countA + 1
        if x > 1200:
            countB = countB + 1
            
            
def getOutputsNames(net):
    layersNames = net.getLayerNames()
    return [layersNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]


net = cv.dnn.readNetFromDarknet(modelConf, modelWeights)
net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)


frame = cv.imread('test.jpeg') 
blob = cv.dnn.blobFromImage(frame, 1/255, (inpWidth, inpHeight), [0,0,0], 1, crop = False)
net.setInput(blob)
outs = net.forward(getOutputsNames(net))
postprocess(frame, outs)


x = {
     "countA": countA,
     "countB": countB,
     "ts": datetime.now()
     }

print(x)

es = Elasticsearch(HOST="http://localhost", PORT=9200)
es.index(index="test_index", body=x)




