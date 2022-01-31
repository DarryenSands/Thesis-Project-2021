import tensorflow as tf 
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
import pickle
from keras.models import model_from_json
from keras.models import load_model
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.optimizers import SGD


X = pickle.load(open("X.pickle", "rb"))
y = pickle.load(open("y.pickle", "rb"))

X = X/255.0 # Normalizes our data from 0 to 1

'''
print(X.shape)
print(X.shape[1])
print(X.shape[1:])
print(X[0])
print(y)
'''

X_train, X_test, y_train, y_test = train_test_split(X,y, test_size= 0.1)
'''
print(f"X_train: {X_train}")
print(f"X_test: {X_test}")
print(f"y_train: {y_train}")
print(f"y_test: {y_test}")
'''

print(f"Number of training samples: {len(X_train)}, {len(y_train)} ")
print(f"Number of testing samples: {len(X_test)}, {len(y_test)} ")




epoch = 10
batchSize = 8
opt = SGD(lr=0.001)

# building the actual model 
model = Sequential()

# 3 Convolutional layers 
model.add(Conv2D(128, (2, 2), input_shape = X_train.shape[1:]))
model.add(Activation('sigmoid'))
model.add(MaxPooling2D(pool_size= (2,2)))

model.add(Conv2D(256, (2, 2)))
model.add(Activation("sigmoid"))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Conv2D(256, (2, 2)))
model.add(Activation("sigmoid"))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.25))

model.add(Conv2D(256, (2,2)))
model.add(Activation('sigmoid'))
model.add(MaxPooling2D(pool_size=(2,2)))
#model.add(Dropout(0.25))

model.add(Conv2D(256, (2,2)))
model.add(Activation('sigmoid'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(502))
model.add(Activation("relu"))

model.add(Dense(502))
model.add(Activation("relu"))

model.add(Dense(1))
model.add(Activation("softmax"))

model.summary()

model.compile(loss="binary_crossentropy",
				optimizer=opt,
				metrics=["accuracy"])

history = model.fit(X_train, y_train, batch_size=batchSize, epochs=epoch, validation_data = (X_test, y_test))

model_json = model.to_json()
with open("model.json", "w") as json_file :
	json_file.write(model_json)

model.save_weights("model.h5")
print("Saved model to disk")

model.save('CNN.model')

# Printing a graph showing the accuracy changes during the training phase
print(history.history.keys())
plt.figure(1)
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='upper left')
plt.show()


test_loss, test_acc = model.evaluate(X_test, y_test, verbose = 2)
print(test_acc)
