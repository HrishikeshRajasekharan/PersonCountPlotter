# -*- coding: utf-8 -*-
import cv2 as cv
import numpy as np


confThreshold = 0.43
nmsThreshold = 0.40
inpWidth = 416
inpHeight = 416


classesFile = "coco.names"
classes = None


with open(classesFile,'rt') as f: # rt mode is for reading text
    classes = f.read().rstrip('\n').split('\n')


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
        
        drawPred(classIDs[i], confidences[i], left, top, width, height)


def drawPred(classId, conf, left, top, width, height):
    global countA, countB
    label = '%.2f' % conf
    x = left + width/2
    if classes:
        assert (classId < len(classes))
        label = '%s:%s' % (classes[classId], label)    
    if classes[classId] == 'person':
        cv.rectangle(frame, (left, top), (left+width, top+height), (255, 178, 50), 3)
        cv.putText(frame, label, (left,top), cv.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
        print(label)
        if x <= 1200:
            countA = countA + 1
        if x > 1200:
            countB = countB + 1
    

def getOutputsNames(net):
    layersNames = net.getLayerNames() 
    return [layersNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]


countA = 0
countB = 0 


net = cv.dnn.readNetFromDarknet(modelConf, modelWeights)
net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)


frame = cv.imread('test1.jpeg')

  
blob = cv.dnn.blobFromImage(frame, 1/255, (inpWidth, inpHeight), [0,0,0], 1, crop = False)

net.setInput(blob)
outs = net.forward(getOutputsNames(net))
postprocess(frame, outs)

winName = 'View Count'
cv.namedWindow(winName, cv.WINDOW_NORMAL)
cv.resizeWindow(winName, 1000, 1000)
cv.line(frame,(1200,0),(1200,1000),(255,0,0),5)
cv.imshow(winName, frame)
k = cv.waitKey(0)
if k == 27:
    cv.destroyAllWindows()

print("Aisle A: ",countA)
print("Aisle B: ",countB)
