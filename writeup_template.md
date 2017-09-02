#**Behavioral Cloning** 

##Writeup Template

###You can use this file as a template for your writeup if you want to submit it as a markdown file, but feel free to use some other method and submit a pdf if you prefer.

---

**Behavioral Cloning Project**

The goals / steps of this project are the following:
* Use the simulator to collect data of good driving behavior
* Build, a convolution neural network in Keras that predicts steering angles from images
* Train and validate the model with a training and validation set
* Test that the model successfully drives around track one without leaving the road
* Summarize the results with a written report


[//]: # (Image References)

[image1]: ./examples/placeholder.png "Model Visualization"
[image2]: ./examples/center_2017_08_19_09_14_11_010.jpg "Grayscaling"
[image3]: ./examples/center_2017_08_19_10_07_22_844.jpg "Recovery Image"
[image4]: ./examples/center_2017_08_19_10_07_23_130.jpg "Recovery Image"
[image5]: ./examples/center_2017_08_19_10_07_23_267.jpg "Recovery Image"
[image6]: ./examples/original.png "Normal Image"
[image7]: ./examples/flip.png "Flipped Image"

## Rubric Points
###Here I will consider the [rubric points](https://review.udacity.com/#!/rubrics/432/view) individually and describe how I addressed each point in my implementation.  

---
###Files Submitted & Code Quality

####1. Submission includes all required files and can be used to run the simulator in autonomous mode

My project includes the following files:
* h5create.py containing the script to create and train the model
* drive.py for driving the car in autonomous mode
* model.h5 containing a trained convolution neural network 
* writeup_report.md or writeup_report.pdf summarizing the results

####2. Submission includes functional code
Using the Udacity provided simulator and my drive.py file, the car can be driven autonomously around the track by executing 
```sh
python drive.py model.h5
```

####3. Submission code is usable and readable

The h5create.py file contains the code for training and saving the convolution neural network. The file shows the pipeline I used for training and validating the model, and it contains comments to explain how the code works.

###Model Architecture and Training Strategy

####1. An appropriate model architecture has been employed

My model consists of a convolution neural network with 5x5, 3x3 filter sizes  (h5create.py lines 81-90) 

The model includes RELU layers to introduce nonlinearity (code line 81-85), and the data is normalized in the model using a Keras lambda layer (code line 80). 

####2. Attempts to reduce overfitting in the model

The model doesn't contain dropout layers in order to reduce overfitting. 

####3. Model parameter tuning

The model used an adam optimizer, so the learning rate was not tuned manually (h5create.py line 93).

####4. Appropriate training data

Training data was chosen to keep the vehicle driving on the road. I used a combination of center lane driving, recovering from the left and right sides of the road, and driving reserve on track.

###Model Architecture and Training Strategy

####1. Solution Design Approach

My first step was to use a convolution neural network model similar to the NVIDIA Architecture. 

The final step was to run the simulator to see how well the car was driving around track one. To improve the driving behavior, 
I used more images of driving reverse track and side of the track.

At the end of the process, the vehicle is able to drive autonomously around the track without leaving the road.

####2. Final Model Architecture

The final model architecture (h5create.py lines 78-90) consisted of a NVIDIA Architecture with the following layers and layer sizes 

filter | kernel|stride|Description
|:------:|:--------:|:--------:|:--------:| 
24|5x5|2,2|relu
36|5x5|2,2|relu
48|5x5|2,2|relu
64|3x3| |relu
64|3x3| |relu
flatten|||
dense|||100
dense|||50
dense|||10
dense|||1



####3. Creation of the Training Set & Training Process

To capture good driving behavior, I first recorded two laps on track one using center lane driving. Here is an example image of center lane driving:

![alt text][image2]

I then recorded the vehicle recovering from the left side and right sides of the road back to center so that the vehicle would learn to recover position into center. 

![alt text][image3]
![alt text][image4]
![alt text][image5]

Then I repeated this process on track two in order to get more data points.

To augment the data sat, I also flipped images and angles thinking that this would ... For example, here is an image that has then been flipped:

![alt text][image6]
![alt text][image7]

And I used images of driving reverse track.

After the collection process, I had 21,102 number of images and 5,465 data sets . I then preprocessed this data by using generator funtion.


I finally randomly shuffled the data set and put 0.6% of the data into a validation set. 

I used this training data for training the model. The validation set helped determine if the model was over or under fitting. The ideal number of epochs was 32. I used an adam optimizer so that manually training the learning rate wasn't necessary.
