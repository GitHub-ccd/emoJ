import tensorflow as tf

import keras
from keras.models import Sequential
from keras.models import load_model
from keras.layers import Conv2D, MaxPooling2D, AveragePooling2D
from keras.layers import Dense, Activation, Dropout, Flatten

from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator

import numpy as np
import matplotlib.pyplot as plt

import cv2

#Saving the model
model = load_model('templates/model100.h5', compile=False)
#model.summary()

def emotion_analysis(file):
    # true_image = image.load_img(file) 
    
    img = image.load_img(file, color_mode = "grayscale", target_size=(48, 48))

    x = image.img_to_array(img)
    x = np.expand_dims(x, axis = 0)

    x /= 255

    custom = model.predict(x)
    emotions = custom[0]

    x = np.array(x, 'float32')
    x = x.reshape([48, 48]);

    # plt.gray()
    # plt.imshow(true_image)
    # plt.show()

    objects = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')
    y_pos = np.arange(len(objects))
    
    plt.bar(y_pos, emotions, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('percentage')
    plt.title('emotion')
    
    #plt.show()
    plt.savefig('media/predict/result.png')



# emotion_analysis('../templates/1.jpg')