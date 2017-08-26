import csv
import cv2
import numpy as np
import os
from sklearn.model_selection import train_test_split
import sklearn
import random

lines = []
samples = []
with open('driving_log.csv') as csvfile:
    reader = csv.reader(csvfile)
    for line in reader:
        #lines.append(line)
        samples.append(line)

train_samples, validation_samples = train_test_split(samples, test_size=0.2)

'''images = []
measurements = []
for line in lines:
    for i in range(3):
        source_path = line[i]
        filename = source_path.split('\\')[-1]
        current_path = './IMG/' + filename
        image = cv2.imread(current_path)
        if image is None:
            print("Image path incorrect: ", current_path)
            continue  # skip adding these rows in the for loop
        images.append(image)
        measurement = float(line[3])
        measurements.append(measurement)    '''
    

    
#X_train = np.array(images)
#y_train = np.array(measurements)

#X_train = np.array(augmented_images)
#y_train = np.array(augmented_measurements)


def generator(samples, batch_size=32):
    num_samples = len(samples)
    while 1: # Loop forever so the generator never terminates
        random.shuffle(samples)
        for offset in range(0, num_samples, batch_size):
            batch_samples = samples[offset:offset+batch_size]

            images = []
            angles = []
            for batch_sample in batch_samples:
                name = './IMG/'+batch_sample[0].split('\\')[-1]
                center_image = cv2.imread(name)
                center_angle = float(batch_sample[3])
                images.append(center_image)
                angles.append(center_angle)

                augmented_images, augmented_angles = [], []
                for image, angle in zip(images, angles):
                    augmented_images.append(image)
                    augmented_angles.append(angle)
                    augmented_images.append(cv2.flip(image,1))
                    augmented_angles.append(angle*-1.0)
            # trim image to only see section with road
            X_train = np.array(augmented_images)
            y_train = np.array(augmented_angles)
            yield sklearn.utils.shuffle(X_train, y_train)
            
from keras.models import Sequential
from keras.layers import Flatten, Dense, Lambda, Cropping2D
from keras.layers import Convolution2D
#from keras.layers.pooling import MaxPooling2D
from keras.models import Model
import matplotlib.pyplot as plt



model = Sequential()
model.add(Lambda(lambda x: x / 255.0 - 0.5, input_shape=(160, 320, 3)))
model.add(Cropping2D(cropping=((70,25),(0,0))))
model.add(Convolution2D(24,5,5,subsample=(2,2),activation="relu"))
model.add(Convolution2D(36,5,5,subsample=(2,2),activation="relu"))
model.add(Convolution2D(48,5,5,subsample=(2,2),activation="relu"))
model.add(Convolution2D(64,3,3,activation="relu"))
model.add(Convolution2D(64,3,3,activation="relu"))
model.add(Flatten())
model.add(Dense(100))
model.add(Dense(50))
model.add(Dense(10))
model.add(Dense(1))

model.compile(loss='mse', optimizer='adam')

# compile and train the model using the generator function
train_generator = generator(train_samples, batch_size=32)
validation_generator = generator(validation_samples, batch_size=32)

ch, row, col = 3, 80, 320  # Trimmed image format



#model.fit(X_train, y_train, validation_split=0.2, shuffle=True, nb_epoch=3)
model.fit_generator(train_generator, samples_per_epoch= len(train_samples), 
                    validation_data=validation_generator, 
                    nb_val_samples=len(validation_samples), nb_epoch=3)
model.save('model.h5')

### print the keys contained in the history object
history_object = model.fit_generator(train_generator, samples_per_epoch =
    len(train_samples), validation_data = 
    validation_generator,
    nb_val_samples = len(validation_samples), 
    nb_epoch=5, verbose=1)

print(history_object.history.keys())

### plot the training and validation loss for each epoch
plt.plot(history_object.history['loss'])
plt.plot(history_object.history['val_loss'])
plt.title('model mean squared error loss')
plt.ylabel('mean squared error loss')
plt.xlabel('epoch')
plt.legend(['training set', 'validation set'], loc='upper right')
plt.show()
