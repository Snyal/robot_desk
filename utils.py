from ast import walk
import os
import time
import cv2
import face_recognition
import numpy as np

current_save_image = 0

# --- BOUNDING BOX ---
def faces_encodings(path= "./images/persons"):
    persons = np.array([])
    subfolders = [ f.path for f in os.scandir(path) if f.is_dir() ]

    for folder in subfolders : 

        faces_encodings = []
        for filenames in os.listdir(folder):
            img = os.path.join(folder, filenames)
            face  = face_recognition.load_image_file(img)
            face_enc = face_recognition.face_encodings(face)

            if(len(face_enc)>0):
                faces_encodings.append(face_enc[0])
        
        persons = np.append(persons, {"name": folder.split("/")[-1], "faces_encodings" : faces_encodings})
    
    # save face encoding to a numpy file
    np.save("./assets/faces_encodings", persons, allow_pickle=True)
    return persons

def faces_recognitions(faces_encodings, frame, bounding_box = None):
    # TODO : set known_face_locations with bounding box
    face_enc = face_recognition.face_encodings(frame)

    name = "Unknow"

    if(len(face_enc) > 0):
        unknown_face_encoding = face_enc[0]
        for face_encoding in faces_encodings :
            results = face_recognition.compare_faces(face_encoding["faces_encodings"], unknown_face_encoding)
            for result in results:
                if result:
                    name = face_encoding["name"]
                    break
     
        
    return name

def write_name_over_bounding_box(image, bounding_box, name):
    y = bounding_box[0] - 15 if bounding_box[0] - 15 > 15 else bounding_box[0] + 15
    cv2.putText(image, name, (bounding_box[1], y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 5, cv2.LINE_AA)
    return image

# --- MATHS ---
# angle (degres) to percentage for servo motor
def angle_to_percentage(angle):
    return 2+(angle/18)/2

def get_center_bounding_box(bounding_box):
    #xmin, ymin, xmax, ymax
    corners = bounding_box["boundingBox"]
    
    return  int((corners[1]+corners[3])/2), int((corners[0]+corners[2])/2)


# --- CAMERA ---
def take_picture(robot_s):

    img_name = str(time.time())+".jpg"
    last_img = robot_s.frames[-1]
    cv2.imwrite("/home/bordes/Documents/development/robot_desk/assets/image_for_calibration/"+img_name, last_img)
    print("photo prise")

def init_cam_distortion():
    K = np.load("./assets/calibration_values/k.npy")
    D = np.load("./assets/calibration_values/d.npy")
    DIM = np.load("./assets/calibration_values/dim.npy")

    return K, D, DIM

def undistort(img, K, D, DIM):
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    return undistorted_img
