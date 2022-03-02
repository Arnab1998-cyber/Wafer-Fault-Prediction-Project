from flask import Flask,request,render_template,Response
from flask_cors import CORS,cross_origin
import json
import shutil
from training_pipeline import training_pipeline
from prediction_pipeline import prediction


app=Flask(__name__)

@app.route('/',methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
@cross_origin()
def prediction_route():
    try:
        train=request.form['test_file']
        pred=request.form['prediction_file']
        training_file_path='Training_Batch_Files'
        prediction_file_path='Prediction_Batch_Files'
        train=training_pipeline(training_files=train)
        columns_to_drop=train.trainig_pipeline()
        predict=prediction(prediction_files=pred)
        result,outcome_file_path=predict.get_prediction(columns_to_drop=columns_to_drop)
        print('result is ', result)
        print('path to full result ',outcome_file_path)
        return render_template('results.html', file_path=outcome_file_path, predictions=json.loads(result))
    except Exception as e:
        print(e)
        return 'something went wrong'


if __name__=='__main__':
    app.run()