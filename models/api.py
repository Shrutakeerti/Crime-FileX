from flask import Flask, request, jsonify
from database import create_connection
import joblib

app = Flask(__name__)

@app.route('/add_case', methods=['POST'])
def add_case():
    data = request.json
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO cases (case_id, name, blood_group, dna, retina_scan, fingerprint, photos)
                      VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                      (data['case_id'], data['name'], data['blood_group'], data['dna'], 
                       data['retina_scan'], data['fingerprint'], data['photos']))
    conn.commit()
    conn.close()
    return jsonify({"status": "Case added successfully"})

@app.route('/crime_pattern_analysis', methods=['POST'])
def crime_pattern_analysis():
    # Placeholder for crime pattern analysis model
    model = joblib.load("models/crime_pattern_model.pkl")
    data = request.json['data']
    prediction = model.predict([data])  # Simplified
    return jsonify({"pattern": prediction[0]})

@app.route('/chatbot', methods=['POST'])
def chatbot():
    # Placeholder chatbot model
    user_message = request.json['message']
    response = f"Simulated response for: {user_message}"
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
