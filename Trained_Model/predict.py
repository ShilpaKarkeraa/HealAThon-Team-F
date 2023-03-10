from flask import Flask, render_template, request
from flask import make_response
import pandas as pd
import pickle
import js2py

app = Flask(__name__, template_folder='templates/')

# load the saved model
filename = 'CKD_Model.sav'
loaded_model = pickle.load(open(filename, 'rb'))

# define a route for the web app
@app.route('/')
def home():
	return render_template('home.html')


# define a route to handle form submission
@app.route('/', methods=['GET', 'POST'])
def predict():
	if request.method == 'POST':
		# get the user input from the form
		age = request.form['age']
		bp = request.form['blood_pressure']
		sg = request.form['specific_gravity']
		al = request.form['albumin']
		su = request.form['sugar']
		rbc = request.form['red_blood_cells']
		pc = request.form['pus_cell']
		pcc = request.form['pus_cell_clumps']
		ba = request.form['bacteria']
		bgr = request.form['blood_glucose_random']
		bu = request.form['blood_urea']
		sc = request.form['serum_creatinine']
		sod = request.form['sodium']
		pot = request.form['potassium']
		hemo = request.form['hemoglobin']
		pcv = request.form['packed_cell_volume']
		wc = request.form['white_blood_cell_count']
		rc = request.form['red_blood_cell_count']
		htn = request.form['hypertension']
		dm = request.form['diabetes_mellitus']
		cad = request.form['coronary_artery_disease']
		appet = request.form['appetite']
		pe = request.form['peda_edema']
		ane = request.form['anemia']
		
		# check if any required field is empty
		required_fields = ['age', 'blood_pressure', 'specific_gravity', 'albumin', 'sugar',
						'blood_glucose_random', 'blood_urea', 'serum_creatinine', 'sodium',
						'potassium', 'hemoglobin', 'packed_cell_volume', 'white_blood_cell_count',
						'red_blood_cell_count']
		for field in required_fields:
			if not request.form.get(field):
				error_message = f"Error: {field} field is required"
				return render_template('result.html', prediction=error_message)


		# create a DataFrame with the user input
		user_input = pd.DataFrame({'age': [float(age)], 'blood_pressure': [float(bp)],
								'specific_gravity': [float(sg)], 'albumin': [float(al)], 
								'sugar': [float(su)], 'red_blood_cells': [float(rbc)], 'pus_cell': [float(pc)],
								'pus_cell_clumps': [float(pcc)], 'bacteria': [float(ba)], 'blood_glucose_random': [float(bgr)],
								'blood_urea': [float(bu)], 'serum_creatinine': [float(sc)], 'sodium': [float(sod)], 
								'potassium': [float(pot)], 'hemoglobin': [float(hemo)], 'packed_cell_volume': [float(pcv)], 
								'white_blood_cell_count': [float(wc)], 'red_blood_cell_count': [float(rc)], 'hypertension': [float(htn)], 
								'diabetes_mellitus': [float(dm)], 'coronary_artery_disease': [float(cad)], 'appetite': [float(appet)], 
								'peda_edema': [float(pe)], 'anemia': [float(ane)]})
		prediction = loaded_model.predict(user_input)[0]
		if prediction == 1:
			prediction_label = 'CKD'
		else:
			prediction_label = 'Not CKD'

		# render the result page with the prediction
		return render_template('result.html', prediction=prediction_label)
	# Render home page
	return render_template('home.html')

if __name__ == '__main__':
	app.run(debug=True, use_reloader=False, port=8080)