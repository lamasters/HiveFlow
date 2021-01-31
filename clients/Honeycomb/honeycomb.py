import time
import face_detection as fr
import cv2 as cv
import numpy as np
from skimage.metrics import structural_similarity as ssim

cap = cv.VideoCapture(0)
in_home = False
_, bg_filter = cap.read()
frame_time = time.time()
bg_time = time.time()
detecting = False

known_faces = []
known_names = []
ids = []

# Find face image files and load with associated names
def load_users():
    global known_faces, known_names
    f = open('users.dat', 'r')
    users = f.readlines()
    for user in f.readlines():
        user_id = user.split(',')[0]
        user_name = user.split(',')[1]
        for i in range(5):
            user_face = fr.load_image_file('./' + user_id + '/' + user_id + '_' + str(i) + '.jpg')
            known_faces.append(fr.face_encodings(user_face)[0])
            known_names.append(user_name)

# Generate a unique id for a user
def generate_uid():
    uid = ''
    for i in range(16):
        fig = str(np.random.random() * 10)
        uid = uid + fig
    return uid

# Apply image adjustments for processing
def process_image(frame):
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    gray = cv.resize(gray, (0,0), fx=0.25, fy=0.25))
    gray = cv.GaussianBlur(gray, (13, 13), 0)
    return gray

# Get an idle image to watch for
def create_filter():
    global bg_filter
    _, frame = cap.read()
    bg_filter = process_image(frame)
    return 0

# Passively detect movement
def idle(change_count):
    global bg_filter, bg_time, frame_time
    
    if change_count == 0:
        frame_wait = 1/2
    else:
        frame_wait = 1/30

    if time.time() - frame_time > frame_wait:
        _, frame = cap.read()
        frame = process_image(frame)
        score, diff_map = ssim(frame, bg_filter, full=True)
        if score < 0.8:
            bg_time = time.time()
            return False
        elif time.time() - bg_time > 30:
            create_filter()
            bg_time = time.time()
        frame_time = time.time()

    return True

# Find faces in video feed
def detect():
    global detecting, frame_time
    _, frame_bgr = cap.read()
    frame_bgr = cv.resize(frame_bgr, (0, 0), fx=0.25, fy=0.25)
    frame = frame_bgr[:, :, ::-1]
    name = "Unknown"
    if time.time() - frame_time > 1/10:
        face_loc = fr.face_locations(frame)
        face_enc = fr.face_encodings(frame, face_loc)

        for face in face_enc:
            matches = fr.compare_faces(known_faces, face)

            if True in matches:
                first_match = matches.index(True)
                name = known_faces[first_match]
                detecting = False
    
    return name

# Scan a new face
def scan():
    return 0

# Greet existing user
def greet(name):
    return 0

load_users()

create_filter()
change_count = 0

while True:
    if in_home:
        continue
    
    if not detecting and idle(change_count):
        change_count = 0
        continue
    elif not detecting:
        change_count += 1

    if change_count > 30 and detecting:
        detecting = True
        frame_time = time.time()
        name = detect()
    elif chane_count > 30:
        if name != "Unknown":
            scan()
        else:
            in_home = True
            greet(name)