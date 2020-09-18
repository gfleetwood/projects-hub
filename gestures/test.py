# https://gestoos.com/app/
# https://github.com/automagica/automagica
# https://github.com/kelaberetiv/TagUI https://github.com/tebelorg/RPA-Python

import numpy as np
import cv2
import rpa as r
import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np

r.init(visual_automation = True, chrome_browser = False)

cap = cv2.VideoCapture(0)

# Disable scientific notation for clarity
np.set_printoptions(suppress = True)

# Load the model
model = tensorflow.keras.models.load_model(
    'converted_keras/keras_model.h5',
    compile = True
)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    #cv2.imshow('frame', gray)
    
    # Replace this with the path to your image
    image = frame
    
    data = np.ndarray(shape = (1, 224, 224, 3), dtype = np.float32)

    #resize the image to a 224x224 with the same strategy as in TM2:
    #resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)
    
    #turn the image into a numpy array
    image_array = np.asarray(image)

    # display the resized image
    # image.show()

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # run the inference
    prediction = model.predict(data)
    #print(prediction)

    if prediction.max() <= .5:
        pass
    elif prediction[0].argmax() == 0:
        r.keyboard('k')
    else: 
        r.keyboard("[ctrl]w")
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
