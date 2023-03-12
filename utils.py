from ast import walk
import os
import cv2
import face_recognition
import numpy as np


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

# angle (degres) to percentage for servo motor
def angle_to_percentage(angle):
    return 2+(angle/18)/2