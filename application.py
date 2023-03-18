##for deploying the app we have to name it application and have to follow specific instruction regarding the python config
from flask import Flask,request,render_template
import numpy as np
import pandas as pd

from src.logger import logging
from sklearn.preprocessing import StandardScaler
from src.pipeline.predict_pipeline import CustomData,PredictPipeline
application = Flask(__name__)   ##this give entry point for the app

app = application

##route for a home page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predictdata',methods=['GET','POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        data = CustomData(
            gender = str(request.form.get('gender')),
            race_ethnicity = str(request.form.get('race_ethnicity')),
            parental_level_of_education = str(request.form.get('parental_level_of_education')),
            lunch = str(request.form.get('lunch')),
            test_preparation_course = str(request.form.get('test_preparation_course')),
            reading_score = float(request.form.get('reading_score')),
            writing_score = float(request.form.get('writing_score'))
            )
        pred_df = data.get_data_as_data_frame()
        predict_pipeline = PredictPipeline()
        results = predict_pipeline.predict(pred_df)
        logging.info('The selected features are {0} and prediction is : {1}'.format(pred_df,results[0]))
        return render_template('home.html',results=results[0])
    


if __name__=="__main__":
    app.run(host='0.0.0.0')    #we have to remove debug = true before deployment