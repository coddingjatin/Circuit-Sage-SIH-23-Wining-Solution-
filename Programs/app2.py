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
def CookieScrapper():
    cookie_dict = {
        "__Secure-1PSID": "g.a000gQiUyHwmMr9MIBWd1OCW1lOxA7P74nUFK9UYrgUuXZD8eALZ1Vbg95MorQMeSfuTtNMf3QACgYKAdsSAQASFQHGX2MiYxPjG4dxF3ggpUjAFteQ_RoVAUF8yKodGLuRXOAL6Re6TWR1rTcF0076",
        "__Secure-1PSIDTS": "sidts-CjEBYfD7Z7IB7bFtohU8PA3YtucXzxUcOhlZhJB4HuyzFZaVnoJutfJmw0rbeDOu9pjUEAA",
        "__Secure-1PSIDCC": "ABTWhQHVftHIfg0ZYY8Gwf9PoUDjzwUwtGZ4hInS_QHOsQ8JoRJrEaubnuoWR8rZKIgqr2Lqb-qV",
    }
    return cookie_dict

# Initialize Bard object and get cookies
cookie_dict = CookieScrapper()
bard = BardCookies(cookie_dict=cookie_dict)

@app.route('/')
def index():
    return render_template('index.html') 
@app.route('/index1')
def index1():
    return render_template('index1.html')

def preprocess_image(img):
    img_array = cv2.resize(img, (224, 224))
    img_array = image.img_to_array(img_array)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    return img_array

def predict_image(img, custom_model, class_labels):
    img_array = preprocess_image(img)
    predictions = custom_model.predict(img_array)

    # Assuming your custom model directly outputs class probabilities
    # Adjust this part based on your custom model's output format
    top_predictions = np.argsort(predictions[0])[::-1][:5]  # Get indices of top 5 predictions
    labels = [str(idx) for idx in top_predictions]

    decoded_predictions = [(label, class_labels[int(label)], predictions[0, int(label)]) for label in labels]

    return decoded_predictions

def select_image():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path

def process_data_custom(custom_model, class_labels):
    image_path = select_image()

    if image_path:
        img = cv2.imread(image_path)
        predictions = predict_image(img, custom_model, class_labels)

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

@app.route('/process_data', methods=['POST'])
def process_data():
    # Load your custom model for the transformer
    custom_model_transformer = tf.keras.models.load_model('custom_transformer_model.h5')
    class_labels_transformer = ["Oil Leakage\n Solution for Oil Leakage : \n 1)Identify Source:\n Locate the oil leakage source through visual inspection.\n 2)Isolate Transformer:\nDe-energize and isolate the transformer for safety.\n 3)Assess Severity:\nDetermine the extent of the leakage.\n 4)Safety Measures:\nWear appropriate PPE for safety.\n 5)Contain Spill:\nUse absorbent materials to contain and clean up spilled oil.\n", "Normal:\n Transformer is not in Normal State if value is more than 0.03\nThere is :", "Burnt Transformer\nSolution for Burst Transformer :\n 1)Safety First:\nDe-energize and isolate the transformer.\nWear appropriate PPE.\n\nAssessment:\nInspect the transformer for damage.\nDocument the condition and identify the cause of the burning.\n\n\Cool Down:\nAllow the transformer to cool before proceeding\n\nInspect Components:\nCheck bushings and insulation for damage.\n\nRepair/Replace:\nAddress the identified issues through repairs or component replacements.\nTest the transformer's repaired components.\nRe-energize the transformer if deemed safe.\n\nPreventive Measures:\nImplement measures to prevent future incidents, addressing the root cause.", "Rusting :\nIsolate the Transformer:\nDe-energize and isolate the transformer to ensure safety during maintenance\n\nSafety Measures:\nWear appropriate personal protective equipment (PPE), including gloves and safety glasses.\n\nInspect the Transformer:\nThoroughly inspect the transformer for signs of rust on the outer surface and critical components\n\nClean Rusty Areas:\nUse a wire brush, sandpaper, or other appropriate tools to clean the rusted areas. Remove loose rust, scale, and dirt.\n\nApply Rust Converter:\nApply a rust converter or inhibitor to the cleaned surfaces.\n Rust converters chemically convert rust into a stable compound, preventing further corrosion.\n\nRepaint the Transformer:\nAfter applying the rust converter, repaint the transformer with a suitable, corrosion-resistant paint. \nEnsure the paint is designed for outdoor and high-temperature applications\n", "\nTest"]

    # Process data for the transformer
    result_transformer = process_data_custom(custom_model_transformer, class_labels_transformer)
    return result_transformer

@app.route('/process_data_substation', methods=['POST'])
def process_data_substation():
    # Load your custom model for the substation
    custom_model_substation = tf.keras.models.load_model('substation_model.h5')
    class_labels_substation = ['Power_line_conductor Damaged\nIsolate the Damaged Section:\nIdentify the location of the damaged conductor.\nIf possible, isolate the damaged section to prevent further issues or potential hazards.\n\nEnsure Safety:\nBefore conducting any maintenance, ensure that all safety protocols are followed.\nUse appropriate personal protective equipment (PPE) such as insulated gloves and safety gear\n.If the damaged conductor poses a safety risk, secure the area and, if necessary, coordinate with local authorities.\n\nAssess the Damage:\nDetermine the extent of the damage to the conductor.\nEvaluate whether the damage is due to physical impact, corrosion, wear, or other factors.\n\nTemporary Repairs:\nDepending on the severity of the damage, consider making temporary repairs to restore the functionality of the power line.\nThis might involve splicing the conductor, applying conductor repair sleeves, or using other temporary solutions.\n\nCoordinate with Authorities:\nIf the power line is part of a larger electrical grid or system, coordinate with relevant authorities or utility companies.\nInform them about the damage and follow any established procedures for reporting and addressing such issues.\n', 'Insulator Problem\nVisual Inspection:\nConduct regular visual inspections of insulators to identify any signs of physical damage, such as cracks, chips, or contamination.\n\nCleaning:\nIf insulators are contaminated, clean them using a non-abrasive cleaning solution and a soft brush.\nEnsure that the insulator is completely dry before returning it to service.\nInspect for Cracks:\nCarefully inspect insulators for any visible cracks. Cracked insulators can compromise their electrical and mechanical strength.\n\nTesting:\nPerform routine electrical testing to ensure that insulators maintain their dielectric strength.\nUse appropriate testing equipment to measure leakage current, insulation resistance, and other relevant parameters.\n\nReplace Damaged Insulators:\nIf an insulator is found to be damaged beyond repair, replace it promptly.\nUse insulators that meet the specifications and standards for the particular application.', 'Circuit_Breaker Damaged :\nSolutions and Maintance :\n\nIsolate the Circuit:\nEnsure that the circuit breaker is safely isolated from the electrical system. Follow proper lockout/tagout procedures to de-energize the circuit and prevent accidental re-energization during maintenance.\n\nAssessment of Damage:\nIdentify the type and extent of the damage to the circuit breaker. This may include visual inspection and, if necessary, diagnostic testing.\n\nSafety Gear:\nUse appropriate personal protective equipment (PPE), including insulated gloves, safety glasses, and other gear, to protect against electrical hazards.\n\nDocument the Damage:\nDocument the observed damage, including any visible signs of wear, overheating, or physical damage.']

    # Process data for the substation
    result_substation = process_data_custom(custom_model_substation, class_labels_substation)
    return result_substation

@app.route('/query', methods=['POST'])
def process_query():
    if request.method == 'POST':
        try:
            question = request.form['query'].strip()
            real_question = question + "in 75 words related to substation maintainance"

            results = bard.get_answer(real_question)['content']

            speech = gTTS(text=results, lang='en', slow=False)
            speech.save('answer.mp3')

            return results
        except Exception as e:
            return str(e)
        
@app.route('/Circuit_Breaker')
def Circuit_Breaker():
    return render_template('Circuit_Breaker.html')  

@app.route('/Surge_Testing')
def Surge_Testing():
    return render_template('Surge_Testing.html')  

@app.route('/Transformer_Testing')
def Transformer_Testing():
    return render_template('Transformer_Testing.html')        

# code 
@app.route('/translate', methods=['POST']) 
def index_post(): 
	
	# Read the values from the form 
	original_text = request.form['text'] 
	target_language = request.form['language'] 

	# Load the values from .env 
	key = os.environ['KEY'] 
	endpoint = os.environ['ENDPOINT'] 
	location = os.environ['LOCATION'] 

	# Indicate that we want to translate and the API 
	# version (3.0) and the target language 
	path = '/translate?api-version=3.0'
	
	# Add the target language parameter 
	target_language_parameter = '&to=' + target_language 
	
	# Create the full URL 
	constructed_url = endpoint + path + target_language_parameter 

	# Set up the header information, which includes our 
	# subscription key 
	headers = { 
		'Ocp-Apim-Subscription-Key': key, 
		'Ocp-Apim-Subscription-Region': location, 
		'Content-type': 'application/json', 
		'X-ClientTraceId': str(uuid.uuid4()) 
	} 

	# Create the body of the request with the text to be 
	# translated 
	body = [{'text': original_text}] 

	# Make the call using post 
	translator_request = requests.post( 
		constructed_url, headers=headers, json=body) 
	
	# Retrieve the JSON response 
	translator_response = translator_request.json() 
	
	# Retrieve the translation 
	translated_text = translator_response[0]['translations'][0]['text'] 

	# Call render template, passing the translated text, 
	# original text, and target language to the template 
	return render_template( 
		'results.html', 
		translated_text=translated_text, 
		original_text=original_text, 
		target_language=target_language 
	) 


if __name__ == '__main__':
    app.run(debug=True)
