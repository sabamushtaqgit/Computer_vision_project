import os
import tensorflow as tf
import numpy as np
from tensorflow import keras
from tensorflow.keras.applications import MobileNet
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, BatchNormalization, MaxPooling2D, Dropout, Flatten, Dense
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.utils import to_categorical
from keras.preprocessing import image
from keras.optimizers import Adam
from sklearn.metrics import classification_report
from tensorflow.keras.callbacks import EarlyStopping
from sklearn import metrics

!pip install split-folders

import splitfolders

splitfolders.ratio('/kaggle/input/plantdisease/PlantVillage', output='output', seed=1337, ratio=(0.8, 0.1, 0.1))

# ImageDataGenerator for training data with data augmentation
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=25,
    width_shift_range=0.1,
    height_shift_range=0.1,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

# Validation and test sets
val_datagen = ImageDataGenerator(rescale=1./255)
test_datagen = ImageDataGenerator(rescale=1./255)

dataset_path = r'/kaggle/working/output'
img_size = (256, 256)
batch_size = 32

# Create train_generator
train_generator = train_datagen.flow_from_directory(
    os.path.join(dataset_path, 'train'),
    target_size=img_size,
    batch_size=batch_size,
    class_mode='categorical'
)

val_generator = val_datagen.flow_from_directory(
            os.path.join(dataset_path, 'val'),
            target_size=img_size,
            batch_size=batch_size,
            class_mode='categorical'
        )

# Load MobileNet model without the top (fully connected) layers
base_model = MobileNet(weights='imagenet', include_top=False, input_shape=(256, 256, 3))

# Freeze the weights of the pre-trained layers
for layer in base_model.layers:
    layer.trainable = False

# Create a new model
model = Sequential()
# Add the pre-trained MobileNet base
model.add(base_model)
# Add custom layers on top of the pre-trained base
model.add(Conv2D(32, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Flatten())
model.add(Dense(168, activation='relu'))
model.add(BatchNormalization())
model.add(Dense(15, activation='softmax'))

model.summary()

INIT_LR = 1e-3
lr_schedule = keras.optimizers.schedules.ExponentialDecay( initial_learning_rate=INIT_LR,
                                                          decay_steps=len(train_generator),
                                                           decay_rate=0.9, staircase=True)
optimizer = Adam(learning_rate=lr_schedule)

# Compile the model
model.compile(optimizer= optimizer,
              loss='categorical_crossentropy',
              metrics=['accuracy']) #tf.keras.optimizers.legacy.Adam(learning_rate=0.001  ),

# Train the model
model.fit(train_generator,
          validation_data= val_generator,
          epochs=30,
          verbose = 1)
model.save('Automated_disease_detection.h5')

test_generator = test_datagen.flow_from_directory(
    os.path.join(dataset_path, 'test'),
    target_size=img_size,
    batch_size=batch_size,
    class_mode='categorical'
)
    # Get predictions for the test set
predictions = model.predict_generator(test_generator)

# Convert predicted probabilities to class labels
y_pred = np.argmax(predictions, axis=1)

# Get true labels from the generator
y_true = test_generator.classes

# Get class labels
class_labels = list(test_generator.class_indices.keys())

# Generate a classification report
report = classification_report(y_true, y_pred, target_names=class_labels)

# Print or use the report as needed
print(report)

scores = model.evaluate(test_generator)
print(f"Accuracy: {scores[1]*100}")

model.evaluate(train_generator)
print(f"Accuracy: {scores[1]*100}")
