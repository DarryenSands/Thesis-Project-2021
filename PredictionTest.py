import numpy as np 
import matplotlib.pyplot as plt 
import cv2
import tensorflow as tf
import os, os.path

CATEGORIES = ["Noise", "Signal"]
def prepare(src):
    imgSize = 400
    moddedImage = cv2.imread(src, cv2.IMREAD_UNCHANGED)
    moddedImage = cv2.resize(moddedImage,(imgSize,imgSize))
    print(moddedImage.shape)
    #moddedImage = np.reshape(moddedImage,[1,imgSize,imgSize,3])
    return moddedImage

model = tf.keras.models.load_model("CNN.model")
model.summary()
image = "/home/darryen/Documents/thesis-project-2021/PredictedImages/signal729.png"
resizedImage = prepare(image)
prediction = model.predict([resizedImage])
prediction = list(prediction[0])
print(CATEGORIES[prediction.index(max(prediction))])