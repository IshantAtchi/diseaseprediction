from flask import Flask, render_template, request

app = Flask(__name__)

# Route to display the index page (the form)
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle form submission and display results
@app.route('/result', methods=['POST'])
def result():
    # Collect user input from the form
    age = int(request.form['age'])
    systolic_bp = int(request.form['systolic_bp'])
    diastolic_bp = int(request.form['diastolic_bp'])
    fasting_glucose = float(request.form['fasting_glucose'])
    hba1c = float(request.form['hba1c'])
    cholesterol = int(request.form['cholesterol'])
    bmi = float(request.form['bmi'])
    kidney_function = int(request.form['kidney_function'])
    smoking_status = request.form['smoking_status']
    family_history_cancer = request.form['family_history_cancer']
    air_pollution_exposure = request.form['air_pollution_exposure']
    immunization_status = request.form['immunization_status']

    # Diseases list with rules for risk calculation
    diseases = [
        {"Disease": "Heart disease", "Status": calculate_heart_disease_risk(age, systolic_bp, diastolic_bp, cholesterol, smoking_status)},
        {"Disease": "Cancer", "Status": calculate_cancer_risk(age, family_history_cancer, smoking_status)},
        {"Disease": "Chronic lower respiratory diseases", "Status": calculate_respiratory_risk(smoking_status, age, air_pollution_exposure)},
        {"Disease": "Stroke", "Status": calculate_stroke_risk(systolic_bp, diastolic_bp, age)},
        {"Disease": "Alzheimer's disease", "Status": calculate_alzheimer_risk(age, kidney_function)},
        {"Disease": "Diabetes", "Status": calculate_diabetes_risk(fasting_glucose, hba1c, age)},
        {"Disease": "Kidney disease", "Status": calculate_kidney_risk(kidney_function, age)},
        {"Disease": "Flu and pneumonia", "Status": calculate_flu_risk(immunization_status, age)},
        {"Disease": "Liver disease", "Status": calculate_liver_disease_risk(bmi, alcohol_use="no")},  # Modify as needed
        {"Disease": "Blood poisoning", "Status": calculate_blood_poisoning_risk(family_history_cancer, age)},
        {"Disease": "Cardiovascular disease", "Status": calculate_cardiovascular_risk(age, systolic_bp, diastolic_bp, cholesterol)},
        {"Disease": "Respiratory infections", "Status": calculate_respiratory_infection_risk(smoking_status, age)},
        {"Disease": "Chronic obstructive pulmonary disease (COPD)", "Status": calculate_copd_risk(smoking_status, age)},
        {"Disease": "Arthritis", "Status": calculate_arthritis_risk(age, bmi)},
    ]

    # Sort diseases by risk status: "At Risk" first, "Possibly at Risk" second, and "Not Detected" last
    risk_order = {"At Risk": 0, "Possibly at Risk": 1, "Not Detected": 2}
    diseases.sort(key=lambda x: risk_order.get(x["Status"], 2))  # Sort by the numerical value of the risk status

    return render_template('result.html', table=diseases)


# Risk Calculation Functions
def calculate_heart_disease_risk(age, systolic_bp, diastolic_bp, cholesterol, smoking_status):
    if age > 60 or systolic_bp > 160 or diastolic_bp > 100 or cholesterol > 240 or smoking_status == "yes":
        return "At Risk"
    elif age > 45 or (systolic_bp > 140 or diastolic_bp > 90) or cholesterol > 200:
        return "Possibly at Risk"
    return "Not Detected"

def calculate_cancer_risk(age, family_history, smoking_status):
    if family_history == "yes" or smoking_status == "yes" or age > 50:
        return "At Risk"
    elif age > 40 or smoking_status == "yes":
        return "Possibly at Risk"
    return "Not Detected"

def calculate_respiratory_risk(smoking_status, age, air_pollution_exposure):
    if smoking_status == "yes" or age > 60 or air_pollution_exposure == "yes":
        return "At Risk"
    elif age > 45 or smoking_status == "yes":
        return "Possibly at Risk"
    return "Not Detected"

def calculate_stroke_risk(systolic_bp, diastolic_bp, age):
    if systolic_bp > 160 or diastolic_bp > 100 or age > 70:
        return "At Risk"
    elif systolic_bp > 140 or diastolic_bp > 90:
        return "Possibly at Risk"
    return "Not Detected"

def calculate_alzheimer_risk(age, kidney_function):
    if age > 70 or kidney_function < 60:
        return "At Risk"
    elif age > 65 or kidney_function < 70:
        return "Possibly at Risk"
    return "Not Detected"

def calculate_diabetes_risk(fasting_glucose, hba1c, age):
    if fasting_glucose > 125 or hba1c > 6.5 or age > 50:
        return "At Risk"
    elif fasting_glucose > 100 or hba1c > 5.7:
        return "Possibly at Risk"
    return "Not Detected"

def calculate_kidney_risk(kidney_function, age):
    if kidney_function < 60 or age > 65:
        return "At Risk"
    elif kidney_function < 75 or age > 50:
        return "Possibly at Risk"
    return "Not Detected"

def calculate_flu_risk(immunization_status, age):
    if immunization_status == "no" or age > 65:
        return "At Risk"
    elif age > 50:
        return "Possibly at Risk"
    return "Not Detected"

def calculate_liver_disease_risk(bmi, alcohol_use):
    if bmi > 30 or alcohol_use == "yes":
        return "At Risk"
    elif bmi > 25 or alcohol_use == "no":
        return "Possibly at Risk"
    return "Not Detected"

def calculate_blood_poisoning_risk(family_history_cancer, age):
    if family_history_cancer == "yes" or age > 60:
        return "At Risk"
    elif family_history_cancer == "yes":
        return "Possibly at Risk"
    return "Not Detected"

def calculate_cardiovascular_risk(age, systolic_bp, diastolic_bp, cholesterol):
    if age > 50 or systolic_bp > 160 or diastolic_bp > 100 or cholesterol > 240:
        return "At Risk"
    elif age > 45 or systolic_bp > 140 or diastolic_bp > 90 or cholesterol > 200:
        return "Possibly at Risk"
    return "Not Detected"

def calculate_respiratory_infection_risk(smoking_status, age):
    if smoking_status == "yes" or age > 65:
        return "At Risk"
    elif age > 50:
        return "Possibly at Risk"
    return "Not Detected"

def calculate_copd_risk(smoking_status, age):
    if smoking_status == "yes" or age > 60:
        return "At Risk"
    elif smoking_status == "yes":
        return "Possibly at Risk"
    return "Not Detected"

def calculate_arthritis_risk(age, bmi):
    if age > 60 or bmi > 30:
        return "At Risk"
    elif age > 50 or bmi > 25:
        return "Possibly at Risk"
    return "Not Detected"


if __name__ == '__main__':
    app.run(debug=True)
