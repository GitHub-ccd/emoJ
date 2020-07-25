# import tensorflow as tf

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


def facecrop(image):  
    """
    Use pretrained HAAR cascade to detect the face and build a bounding box 
    """
    facedata = 'templates/haarcascade_frontalface_alt.xml'
    #facedata = "templates/haarcascade_frontalface_default.xml"
    cascade = cv2.CascadeClassifier(facedata)

    img = cv2.imread(image)

    try:
    
        minisize = (img.shape[1],img.shape[0])
        print(img.shape[1],img.shape[0])
        miniframe = cv2.resize(img, minisize)

        faces = cascade.detectMultiScale(miniframe)

        for f in faces:
            x, y, w, h = [ v for v in f ]
            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

            sub_face = img[y:y+h, x:x+w]

            
            cv2.imwrite('media/predict/crop.jpg', sub_face)
            print("Writing: ", image)
        

    except Exception as e:
        print (e)

    #cv2.imshow(image, img)
    #plt.imshow(img)

def emotion_analysis(file):
    # true_image = image.load_img(file) 
    model = load_model('templates/model100.h5', compile=False)
    #model.summary()

    output = str(file).split(".", 1)[0].replace('images','predict')
    output = output+'_pred.png'

    file = 'media/'+str(file)

    facecrop(file)
    file = 'media/predict/crop.jpg'

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
    # print(emotions)
    #plt.show()

    plt.savefig('media/'+output)
    return output 



# emotion_analysis('../templates/1.jpg')