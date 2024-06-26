import io
import json
import os

import cv2
import ftfy
from numpy import unicode_
import pytesseract
from flask import Flask, request, jsonify
from flask_cors import CORS

import Dbmongo.connect_database as db
import aadhaar_read
import easy_extract
import pan_read
from aadharValidation import Validate

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/upload', methods=['POST'])
def main():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        # path = r'sample-aadhar5.jpg'
        path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(path)

        img = cv2.imread(path)
        img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        var = cv2.Laplacian(img, cv2.CV_64F).var()

        if var < 5:
            print("Image is Too Blurry....")
            k = input('Press Enter to Exit.')
            exit(1)

        filename = path
        img2str_config_name = "--psm 4 --oem 3"

        text = pytesseract.image_to_string(img, lang='eng+tam')

        # Tamtext = pytesseract.image_to_string(Image.open(filename), lang = 'tam')
        #
        # print(Tamtext)
        # print(Image.open(filename))
        # cv2.imshow("Image",Image.open(filename))

        text_output = open('output.txt', 'w', encoding='utf-8')
        text_output.write(text)
        text_output.close()

        file = open('output.txt', 'r', encoding='utf-8')
        text = file.read()

        text = ftfy.fix_text(text)
        text = ftfy.fix_encoding(text)
        # print(text)
        if "income" in text.lower() or "tax" in text.lower() or "department" in text.lower():
            data = pan_read.pan_read_data(text)
        elif "male" in text.lower():
            data = aadhaar_read.adhaar_read_data(text,img)
        else:
            data = aadhaar_read.adhaar_read_data(text,img)
        print("Data : ",data)
        
        if not data:
            return {"result":"failed", "message":"Aadhar card format out of date or problem with the Image"}
        
        if all(data[key] is not None for key in data):
            pass
        else:
            print("-------------Easy Ocr-------------------")
            text = easy_extract.easy_read(filename)
            # print(text)
            text_output = open('output.txt', 'w', encoding='utf-8')
            text_output.write(text)
            text_output.close()

            file = open('output.txt', 'r', encoding='utf-8')
            text = file.read()

            text = ftfy.fix_text(text)
            text = ftfy.fix_encoding(text)
            data = aadhaar_read.adhaar_read_data(text,img)
            # print("Text: ", text)

        # print("\n\n\n\ndata:", type(data['Adhaar Number']))    
        print("Data :", data)
        Aadhaar_validation = Validate(data['Adhaar Number'])
        print("\n\n\n\n\n", Aadhaar_validation)
        
        if Aadhaar_validation:
            print("\nAadhar Card Number is Verified and Valid!\n")
            
        else:
            result = {"result": "Failed", "message": "Aadhar Verification Failed!. Aadhar number not valid"}
            return jsonify(result)
        
        
        try:
            to_unicode = unicode # type: ignore
            # to_unicode = unicode_
            
        except NameError:
            to_unicode = str
        with io.open('info.json', 'w', encoding='utf-8') as outfile:
            data = json.dumps(data, indent=4, sort_keys=True, separators=(',', ': '), ensure_ascii=False,default=str)
            outfile.write(to_unicode(data))

        with open('info.json', encoding='utf-8') as data:
            data_loaded = json.load(data)

        db.store_aadhar_info(data_loaded)
        print(data_loaded)
        data_loaded["_id"] = str(data_loaded["_id"])

        final_data = {}
        
        final_data["result"] = "Passed"
        final_data["message"] = "Aadhar Verification Successfull"
        final_data["data"] = data_loaded

        if data_loaded['ID Type'] == 'PAN':
            print("\n---------- PAN Details ----------")
            print("\nPAN Number: ", data_loaded['PAN'])
            print("\nName: ", data_loaded['Name'])
            print("\nFather's Name: ", data_loaded['Father Name'])
            print("\nDate Of Birth: ", data_loaded['Date of Birth'])
            print("\n---------------------------------")
        elif str.upper(data_loaded['ID Type']) == 'ADHAAR':
            print("\n---------- ADHAAR Details ----------")
            print("\nADHAAR Number: ", data_loaded['Adhaar Number'])
            print("\nName: ", data_loaded['Name'])
            print("\nDate Of Birth: ", data_loaded['Date of Birth'])
            print("\nSex: ", data_loaded['Sex'])
            print("\n------------------------------------")
        return jsonify(final_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)