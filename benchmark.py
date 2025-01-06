#!/usr/bin/env python3

import cv2
import time
import sys

def benchmark(num_times):
    """
    Call face_cascade.detectMultiScale 'num_times' number of times 
    and return the execution time.
    """
    start = time.time()  # Use time.time() instead of time.clock_gettime()
    # Load the cascade
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # Read the input image
    img = cv2.imread('test.jpg')
    if img is None:
        raise FileNotFoundError("The image file 'test.jpg' was not found.")

    # Convert into grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Overhead time just to set things up
    overhead_time = time.time() - start  # Use time.time() here

    start = time.time()  # Use time.time() instead of time.clock_gettime()
    # Detect faces
    for i in range(0, num_times): 
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    face_detect_time = time.time() - start  # Use time.time() here

    return (overhead_time, face_detect_time)

if __name__ == '__main__':
    try:
        if len(sys.argv) < 2:
            print("Usage: python benchmark.py <num_times>")
            sys.exit(1)

        num_times = int(sys.argv[1])
        (overhead_time, face_detect_time) = benchmark(num_times)
        print("overhead_time to load classifier and image -> %f seconds" % overhead_time)
        print("time to do %d face detections -> %f seconds" % (num_times, face_detect_time))

    except Exception as e:
        print("An error occurred:", e)

    # Wait for user input before closing
    input("Press Enter to exit...")