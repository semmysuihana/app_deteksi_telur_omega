from flask import Flask, render_template, request, redirect, url_for
from roboflow import Roboflow
from PIL import Image, ImageDraw, ImageFont
import tempfile
import base64  # Add this line to import base64

app = Flask(__name__)

# Replace "your_api_key" with your actual Roboflow API key
rf = Roboflow(api_key="2MccZKlhoXwzPtlFdFy6")

@app.route('/cek-gambar', methods=['GET', 'POST'])
def cek_gambar():
    if request.method == 'POST':
        uploaded_image = request.files['file']
        if uploaded_image.filename != '':
            temp_file = tempfile.NamedTemporaryFile(delete=False)
            uploaded_image.save(temp_file.name)
            
            project = rf.workspace("eggmaster").project("telur-ie0xj").version(1)
            model = project.model
            result = model.predict(image_path=temp_file.name, confidence=40).json()

            image_path = result['predictions'][0]['image_path']
            image = Image.open(image_path)
            draw = ImageDraw.Draw(image)

            for prediction in result['predictions']:
                bbox = [
                    (prediction['points'][0]['x'], prediction['points'][0]['y']),
                    (prediction['points'][1]['x'], prediction['points'][1]['y']),
                    (prediction['points'][2]['x'], prediction['points'][2]['y']),
                    (prediction['points'][3]['x'], prediction['points'][3]['y']),
                ]

                label_name = prediction['class']
                color = ""
                if label_name == "omega3":
                    color = (0, 0, 255)
                elif label_name == "omega9":
                    color = (0, 255, 0)
                elif label_name == "curah":
                    color = (255, 0, 0)
                draw.polygon(bbox, outline=color, width=3)

                predicted_class = prediction['class']
                confidence = prediction['confidence']
                label_text = f"{predicted_class}: {confidence:.2f}"

                box_width = bbox[2][0] - bbox[0][0]
                box_height = bbox[2][1] - bbox[0][1]
                base_font_size = 10
                max_box_dimension = max(box_width, box_height)
                font_size = int(base_font_size * (max_box_dimension / 100))

                font = ImageFont.truetype("arialbd.ttf", font_size)
                label_position = ((bbox[0][0] + bbox[2][0]) / 2, bbox[0][1] - font_size // 2)

                draw.text(label_position, label_text, fill=color, font=font, anchor="mm") 

            annotated_image_path = "static/annotated_image.jpg"
            image.save(annotated_image_path)

            return render_template('cek-gambar.html', uploaded=True, image_path=annotated_image_path)

    return render_template('cek-gambar.html', uploaded=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    # Implement logic for '.html' here
    return render_template('index.html')

@app.route('/cek-kamera', methods=['GET', 'POST'])
def cek_kamera():
    # Implement logic for 'cek-kamera.html' here
    if request.method == 'POST':
        try:
            # Mendapatkan data gambar dari kamera
            captured_data = request.form['capturedData']

            # Mengubah data gambar base64 menjadi objek gambar
            image_data = base64.b64decode(captured_data.split(',')[1])

            # Simpan gambar dalam file sementara
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
                temp_file.write(image_data)
                temp_file_path = temp_file.name

            # Melakukan deteksi pada gambar dari kamera
            project = rf.workspace("eggmaster").project("telur-ie0xj").version(1)
            model = project.model
            result = model.predict(image_path=temp_file_path, confidence=40).json()

            # Menyimpan hasil deteksi ke gambar
            image = Image.open(temp_file_path)
            draw = ImageDraw.Draw(image)

            for prediction in result['predictions']:
                bbox = [
                    (prediction['points'][0]['x'], prediction['points'][0]['y']),
                    (prediction['points'][1]['x'], prediction['points'][1]['y']),
                    (prediction['points'][2]['x'], prediction['points'][2]['y']),
                    (prediction['points'][3]['x'], prediction['points'][3]['y']),
                ]

                label_name = prediction['class']
                color = ""
                if label_name == "omega3":
                    color = (0, 0, 255)
                elif label_name == "omega9":
                    color = (0, 255, 0)
                elif label_name == "curah":
                    color = (255, 0, 0)
                draw.polygon(bbox, outline=color, width=3)

                predicted_class = prediction['class']
                confidence = prediction['confidence']
                label_text = f"{predicted_class}: {confidence:.2f}"

                box_width = bbox[2][0] - bbox[0][0]
                box_height = bbox[2][1] - bbox[0][1]
                base_font_size = 10
                max_box_dimension = max(box_width, box_height)
                font_size = int(base_font_size * (max_box_dimension / 100))

                font = ImageFont.truetype("arialbd.ttf", font_size)
                label_position = ((bbox[0][0] + bbox[2][0]) / 2, bbox[0][1] - font_size // 2)

                draw.text(label_position, label_text, fill=color, font=font, anchor="mm") 

            annotated_image_path = "static/annotated_image.jpg"
            image.save(annotated_image_path)

            return render_template('cek-kamera.html', uploaded=True, image_path=annotated_image_path)
        except Exception as e:
            print(f"Error processing image: {e}")

    return render_template('cek-kamera.html', uploaded=False)

if __name__ == '__main__':
    app.run(debug=True)
