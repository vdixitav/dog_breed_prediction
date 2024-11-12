# -*- coding: utf-8 -*-
"""Dog breed prediction.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ufxTuq04RD5eW8X8_KRrOoMdxZZMFAY5
"""

# run this cell and select kagge.json file downloaded

from google.colab import files
files.upload()

# install kaggle api client

! pip install -q kaggle

#install api using pip installation

!mkdir -p ~/.kaggle
#
# !chmod 600 ~/.kaggle/kaggle.json

!cp kaggle.json ~/.kaggle/

# Commented out IPython magic to ensure Python compatibility.
# creating directory and changing current working directory

!mkdir dog_dataset
# %cd dog_dataset

# searching for dataset

! kaggle datasets list -s dogbreedidfromcomp

# Commented out IPython magic to ensure Python compatibility.
# downloading dataset and coming out of derectory

!kaggle datasets download catherinehorng/dogbreedidfromcomp
# %cd ..

# unzipping dowloaded file and remove unusale file
!unzip dog_dataset/dogbreedidfromcomp.zip -d dog_dataset
!rm dog_dataset/dogbreedidfromcomp.zip
!rm dog_dataset/sample_submission.csv

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from tqdm import tqdm
from keras.preprocessing import image
from sklearn.preprocessing import label_binarize
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense ,Dropout,Flatten,Conv2D ,MaxPool2D
from keras.optimizers import Adam

labels_all=pd.read_csv("dog_dataset/labels.csv")

labels_all.head()

breeds_all=labels_all['breed']
breeds_counts=breeds_all.value_counts()
breeds_counts.head()

CLASS_NAMES=["scottish_deerhound","maltese_dog","bernese_mountain_dog"]
labels=labels_all[(labels_all['breed'].isin(CLASS_NAMES))]
labels=labels.reset_index()
labels.head()

# read the labels.csv file and checking shape and records

labels_all=pd.read_csv("dog_dataset/labels.csv")
print(labels_all.shape)
labels_all.head()

#visualize the number of each breeds

breeds_all=labels_all['breed']
breeds_counts=breeds_all.value_counts()
breeds_counts.head()

# selecting first 3 breeds
CLASS_NAMES=["scottish_deerhound","maltese_dog","bernese_mountain_dog"]
labels=labels_all[(labels_all['breed'].isin(CLASS_NAMES))]
labels=labels.reset_index()
labels.head()

# creating numpy matrix with zeros

X_data=np.zeros((len(labels),224,224,3) ,dtype='float32')

#one hot encoding
Y_data=label_binarize(labels['breed'], classes= CLASS_NAMES)

# reading and converting image to numpy array and normalizing dataset

for i in tqdm(range(len(labels))):
  img=image.load_img('dog_dataset/train/%s.jpg'% labels['id'][i], target_size=(224,224))
  img=image.img_to_array(img)
  x=np.expand_dims(img.copy(),axis=0)
  X_data[i]= x/255.0

# printing train images and one hot encode shape and size

print("\nTraing Images shape :" , X_data.shape,'size:{:,}' .format(X_data.size))
print("one hot encoded output shape :" , Y_data.shape,'size:{:,}' .format(Y_data.size))

import tensorflow as tf
from tensorflow import keras
from keras import regularizers

# building the model

model=keras.models.Sequential()

model.add(keras.layers.Conv2D(filters=64,kernel_size=(5,5),activation='relu',input_shape=(224,224,3)))
model.add(keras.layers.MaxPool2D(pool_size=(2,2)))

# Corrected line: Using regularizers.l2(0.01) for L2 regularization
model.add(keras.layers.Conv2D(filters=32,kernel_size=(3,3),activation='relu',kernel_regularizer=regularizers.l2(0.01)))
model.add(keras.layers.MaxPool2D(pool_size=(2,2)))

# Corrected line: Using regularizers.l2(0.01) for L2 regularization
model.add(keras.layers.Conv2D(filters=16,kernel_size=(7,7),activation='relu',kernel_regularizer=regularizers.l2(0.01)))
model.add(keras.layers.MaxPool2D(pool_size=(2,2)))

# Corrected line: Using regularizers.l2(0.01) for L2 regularization
model.add(keras.layers.Conv2D(filters=8,kernel_size=(5,5),activation='relu',kernel_regularizer=regularizers.l2(0.01)))
model.add(keras.layers.MaxPool2D(pool_size=(2,2)))


model.add(keras.layers.Flatten())
# Corrected line: Using regularizers.l2(0.01) for L2 regularization
model.add(keras.layers.Dense(128,activation='relu',kernel_regularizer=regularizers.l2(0.01)))
# Corrected line: Using regularizers.l2(0.01) for L2 regularization
model.add(keras.layers.Dense(64,activation='relu',kernel_regularizer=regularizers.l2(0.01)))
model.add(keras.layers.Dense(len(CLASS_NAMES),activation='softmax'))

model.compile(loss='categorical_crossentropy',optimizer=keras.optimizers.Adam(0.0001),metrics=['accuracy'])

model.summary()

# splitting the data set into training and testing data set

X_train_and_val,X_test,Y_train_and_val,Y_test=train_test_split(X_data,Y_data,test_size=0.1)

X_train,X_val,Y_train,Y_val=train_test_split(X_train_and_val,Y_train_and_val,test_size=0.2)

# training the model

epoch=100
batch_size=128
history=model.fit(X_train,Y_train,batch_size=batch_size,epochs=epoch,validation_data=(X_val,Y_val))

# ploting training history


plt.figure(figsize=(12,5))
plt.plot(history.history['accuracy'], color='r')
plt.plot(history.history['val_accuracy'], color='b')
plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epochs')
plt.legend(['train', 'val'])
plt.show()

# predicting usig predict function
# predicting usig predict function
Y_pred=model.predict(X_test)
score=model.evaluate(X_test ,Y_test)
print("Accuracy over the test set: \n ", round((score[1]*100), 2),"%")

# plotting image to compare

plt.imshow(X_test[1,:,:,:])
plt.show()


print("Originally :",labels['breed'][np.argmax(Y_test[1])])
print("Predicted :",labels['breed'][np.argmax(Y_pred[1])])

model.save("dog_breed.h5")

