# import the necessary packages
import flask, render_template, redirect, url_for, request,session,Response
from werkzeug import secure_filename
import os
#from supportFile import *
import pickle
from sms import sendSMS
import sqlite3
from datetime import datetime
import pandas as pd

app = Flask(__name__)

app.secret_key = '1234'
app.config["CACHE_TYPE"] = "null"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/', methods=['GET', 'POST'])
def landing():
	return render_template('home.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
	return render_template('home.html')


@app.route('/input', methods=['GET', 'POST'])
def input():
	if request.method == 'POST':
		if request.form['sub']=='Upload':
			savepath = r'upload/'
			dataset = request.files['dataset']
			dataset.save(os.path.join(savepath,(secure_filename('dataset.csv'))))
			return render_template('input.html',mgs="Dataset Uploaded..!!!")

	return render_template('input.html')		

@app.route('/dataset', methods=['GET', 'POST'])
def dataset():
	df = pd.read_csv('upload/dataset.csv')
	return render_template('dataset.html', tables=[df.to_html(classes='w3-table-all w3-hoverable')], titles=df.columns.values)

@app.route('/clean', methods=['GET', 'POST'])
def clean():
	df = pd.read_csv('upload/dataset.csv')
	df.drop(['id_str', 'screen_name', 
                    'location', 'description', 
                    'url', 'created_at', 
                    'lang', 'status',
                    'default_profile',
                    'default_profile_image',
                    'has_extended_profile','name'],axis=1,inplace=True)

	return render_template('clean.html', tables=[df.to_html(classes='w3-table-all w3-hoverable')], titles=df.columns.values)


# No caching at all for API endpoints.
@app.after_request
def add_header(response):
	# response.cache_control.no_store = True
	response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
	response.headers['Pragma'] = 'no-cache'
	response.headers['Expires'] = '-1'
	return response


if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True, threaded=True)
