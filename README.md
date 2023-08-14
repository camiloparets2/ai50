# Traffic Sign Recognition with Convolutional Neural Networks

## Introduction
In this project, the aim was to develop a model that could identify traffic signs from images. We utilized Convolutional Neural Networks (CNNs) due to their prowess in handling image data. The dataset consists of 43 different classes of traffic signs.

## Model Architecture and Experimentation
### Initial Model:
Our initial model comprised a single convolutional layer followed by max-pooling, and then a dense layer. This basic structure served as a starting point to understand how our data would interact with the network.
#### Further Experimentation:

    Adding More Convolutional Layers: We quickly realized the initial model's limitations. Thus, another convolutional layer was introduced, which helped the model to detect more intricate patterns and improved accuracy.

    Playing with Filters: The number of filters in the convolutional layers was a significant factor. Increasing it from the initial 16 to 32 and then to 64 for the subsequent layer gave our model a broader scope to identify features.

    Introducing Dropout: Overfitting is a typical issue with deep learning models. Introducing a dropout layer after the dense layers helped in regularizing the model. A dropout rate of 0.5 was found optimal in our experiments.

    Optimizers: The initial models utilized the SGD optimizer. However, upon switching to Adam, the convergence was quicker, and the results were better. Adam's adaptive learning rate proved beneficial for our training process.

    Activation Functions: The ReLU activation function was used for the convolutional layers due to its efficiency and ability to handle the vanishing gradient problem.

### Final Model:

The final architecture consists of:

    Two convolutional layers (with 32 and 64 filters respectively).
    Two max-pooling layers following the convolutional layers.
    A dense layer with 128 units.
    Dropout for regularization.
    Output layer with 43 units (for each traffic sign category) using softmax activation.

## Observations:
The CNN model, with the architecture mentioned above, gave satisfactory results. The inclusion of more convolutional layers, experimenting with different optimizers, and introducing dropout significantly impacted the model's performance.

## Future Work:
### For future improvements, we could consider:

    Experimenting with different architectures, like introducing more convolutional layers or increasing the number of filters further.
    Using data augmentation techniques to introduce variability in the training data and further prevent overfitting.
    Fine-tuning with learning rate schedulers or early stopping.

## Conclusion:
This project offered a deep dive into the workings of CNNs for image classification tasks. Through rigorous experimentation and fine-tuning, we achieved a model capable of recognizing traffic signs with commendable accuracy.