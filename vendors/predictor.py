from tensorflow import keras
from PIL import Image

import numpy as np
import cv2
import matplotlib.pyplot as plt

from vendors.graphic import getH, getS, getV

UPLOAD_FOLDER = '/home/leber/PycharmProjects/soil_care_api/uploads'

soil_types = [
    'Gravel',
    'Sand',
    'Silt'
]


def present_soil_type_prediction(predictions):
    highest_index = 0

    predictions = predictions[0]

    for i, confidence in enumerate(predictions):

        if predictions[highest_index] < confidence:
            highest_index = i

    return {
        'type': soil_types[highest_index],
        'confidence': predictions[highest_index],
    }

def present_ph_prediction(prediction):
    return prediction

def prepare_soil_type_data(prediction):
    return prediction

def prepare_ph_data(prediction):

    print('************** color-prediction')
    print(len(prediction))

    color = np.mean(prediction, axis=(0, 1))

    color = {
        'r': color[0],
        'g': color[1],
        'b': color[2],
    }

    color['h'] = getH(color['r'], color['g'], color['b'])
    color['s'] = getS(color['r'], color['g'], color['b'])
    color['v'] = getV(color['r'], color['g'], color['b'])

    color['si1'] = color['r'] / color['g'] / color['b']
    color['si2'] = color.h / color.s / color.v
    color['si3'] = color.h / color.s
    color['si4'] = color.h + color.s
    color['si5'] = color.h + color.s + color.v
    color['si6'] = color.s / color.v
    color['si7'] = color.s + color.v
    color['si8'] = color['r'] / color['g']
    color['si9'] = color['r'] + color['g']
    color['si10'] = color['r'] + color['g'] + color['b']
    color['si11'] = color['g'] / color['b']
    color['si12'] = color['g'] + color['b']

    print('************** color')
    print(len(color))

    return color


MODEL_FUNCTIONS = {
    'soiltype': {
        'present': present_soil_type_prediction,
        'prepare': prepare_soil_type_data,
    },
    'ph': {
        'present': present_ph_prediction,
        'prepare': prepare_ph_data,
    },
}

def load_model(model_path):

    print(model_path)

    return keras.models.load_model(filepath=model_path)

def load_image_batch(image_fp):

    im = cv2.imread(image_fp)  # load image
    plt.imshow(im[:, :, [2, 1, 0]])
    img = keras.preprocessing.image.load_img(image_fp, target_size=(256, 256))
    img = keras.preprocessing.image.img_to_array(img)

    image_array = img / 255.  # scale the image

    return np.expand_dims(image_array, axis=0)


def make_predictions(image_fp):

    img_batch = load_image_batch(image_fp)

    predictions = {}

    for model_path, model_function in MODEL_FUNCTIONS.items():

        try:

            input_data = model_function['prepare'](img_batch)

            model = load_model(
                'model/' + model_path + '.h5'
            )

            prediction = model.predict(input_data)

            data = model_function['present'](prediction.tolist())

            predictions[model_path] = data



        except Exception as e:
            print('*********** exception')
            print(e)
            pass

    return predictions


def remove_background(image, bg_color=255):
    # assumes rgb image (w, h, c)
    intensity_img = np.mean(image, axis=2)

    # identify indices of non-background rows and columns, then look for min/max indices
    non_bg_rows = np.nonzero(np.mean(intensity_img, axis=1) != bg_color)
    non_bg_cols = np.nonzero(np.mean(intensity_img, axis=0) != bg_color)
    r1, r2 = np.min(non_bg_rows), np.max(non_bg_rows)
    c1, c2 = np.min(non_bg_cols), np.max(non_bg_cols)

    # return cropped image
    return image[r1+10:r2+0, c1+10:c2+0, :]


def prepare_image(file_data):

    # convert string data to numpy array
    file_bytes = np.fromstring(file_data, np.uint8)

    # convert numpy array to image
    img = cv2.imdecode(file_bytes, cv2.IMREAD_UNCHANGED)

    ## (1) Convert to gray, and threshold
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    th, threshed = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

    ## (2) Morph-op to remove noise
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    morphed = cv2.morphologyEx(threshed, cv2.MORPH_CLOSE, kernel)

    ## (3) Find the max-area contour
    cnts = cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    cnt = sorted(cnts, key=cv2.contourArea)[-1]

    ## (4) Crop and save it
    x, y, w, h = cv2.boundingRect(cnt)

    result = img[y+10:y + h-10, x+10:x + w-10]

    return result, Image.fromarray(result)