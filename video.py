import cv2
import numpy as np
import tensorflow as tf
import os
import random

IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
SAMPLE_SIZE = 5

def load_data(data_dir):
    all_images = []
    all_labels = []
    
    # Iterate over each directory (label) in the dataset
    for folder in sorted(os.listdir(data_dir), key=int):  # Sorting by integer ensures the class order
        folder_path = os.path.join(data_dir, folder)
        images = []
        labels = []
        
        if os.path.isdir(folder_path):
            # Iterate over each image in the folder
            for filename in os.listdir(folder_path):
                img_path = os.path.join(folder_path, filename)
                img = cv2.imread(img_path)
                img = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT))
                images.append(img)
                labels.append(int(folder))
            
            # Select 5 random images from this class
            selected_samples = random.sample(list(zip(images, labels)), SAMPLE_SIZE)
            for img, lbl in selected_samples:
                all_images.append(img)
                all_labels.append(lbl)
                
    return all_images, all_labels

def main():
    # Load trained model
    model = tf.keras.models.load_model('best_model.h5')
    
    # Load data
    images, labels = load_data('gtsrb')

    for img, label in zip(images, labels):
        # Preprocess image for model prediction
        img_for_pred = np.expand_dims(img, axis=0)
        predicted_label = np.argmax(model.predict(img_for_pred))

        # Write the actual label and the prediction on the image
        if predicted_label == label:
            display = "YES"
            color = (0, 255, 0)
        else:
            display = "NO"
            color = (0, 0, 255)
        
        print(f'\nPredicted: {predicted_label}\nActual: {label}\n')
        cv2.putText(img, display, (5, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

        # Display the image
        cv2.imshow('Traffic Sign Prediction', img)
        cv2.waitKey(1000)  # Display each image for 1 second

    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
