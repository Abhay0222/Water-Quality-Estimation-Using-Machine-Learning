from flask import Flask, render_template, request
import joblib
import numpy as np

app = Flask(__name__)

model = joblib.load('water_quality_model.pkl')

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    form_data = {}

    if request.method == 'POST':
        # SAFELY get form inputs
        form_data['ph'] = request.form.get('ph')
        form_data['hardness'] = request.form.get('hardness')
        form_data['solids'] = request.form.get('solids')
        form_data['chloramines'] = request.form.get('chloramines')
        form_data['sulfate'] = request.form.get('sulfate')
        form_data['conductivity'] = request.form.get('conductivity')
        form_data['organic_carbon'] = request.form.get('organic_carbon')
        form_data['trihalomethanes'] = request.form.get('trihalomethanes')
        form_data['turbidity'] = request.form.get('turbidity')

        # ✅ Now build the input array CORRECTLY
        input_data = np.array([[
            float(form_data['ph']),
            float(form_data['hardness']),
            float(form_data['solids']),
            float(form_data['chloramines']),
            float(form_data['sulfate']),
            float(form_data['conductivity']),
            float(form_data['organic_carbon']),
            float(form_data['trihalomethanes']),
            float(form_data['turbidity'])
        ]])

        prediction = model.predict(input_data)[0]

        if prediction == 1:
            result = "✅ Water is POTABLE (Safe to drink)."
        else:
            result = "🚫 Water is NOT POTABLE (Unsafe to drink)."

    return render_template('index.html', result=result, form_data=form_data)

if __name__ == '__main__':
    app.run(debug=True)
# app.py - Flask application for water quality prediction
# Uses a pre-trained model to predict water potability based on user input
# The model is loaded from a .pkl file and predictions are made based on form data