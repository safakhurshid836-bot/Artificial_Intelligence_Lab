from flask import Flask, render_template, request
import numpy as np
import pickle

app = Flask(__name__)

# Load Model
model = pickle.load(open('models/rf_model.pkl', 'rb'))

# Label Decoder
reverse_map = {
    0: "FALSE POSITIVE",
    1: "CONFIRMED"
}


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():

    try:

        features = [
            float(request.form['koi_period']),
            float(request.form['koi_duration']),
            float(request.form['koi_depth']),
            float(request.form['koi_prad']),
            float(request.form['koi_teq']),
            float(request.form['koi_insol']),
            float(request.form['koi_model_snr']),
            float(request.form['koi_steff']),
            float(request.form['koi_slogg']),
            float(request.form['koi_srad']),
            float(request.form['koi_kepmag'])
        ]

        X = np.array([features])

        prediction = model.predict(X)

        result = reverse_map[prediction[0]]

        return render_template(
            'index.html',
            prediction_text=f'Prediction: {result}'
        )

    except Exception as e:

        return render_template(
            'index.html',
            prediction_text=f'Error: {str(e)}'
        )


if __name__ == '__main__':
    app.run(debug=True)