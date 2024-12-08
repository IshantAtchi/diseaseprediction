from flask import Flask, render_template, request
from tabulate import tabulate

app = Flask(__name__)
app.run(host="0.0.0.0", port=8080)
app.secret_key = 'your_secret_key'

# Disease detection logic
def detect_diseases(data):
    at_risk = []
    possibly_at_risk = []
    not_detected = []

    if data.get("systolic_bp") > 140 or data.get("diastolic_bp") > 90:
        at_risk.append("Hypertension (High BP) - a risk factor for heart disease and stroke")
    else:
        not_detected.append("Hypertension (High BP)")

    if data.get("fasting_glucose") > 125 or data.get("hba1c") > 6.5:
        at_risk.append("Diabetes - a risk factor for multiple complications")
    elif 100 < data.get("fasting_glucose") <= 125 or 5.7 <= data.get("hba1c") <= 6.5:
        possibly_at_risk.append("Diabetes - prediabetes stage detected")
    else:
        not_detected.append("Diabetes")

    if data.get("cholesterol") > 240:
        at_risk.append("Hypercholesterolemia - linked to heart disease")
    elif 200 < data.get("cholesterol") <= 240:
        possibly_at_risk.append("Hypercholesterolemia - borderline levels detected")
    else:
        not_detected.append("Hypercholesterolemia")

    if data.get("bmi") > 30:
        at_risk.append("Obesity - a risk factor for various diseases")
    elif 25 <= data.get("bmi") <= 30:
        possibly_at_risk.append("Overweight - approaching obesity")
    else:
        not_detected.append("Obesity")

    if data.get("age") > 50 and data.get("smoking_status") == "yes":
        at_risk.append("Chronic Obstructive Pulmonary Disease (COPD)")
    else:
        not_detected.append("Chronic Obstructive Pulmonary Disease (COPD)")

    if data.get("family_history_cancer") == "yes" and data.get("smoking_status") == "yes":
        at_risk.append("Cancer - higher risk due to lifestyle and family history")
    else:
        not_detected.append("Cancer")

    if data.get("age") > 60 and data.get("smoking_status") == "yes" and data.get("cholesterol") > 240:
        at_risk.append("Heart Disease")
    else:
        not_detected.append("Heart Disease")

    if data.get("kidney_function") < 60:
        at_risk.append("Chronic Kidney Disease")
    elif 60 <= data.get("kidney_function") < 90:
        possibly_at_risk.append("Chronic Kidney Disease - mildly reduced function")
    else:
        not_detected.append("Chronic Kidney Disease")

    if data.get("smoking_status") == "yes" or data.get("air_pollution_exposure") == "yes":
        possibly_at_risk.append("Lower Respiratory Infections or Respiratory Disease")
    else:
        not_detected.append("Lower Respiratory Infections or Respiratory Disease")

    if data.get("immunization_status") == "no":
        at_risk.append("Preventable Infectious Diseases")
    else:
        not_detected.append("Preventable Infectious Diseases")

    return at_risk, possibly_at_risk, not_detected

# Flask routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    health_data = {
        "age": int(request.form.get("age", 0)),
        "systolic_bp": int(request.form.get("systolic_bp", 0)),
        "diastolic_bp": int(request.form.get("diastolic_bp", 0)),
        "fasting_glucose": float(request.form.get("fasting_glucose", 0)),
        "hba1c": float(request.form.get("hba1c", 0)),
        "cholesterol": float(request.form.get("cholesterol", 0)),
        "bmi": float(request.form.get("bmi", 0)),
        "kidney_function": float(request.form.get("kidney_function", 0)),
        "smoking_status": request.form.get("smoking_status", "no").lower(),
        "family_history_cancer": request.form.get("family_history_cancer", "no").lower(),
        "air_pollution_exposure": request.form.get("air_pollution_exposure", "no").lower(),
        "immunization_status": request.form.get("immunization_status", "yes").lower(),
    }
    at_risk, possibly_at_risk, not_detected = detect_diseases(health_data)

    # Format data for rendering
    table = []
    for disease in at_risk:
        table.append([disease, "At Risk"])
    for disease in possibly_at_risk:
        table.append([disease, "Possibly At Risk"])
    for disease in not_detected:
        table.append([disease, "Not Detected"])

    return render_template('result.html', table=table)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
