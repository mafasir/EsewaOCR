# Model Setup

This directory contains models required for the application to function. The models are hosted on Hugging Face and must be cloned from their respective repositories.

## Prerequisites

* You must have **Git** installed on your system.
* You should have **Git LFS** (Large File Storage) installed, as these models may be large. You can install it by following the instructions [here](https://git-lfs.com).

## Setup Instructions

To set up the models, you will need to clone two separate repositories and then copy the model folders into this directory.

1.  **Clone the First Model (e.g., Devanagari Correction)**
    Navigate to a temporary location outside of this project directory and clone the first model's repository.

    ```bash
    git clone https://huggingface.co/CrashOnline/Nayan-Devnagari-Modell/
    ```

2.  **Clone the Second Model (e.g., Roman Nepali Correction)**
    In the same temporary location, clone the second model's repository.

    ```bash
    git clone https://huggingface.co/CrashOnline/Nayan-OCR
    ```

3.  **Copy the Models into this Directory**
    Once cloned, copy the actual model folders from the cloned repositories into this `backend/model/` directory.

    Folders Name:
    ocr_correction_model/ (For Roman Nepali.)
    ocr-post-corr-nepali/ (For Devnagari Nepali)


After copying, your `model` directory should look something like this:
```
├── backend/
│   ├── model/
        <!-- added after downloading the model -->
│   │   └── ocr_correction_model/
│   │   └── ocr-post-corr-nepali/
│   │   └── README.md
```