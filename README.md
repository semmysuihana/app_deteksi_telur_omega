# EggMaster: Omega Egg Detection
EggMaster is a web application designed to detect and classify different types of eggs based on their variety. Using a machine learning model from Roboflow, it can identify 'Omega 3', 'Omega 9', and 'Curah' (standard) eggs from either an uploaded image or a live camera feed.

## Features

*   **Image-based Detection:** Upload a `.jpg`, `.jpeg`, or `.png` image to detect and classify eggs.
*   **Live Camera Detection:** Use your device's camera to capture and analyze eggs in real-time.
*   **Classification:** Identifies three classes of eggs: `omega3`, `omega9`, and `curah`.
*   **Visual Feedback:** Displays the analyzed image with colored bounding boxes, class labels, and confidence scores for each detected egg.

## How It Works

The application provides a simple web interface with two options: upload an image or use the camera.

1.  **Image Submission:** The user's image (from a file or camera capture) is sent to the Flask backend.
2.  **Model Prediction:** The Flask server sends the image to a pre-trained Roboflow object detection model (`eggmaster/telur-ie0xj`).
3.  **Result Processing:** The backend receives the prediction results (class, coordinates, confidence) in JSON format.
4.  **Image Annotation:** Using the Pillow library, the application draws bounding boxes and labels for each detected egg directly onto the image. The box color corresponds to the egg class:
    *   **Blue:** Omega 3
    *   **Green:** Omega 9
    *   **Red:** Curah (Standard)
5.  **Display Result:** The final annotated image is saved to the `static` directory and displayed to the user on the web page.

## Technology Stack

*   **Backend:** Python, Flask
*   **Frontend:** HTML, Bootstrap 5, JavaScript
*   **Object Detection:** [Roboflow](https://roboflow.com/)
*   **Image Processing:** Pillow (PIL)
*   **Deployment:** Configured for Vercel

## Local Setup and Installation

To run this project on your local machine, follow these steps.

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/semmysuihana/app_deteksi_telur_omega.git
    cd app_deteksi_telur_omega
    ```

2.  **Create and Activate a Virtual Environment**
    ```bash
    # For Unix/macOS
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    venv\Scripts\activate
    ```

3.  **Install Dependencies**
    A `requirements.txt` is not included. You will need to install the required packages manually.
    ```bash
    pip install Flask roboflow Pillow
    ```
    The application also requires the "Arial Bold" font (`arialbd.ttf`) to be available on the system to render labels on the images. This font is standard on most Windows systems but may need to be installed on Linux/macOS.

4.  **Configure API Key**
    The application requires a Roboflow API key. Open `app.py` and replace the existing key with your own Roboflow private API key.
    ```python
    # in app.py
    rf = Roboflow(api_key="YOUR_ROBOFLOW_API_KEY")
    ```

5.  **Run the Application**
    ```bash
    flask run
    ```
    Open your web browser and navigate to `http://127.0.0.1:5000` to use the application.

## Project Structure

```
.
├── app.py              # Main Flask application with all backend logic
├── vercel.json         # Vercel deployment configuration
├── templates/
│   ├── index.html      # Main landing page with navigation
│   ├── cek-gambar.html # Page for image upload and detection
│   └── cek-kamera.html # Page for live camera detection
└── static/
    ├── asset/          # UI images for cards
    └── annotated_image.jpg # Default output path for processed images
