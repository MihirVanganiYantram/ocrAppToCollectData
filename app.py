from flask import Flask, render_template, request, jsonify
from PIL import Image
from io import BytesIO
import base64
import easyocr
import numpy as np

app = Flask(__name__)
reader = easyocr.Reader(['en'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    image_file = request.files['image']
    image = Image.open(image_file)
    image.save('static/uploaded_image.png')
    return jsonify({'status': 'Image uploaded'})

@app.route('/ocr', methods=['POST'])
def apply_ocr():
    data = request.json
    image_data = data['image']
    selection = data['selection']

    # Decode the base64 image data and open it as an image
    image = Image.open(BytesIO(base64.b64decode(image_data)))

    # Crop the image to the selected region
    cropped_image = image.crop((
        selection['startX'],
        selection['startY'],
        selection['startX'] + selection['width'],
        selection['startY'] + selection['height']
    ))

    # Convert the cropped image to a format EasyOCR can work with
    cropped_image = np.array(cropped_image)

    # Apply OCR
    result = reader.readtext(cropped_image)
    text = ' '.join([item[1] for item in result])

    return jsonify({'text': text})

if __name__ == '__main__':
    app.run(debug=True)
