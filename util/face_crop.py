#!/usr/bin/env python

# This is a stanalone program that first ensures if "one" face of a person 
# exists in the given image and crops it

import cv2
import os

# DIRECTORY of the images scaraped from web. Can have sub directory for each emotion
directory = "images/"

# directory where the images to be saved. will be seved on relavant sub directory. 
# please make sure to create the sub directory with proper label
f_directory = "done/"
            
def facecrop(image):
    # Crops the face of a person from any image!
	# images with only one face is processed. 

    # OpenCV XML FILE for Frontal Facial Detection using HAAR CASCADES.
    facedata = "haarcascade_frontalface_alt.xml"
    cascade = cv2.CascadeClassifier(facedata)

    # Reading the given Image with OpenCV
    img = cv2.imread(image)
    img=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    

    try:
        ## Some downloaded images are of unsupported type and should be ignored while raising Exception
    
        minisize = (img.shape[1],img.shape[0])
        miniframe = cv2.resize(img, minisize)

        faces = cascade.detectMultiScale(miniframe)
        nFaces = len(faces)
        #print("# of faces", nFaces)

        for f in faces:
            x, y, w, h = [ v for v in f ]
            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

            sub_face = img[y:y+h, x:x+w]

            f_name = image.split('/')
            f_name = f_name[-1]

    except:
        pass
    if nFaces > 0:
        return nFaces, sub_face
    else:
        sub_face = "none" 
        return nFaces, sub_face


if __name__ == '__main__':

	emotions = os.listdir(directory)
	for emo in emotions:
		print("processing files in ", emo)
		files = os.listdir(directory+emo)
		for file in files:
			#print(file)
			img = directory + emo + "/"+ file
			#print(img)
			nFaces, sub_face = facecrop(img)
			if nFaces == 1:
				output = f_directory + emo + "/" + file
				#print("output", output)
				cv2.imwrite(output, sub_face)
				print ("Writing: ", emo, file)
			else:
				#pass
				print(emo, file, " image will be removed" )
