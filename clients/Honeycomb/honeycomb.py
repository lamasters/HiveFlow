import time
import face_detection as fr
import cv2 as cv
import numpy as np
from skimage.metrics import structural_similarity as ssim

cap = cv.VideoSource(0)
in_home = False
_, bg_filter = cap.read()
bg_shape = (0,0)
frame_time = time.time()
bg_time = time.time()

# Generate a unique id for a user
def generate_uid():
    uid = ''
    for i in range(16):
        fig = str(np.random.random() * 10)
        uid = uid + fig
    return uid

# Apply image adjustments for processing
def process_image(frame):
    global bg_shape
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    gray = cv.resize(gray, bg_shape)
    gray = cv.GaussianBlur(gray, (13, 13), 0)
    return gray

# Get an idle image to watch for
def create_filter():
    global bg_filter, bg_shape
    _, frame = cap.read()
    bg_shape = frame.shape
    bg_filter = process_image(frame)
    return 0

# Passively detect movement
def idle(change_count):
    global bg_filter, frame_time
    
    if change_count = 0:
        frame_wait = 1/2
    else:
        frame_wait = 1/30

    if time.time() - frame_time > frame_wait:
        _, frame = cap.read()
        frame = process_image(frame)
        score, diff_map = ssim(frame, bg_filter, full=True)
        if score < 0.75:
            bg_time = time.time()
            return False
        elif time.time() - bg_time > 60:
            create_filter()
            bg_time = time.time()

    return True

# Find faces in video feed
def detect():
    return 0

# Scan a new face
def scan():
    return 0

# Greet existing user
def greet():
    return 0

create_filter()
change_count = 0

while True:
    if in_home:
        continue
    
    if idle(change_count):
        change_count = 0
        continue
    else:
        change_count += 1

    if change_count > 30:
        faces = detect()

        if len(faces) == 0:
            scan()
        else:
            in_home = True
            greet(faces)