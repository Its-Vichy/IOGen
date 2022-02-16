"""
HCaptcha ai solver.
Made by https://github.com/its-vichy

Credit to:
    - https://github.com/MaxAndolini/hCaptcha-Images for images datacet.
"""

from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt
from tensorflow import keras
import tensorflow as tf
import pathlib, json

data_dir = pathlib.Path('./img/')
config = json.load(open('./config.json'))

batch_size = config['batch_size']
img_height = config['image_size']  # 128 original hcaptcha size
img_width = config['image_size']

train_data = tf.keras.preprocessing.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="training",
    seed=42,
    image_size=(img_height, img_width),
    batch_size=batch_size,
)

val_data = tf.keras.preprocessing.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="validation",
    seed=42,
    image_size=(img_height, img_width),
    batch_size=batch_size
)

class_names = val_data.class_names

plt.figure(figsize=(10, 10))
for images, labels in train_data.take(1):
    for i in range(3):
        ax = plt.subplot(1, 3, i + 1)
        plt.imshow(images[i].numpy().astype("uint8"))
        plt.title(class_names[labels[i]])
        plt.axis("off")

num_classes = 8

while True:
    model = load_model('data.h5')
    model.compile(optimizer='adam', loss=tf.losses.SparseCategoricalCrossentropy(from_logits=True), metrics=['accuracy'],)
    tensorboard_callback = keras.callbacks.TensorBoard(log_dir="logs",histogram_freq=1, write_images="logs", embeddings_data=train_data)

    model.fit(
        train_data,
        validation_data=val_data,
        epochs=config['epoch'],
        callbacks=[tensorboard_callback]
    )

    model.save('data.h5')
    model.summary()
    print('Dataset updated')