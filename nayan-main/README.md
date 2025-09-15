# Nayan - Post OCR Correction Tool

Nayan is a post-OCR correction tool designed to refine and correct text from OCR'd Nepali KYC documents like citizenship cards and voter IDs. The core of the application is a custom-trained Google T5 model, using transfer learning on a private dataset to correct both Devanagari and Roman Nepali script as accurately as possible.

It features a Python FastAPI backend that serves the correction model and a user-friendly React frontend for interaction. The entire application is containerized using Docker and Docker Compose for a consistent and streamlined development experience.

---
## Tech Stack 🛠️

* **Backend:** Python, FastAPI 
* **Frontend:** React, Node.js 
* **Containerization:** Docker, Docker Compose 

---
## File Structure
```
nayan/
├── dataset/
    ├── Data Augmentation/
    └── roman_nepali_dataset.csv 
    └── devnagari_nepali_dataset.csv 
│   │
├── backend/
│   ├── model/
        <!-- added after downloading the model -->
│   │   └── ocr_correction_model/
│   │   └── ocr-post-corr-nepali/
│   │   └── README.md
│   ├── app.py
│   ├── Dockerfile
│   ├── .dockerignore
│   └── requirements.txt
│
├── frontend/
│   ├── public/
│   ├── src/
│   ├── Dockerfile
│   ├── .dockerignore
│   └── package.json
│
├── .gitignore
├── docker-compose.yml
└── README.md
```

---
## Setup and Running the Application

This project is fully containerized, so you do not need to install Python or Node.js on your host machine.

### Prerequisites

* [Docker](https://www.docker.com/products/docker-desktop/)
* Docker Compose (V2 Plugin, which is included with modern Docker installations)

### Installation & Usage

1.  **Clone the repository**
    ```bash
    git clone https://gitlab.com/BipinNeupane/nayan/
    cd nayan
    ```

2.  **Build the Docker images**
    ```bash
    docker compose build
    ```

3.  **Run the application**
    ```bash
    docker compose up
    ```
    * The **React Frontend** will be available at `http://localhost:3000`
    * The **FastAPI Backend** will be available at `http://localhost:8000`

4.  **Stopping the application**
    To stop and remove the containers, press `Ctrl + C` in the terminal where the application is running, or run the following command from another terminal:
    ```bash
    docker compose down
    ```

---

## Model Setup

This project requires custom models to function. These models must be downloaded separately. For detailed instructions on how to download and place the models correctly, please see the model setup guide:

**[Click here for Model Setup Instructions](./backend/model/README.md)**

## Development Workflow

This setup is configured for an efficient development workflow with **hot-reloading**.

* Any changes you make to the frontend code (`frontend/src`) will automatically reload in your browser.
* Any changes you make to the backend code (`backend/app.py`, etc.) will automatically restart the FastAPI server.

There is no need to rebuild the images unless you install new dependencies in `requirements.txt` or `package.json`. If you do, just run `docker compose up --build`.
