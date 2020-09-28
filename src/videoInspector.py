import threading
import cv2
import queue
import asyncio
from scenedetect.detectors import ThresholdDetector

def find_threshold(file_path):
    vidReader = cv2.VideoCapture(file_path)

    success = 1

    while success:
        success, image = vidReader.read()
        