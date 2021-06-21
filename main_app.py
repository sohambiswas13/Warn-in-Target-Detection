# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 17:45:43 2021

@author: Soham
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Jun 20 13:55:42 2021

@author: Soham
"""
import pixellib
from pixellib.instance import instance_segmentation
import cv2
import os
import sys
import time
from pygame import mixer  


mixer.init()
mixer.music.load('alarm.wav')

# image segmenation
# taking loaded model from local directory

segment_image = instance_segmentation()
segment_image.load_model("mask_rcnn_coco.h5") 

# setting the target class from the user
print('Choose a target object from the below options :')
target_classes = segment_image.select_target_classes()
for key, value in target_classes.items() :
    print (key)

print('Enter your selected target object:')
target_input = input()
target_classes[target_input] = 'valid'

print("Press 'Y' if you are using any IP/Wifi camera else press 'N' if using default camera:")
camera_input = input()

# main function
def Detect_object(camera_input =  camera_input):
    # taking input from webcam 
    # storing it to directory
    # accesng ip webcam
    
    if camera_input == 'Y':
        print('Enter the IP adress of connected camera like : 192.168.0.235:8080 ')
        url = 'https://'+input()+'/video'  #'https://192.168.0.235:8080/video' 
        videoCaptureObject = cv2.VideoCapture(url)
    else:
        videoCaptureObject = cv2.VideoCapture(0)
        
    # taking the input from choosen camera    
    ret,frame = videoCaptureObject.read()
    

    cv2.imshow('Capturing Video',frame)
    cv2.imwrite('input_image.jpg', frame)
    cv2.waitKey(1)
    videoCaptureObject.release()
    cv2.destroyAllWindows()
    
    
    # passing the input into 
    # segmentation model from directory
    # and checking the ROI inside the output tuple
    output = segment_image.segmentImage('input_image.jpg',segment_target_classes=target_classes, show_bboxes = True )
    output_list = output[0]['rois']
    
    # cheching for presence of the object
    # in input image
    if len(output_list )!= 0:
        print('Found')
        mixer.music.play()
        cv2.imshow('output', output[1])
        cv2.waitKey(2)
        cv2.destroyAllWindows() 
    else :
        print('Not found')
    
    
    # removing the last saved image input from directory
    os.remove('input_image.jpg')



#exit()

# running the function
# every 30 sec delay
def main():    
    t = 0
    while True :
        
        if t%30 == 0 :
            Detect_object(camera_input =  camera_input)
        t = int(time.time()) + 1
    
main()
