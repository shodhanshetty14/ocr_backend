# Aadhar Card OCR System

## Overview

This project is aimed at developing an OCR (Optical Character Recognition) system tailored for extracting essential information from Aadhar cards. The system processes Aadhar card images and extracts key details such as the individual's name, Aadhar number, date of birth, address, and other relevant information. It utilizes various technologies and libraries to achieve accurate and efficient OCR capabilities.

## Technologies Used

- **Python**: Programming language used for the backend implementation.
- **Tesseract OCR**: Open-source OCR engine for accurate text recognition.
- **EasyOCR**: Python library for OCR tasks, providing support for multiple languages and scripts.
- **Flask**: Lightweight Python web framework used for building the backend server.
- **Matplotlib**: Python plotting library for visualization purposes.
- **MongoDB**: NoSQL database used for storing extracted information (optional, based on project requirements).

## Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/shodhanshetty14/ocr_backend.git
   cd ocr_backend

   pip install vitualenv
   virtualenv venv

   activating virtual environment
            - Windows = venv\Scripts\activate
            - linux = source venv/bin/activate

   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt //if faced some problems use the below command
    pip install -r old_requirements.txt
   ```

3. if used old_requirements.txt then follow these steps
    ```bash
    - open the python interpreter in terminal in your virtual environment
    - then follow these commands in python interpeter
         - from spacy.cli import download
         - download("en_core_web_sm")
    ```

4. Run the Flask server:
   ```bash
   python Main_extract.py
   ```
5. Access the OCR system through the provided endpoints.

## Project Structure

- **`Main_extract.py`**: Flask application entry point containing API endpoints for OCR functionality.
- **`ocr.py`**: Module for performing OCR tasks using Tesseract OCR and EasyOCR.
- **`uploads`**: Contains the images uploaded
- **`requirements.txt`**: List of Python dependencies.
- **`README.md`**: Project documentation.



# Data flow

![image](https://github.com/Anands001/OCR-Project/assets/110816114/0b329a29-674e-409e-b557-4387729be740)

# Project Demo Images
![image](https://github.com/Anands001/OCR-Project/assets/110816114/67a9e15f-2673-436c-9b08-8fcb8b67151c)


