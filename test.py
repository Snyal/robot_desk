import cv2
import tensorflow as tf

from cv.model import run_odt_and_draw_results

cam = cv2.VideoCapture(0)
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

interpreter = tf.lite.Interpreter(model_path="/home/bordes/Documents/development/robot_cam/assets/model.tflite")
interpreter.allocate_tensors()

while(True):
      
    # Capture the video frame
    # by frame
    ret, frame = cam.read()
  
    # Display the resulting frame

    detection_result_image, _ = run_odt_and_draw_results(
        frame,
        None,
        interpreter,
        threshold=0.7
    )

    cv2.imshow('frame', detection_result_image)

    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
# After the loop release the cap object
cam.release()
# Destroy all the windows
cv2.destroyAllWindows()