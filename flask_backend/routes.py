# routes.py
from flask import Flask, render_template, request, redirect, url_for
from models import init_db, add_case
from face_detection import detect_face
from retina_scan import retina_scan
from pdf_analysis import analyze_pdf
import os

app = Flask(__name__)
init_db()

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    biometric = request.form['biometric']
    
    # Mock verification logic
    if username == "admin" and password == "password" and biometric == "biometric_data":
        image_path = os.path.join('static', 'face_images', 'user_face.jpg')  # Simulated face path
        if detect_face(image_path):
            return redirect(url_for('home_page'))
        else:
            return "Face not detected. Please try again."
    return "Invalid login details."

@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    pdf_file = request.files['pdf_file']
    if pdf_file:
        file_path = os.path.join('uploads', pdf_file.filename)
        pdf_file.save(file_path)
        result = analyze_pdf(file_path)
        return f"Crime Analysis: {result}"

@app.route('/retina_scan', methods=['POST'])
def retina_scan_route():
    retina_image = request.files['retina_image']
    if retina_image:
        result = retina_scan(retina_image.filename)
        return f"Result: {result}"

@app.route('/manage_case', methods=['POST'])
def manage_case_route():
    case_details = request.form['case_details']
    location = request.form['location']
    crime_type = request.form['crime_type']
    add_case(case_details, location, crime_type)
    return redirect(url_for('case_management'))

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/contact')
def contact_page():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
