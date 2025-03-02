# Person Detection System

This project is a web-based application that allows users to upload an image and detect people in it using a person detection algorithm. The system processes the uploaded image by drawing bounding boxes around detected persons, returns the processed image along with the count of detected people, and saves the results to a PostgreSQL database. A dedicated web page provides access to historical records with pagination, search, and filtering capabilities.

---

## Table of Contents

- [Person Detection System](#person-detection-system)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Architecture](#architecture)
    - [Backend](#backend)
    - [Frontend](#frontend)
    - [Database](#database)
    - [Deployment](#deployment)
  - [Setup \& Installation](#setup--installation)
    - [Prerequisites](#prerequisites)
    - [Repository Clone](#repository-clone)
    - [Video Demo](#video-demo)
  - [Training Human Detector](#training-human-detector)
    - [Setup Instructions](#setup-instructions)
    - [Data Preparation](#data-preparation)
    - [Training](#training)
    - [Inference](#inference)
    - [Video Tracking Demo](#video-tracking-demo)

---

## Features

- **Image Upload**: Users can upload an image via a web UI.
- **Person Detection**: The backend runs a person detection algorithm on the uploaded image to count the number of people present.
- **Visualization**: Detected bounding boxes are visualized on the image.
- **Result Display**: The processed image and the count of detected people are returned to the web UI.
- **Database Logging**: Each detection record is saved in a PostgreSQL database along with the timestamp, count of detected persons, and the file path of the visualized image.
- **History Page**: A dedicated web page allows users to view past detection records with features like pagination, search, and filtering.

---

## Architecture

### Backend

- **Language**: Python
- **Framework**: FastAPI
- **Data Validation**: Pydantic models provided by FastAPI for API data validation.
- **Image Processing**: Incorporates a person detection algorithm to identify and count people in images.
- **Database Interaction**: Uses SQLAlchemy for ORM to interact with PostgreSQL.

### Frontend

- **Framework**: Next.js
- **Functionality**: Provides a user-friendly interface for image uploads and displays detection results as well as historical records.

### Database

- **Database**: PostgreSQL
- **ORM**: SQLAlchemy is used to interact with the database, storing records such as detection time, number of detected people, and the path to the visualized image.

### Deployment

- **Containerization**: The application is containerized using Docker, which manages separate containers for the backend, frontend, and database.

---

## Setup & Installation

### Prerequisites

- Docker / Docker Desktop installed on your machine.
- (Optional) Python 3.11+ and Node.js v20+ for local development outside of Docker.

### Repository Clone

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/Hung369/Human-Detector-Website.git
cd Human-Detector-Website/src
```
Build and run the application using Docker Compose:

```bash
docker-compose up --build
```

This command builds the necessary Docker images and starts the containers for the backend, frontend, and PostgreSQL database.

**Accessing the Application**: Visit http://localhost:3000 in your browser.

---
### Video Demo

demo link

---

## Training Human Detector

### Setup Instructions

1. **Clone the repository:**

    ```bash
    git clone https://github.com/Hung369/Human-Detector-Website.git
    cd Human-Detector-Website/training
    ```

2. **Create a virtual environment:**

    ```bash
    python -m venv env
    source env/bin/activate  # Windows: env\Scripts\activate
    ```

3. **Install dependencies:**

    ```bash
    pip install ultralytics
    ```

---

### Data Preparation

1. **Dataset Acquisition:**  
   Obtain a Person Detection dataset via this [Roboflow project](https://universe.roboflow.com/titulacin/person-detection-9a6mk) or your own collection. Ensure your dataset includes annotated images in the YOLOv11 format.

2. **Directory Structure:**  
   Organize your dataset as follows:

    ```
    /train
      /images
      /labels
    /valid
      /images
      /labels
    /test
      /images
      /labels
    ```

3. **Configuration File:**  
   Update the `data.yaml` file with:
   - Paths to your training and validation datasets.
   - List of class names.

---

### Training

Train YOLOv11 using the provided training script. Adjust hyperparameters as needed.

```bash
python train.py
```
---

### Inference

To run detection and tracking on a video:
```bash
python inference.py --input "your input .mp4 video path" --output "your output .mp4 video path" --weights "./runs/detect/train/weights/best.pt" --tracker "botsort.yaml"
```
---

### Video Tracking Demo

<iframe src="https://drive.google.com/file/d/1Wrng3WveRiYwx1IfuDTlkSA3L3L4Cwmv/preview" width="640" height="480" allow="autoplay"></iframe>