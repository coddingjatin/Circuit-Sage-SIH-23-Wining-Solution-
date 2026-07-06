from flask import Flask, render_template, request, jsonify
from gtts import gTTS
from bardapi import BardCookies
from flask_cors import CORS
from flask import send_from_directory
import tensorflow as tf
from tkinter import Tk, filedialog
from flask import Flask, render_template, request
from gtts import gTTS
from bardapi import BardCookies
import pyperclip
from flask_cors import CORS
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
import numpy as np
import cv2
from tkinter import Tk, filedialog


app = Flask(__name__)
CORS(app)

# Define the CookieScrapper function to get the necessary cookies
def CookieScrapper():
    # Your code to retrieve cookies goes here...
    # Replace this with your method to retrieve cookie data from the clipboard or another source
    cookie_dict = {
        "__Secure-1PSID": "eQiEl9iesYcZZBH39i6zIrFnXug4AImdVB8tJrmHT0D_spLv8EaFbBtVENnEEgvJoVd4tg.",
        "__Secure-1PSIDTS": "sidts-CjIBPVxjSnBzUpvRrc_wpbIVm-Gj_SqlWOn0Zv9FGYRX1pb49KAEpLFVYkL483k2NFe7XBAA",
        "__Secure-1PSIDCC": "ABTWhQGcy_LyP3057jMxF4QVXChUhHBwgcuLG-xXefPNQuPAz-6NaWhlnGHuST-4iC093Oaving",
    }
    return cookie_dict

# Initialize Bard object and get cookies
cookie_dict = CookieScrapper()
bard = BardCookies(cookie_dict=cookie_dict)

@app.route('/')
def index():
    return render_template('index.html')  # Render HTML file for user input
@app.route('/index1')
def index1():
    return render_template('index1.html')
@app.route('/process_data', methods=['POST'])
def process_data():
    data = request.json

    # Load your custom model
    custom_model = tf.keras.models.load_model('custom_transformer_model.h5')

    # Create a function to preprocess the image
    def preprocess_image(img):
        img_array = cv2.resize(img, (224, 224))
        img_array = image.img_to_array(img_array)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)
        return img_array

    def predict_image(img):
        img_array = preprocess_image(img)
        predictions = custom_model.predict(img_array)

        # Assuming your custom model directly outputs class probabilities
        # Adjust this part based on your custom model's output format
        top_predictions = np.argsort(predictions[0])[::-1][:5]  # Get indices of top 5 predictions
        labels = [str(idx) for idx in top_predictions]

        # Create a dummy list of labels (you need to replace this with your actual class labels)
        class_labels = ["Oil Leakage", "Normal", "Burnt Transformer", "Rusting","Test"]

        decoded_predictions = [(label, class_labels[int(label)], predictions[0, int(label)]) for label in labels]

        return decoded_predictions


    # Function to open a file dialog for image selection
    def select_image():
        root = Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()
        return file_path

    # Check if an image file is provided or use the camera
    image_path = select_image()

    if image_path:
        img = cv2.imread(image_path)
        predictions = predict_image(img)

        prediction_results = []
        for i, (imagenet_id, label, score) in enumerate(predictions):
            result_data = f"{i + 1}: {label} ({score:.2f})"
            print(result_data)
            prediction_results.append(result_data)

        result = {'result': '\n'.join(prediction_results)}
        print(result)
        return result
    else:
        return {'result': 'No image path provided.'}

@app.route('/query', methods=['POST'])
def process_query():
    if request.method == 'POST':
        try:
            question = request.form['query'].strip()  # Get the user input and remove whitespace
            real_question = question  # Use the cleaned question directly

            # Get the answer from Bard
            results = bard.get_answer(real_question)['content']

            # Convert the answer to speech
            speech = gTTS(text=results, lang='en', slow=False)
            speech.save('answer.mp3')  # Save the speech audio as "answer.mp3"
            print(results)
            # Render the results page with the answer and speech file path
            return results
        except Exception as e:
            return str(e)


if __name__ == '__main__':
    app.run(debug=True)
