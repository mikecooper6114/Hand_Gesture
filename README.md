# 🖐️ Hand Gesture Recognition Website

---

## Project Description

Hand Gesture Recognition is a dynamic and responsive web application designed to help users interact with a system using natural hand movements. Inspired by popular real-time gesture recognition, it leverages **MediaPipe** and **OpenCV** to provide up-to-date information on recognized gestures, detailed visual feedback, and personalized interaction.

Users can browse content by performing hand gestures, receive real-time updates on detected poses, and curate their own interaction experience. The application is built entirely with vanilla HTML, CSS, and JavaScript on the frontend, powered by a Flask backend, focusing on performance and a smooth user experience.

---

## 💻 Local Demo

You can explore a local demo of the application by following the setup instructions below:

### To Run the Application Locally:
1.  **Clone the Repo:**
    ```bash
    git clone [https://github.com/Boda1607/hand-gesture-website.git](https://github.com/Boda1607/hand-gesture-website.git)
    cd hand-gesture-website
    ```
2.  **Create a Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run Locally:**
    ```bash
    python app.py
    ```
    Then open your browser and go to:
    `http://127.0.0.1:5000/`
    (Remember to grant camera permissions in your browser.)

---

## 🔧 Features

* **Real-time Hand Tracking:** Discover popular hand poses and movements.
* **Gesture Recognition:** Filter recognized gestures by various types (e.g., Fist, Open Hand, Thumbs Up, Peace, Heart Gesture).
* **Dynamic Gesture Toggling:** Sidebar gesture lists can be expanded/collapsed independently, and only one primary category's genres are shown at a time.
* **Smooth Functionality:** Powerful search to find specific gestures or hand poses by title.
* **Detailed Content Pages:** View comprehensive details for each detected gesture, including:
    * Visual representation, confidence, and tracking info.
    * Key landmark data, processing speed.

---

## 📁 Project Structure

```
hand-gesture-website/
├── app.py                     # Main Flask app with MediaPipe + OpenCV
├── templates/
│   └── index.html             # Frontend UI
├── static/
│   ├── style.css              # Optional styling
│   └── script.js              # Optional frontend JavaScript
├── requirements.txt           # Python dependencies
├── Procfile                   # For deployment (Render)
└── runtime.txt                # Optional: Python version (e.g., python-3.10.8)
```

---

## 🌐 Deployment on Render

1.  **Push to GitHub:**
    Create a repository and push your code to GitHub.

2.  **Go to Render:**
    Click [New Web Service](https://render.com/dashboard/new/web-service)

    Connect your GitHub repo.

    Set the environment:

    ```yaml
    Build Command: pip install -r requirements.txt
    Start Command: python app.py
    ```
    Deploy 🎉

---

## ✅ Requirements

See `requirements.txt`, but key packages include:

* `flask`
* `opencv-python`
* `mediapipe`
* `numpy`

---

## 📝 License

This project is open source and free to use under the [MIT License](LICENSE).

---

## 🙋‍♂️ Author

AbdElRahman Hesham
Made with ❤️ using Python, MediaPipe, Flask, and OpenCV.

Portfolio: [abdelrahmanz.netlify.app](https://abdelrahmanz.netlify.app)
