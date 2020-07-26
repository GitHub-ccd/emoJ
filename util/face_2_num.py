#!/usr/bin/env python


# # transforming images to a string of numbers
# 
# Objective:
# - convert image to a flatten integers
# - convert list of intergers to a string
# - save string with label and Usage in a .csv file
# - decide the test/train split. (0.7 by default) 
# 
# The .csv file will later be loaded to the refinement of the CNN model based on fer2013

from keras.preprocessing import image

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# directory where the scraped and croped images are located
# There should be 7 sub directories consistant with the emotion names 
# given in the emo_dict dictionary 
directory = "done/"


# load image file and turn to sting of numbers grayscale and 48x48 
def img_2_num(file):
    true_image = image.load_img(file)
    img = image.load_img(file, color_mode = "grayscale" , target_size=(48, 48))
    num = image.img_to_array(img)
    num = num.astype('int').flatten()
    num = num.astype('str').tolist()
    num = " ".join(num)
    return num


if __name__ == '__main__':
	"""
	read the directory and each of the sub directories to identify number of images for each 
	emotion. set the test-train split to appropriate number and label the Usage field
	"""
	#angry-0, disgust-1, fear-2, happy-3, sad-4, surprise-5, neutral-6
	emo_dict = { 'angry': 0, 'disgust': 1, 'fear': 2, 'happy': 3, 'sad': 4, 'surprise': 5, 'neutral' : 6 }
	nEmo_dict = {}
	split = 0.7  # 70% test-train split

	emotions = os.listdir(directory)
	for emo in emotions:
		files = os.listdir(directory+emo)
		n = len(files)
		print(f"{n} files in ({emo_dict[emo]})-{emo} directory")
		# Let's nreate 70:30 train:test split
		nEmo_dict[emo] = round(n * split)
		print(f" training = {nEmo_dict[emo]} and testing = { n - nEmo_dict[emo] } \n")
    

	# Transforming all scraped -> croped -> cleaned imaged to a .csv file

	#create a dataframe
	df = pd.DataFrame(columns = ['emotion', 'pixels', 'Usage'])

	for emo in emotions:
		print(f"processing files in {emo}-({emo_dict[emo]}) directory")
		files = os.listdir(directory+emo)
		i=0
		for file in files:
			f_path = directory + emo + "/"+ file
			#add data 
			if i <= nEmo_dict[emo]:
				data = { 'emotion' : emo_dict[emo], 'pixels' : img_2_num(f_path), 'Usage': 'Training'}
			else:
				data = { 'emotion' : emo_dict[emo], 'pixels' : img_2_num(f_path), 'Usage': 'PublicTest'}
			df = df.append(data, ignore_index=True)
			i+=1
			#print(i)

	#print(df)

	# save the df to a csv file. 
	df.to_csv("FacesInTheWild.csv", index=False)

