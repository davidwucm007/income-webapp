#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import flask
import pickle
import numpy as np


app = flask.Flask(__name__, template_folder='templates')
    
# prediction function 
def ValuePredictor(to_predict_list): 
    to_predict = np.array(to_predict_list).reshape(1, 8) 
    loaded_model = pickle.load(open("model/income_model_gboost.pkl", "rb")) 
    result = loaded_model.predict(to_predict)
    return to_predict, result[0] 

@app.route('/', methods = ['GET','POST']) 
def main(): 
    if flask.request.method == 'GET':
        # Just render the initial form, to get input
        return(flask.render_template('main.html'))
    if flask.request.method == 'POST': 
        to_predict_list = flask.request.form.to_dict() 
        to_predict_list = list(to_predict_list.values()) 
        to_predict_list = list(map(int, to_predict_list)) 
        to_predict, result = ValuePredictor(to_predict_list)         
        if int(result)== 1: 
            prediction ='Income more than 50K'
        else: 
            prediction ='Income less that 50K'            
        return flask.render_template("main.html", original_input={'Age':to_predict[0][0],
                                                     'Education':to_predict[0][1],
                                                     'Marital status':to_predict[0][2],
                                                     'Occupation':to_predict[0][3],
                                                     'Gender':to_predict[0][4],
                                                     'Capital gain':to_predict[0][5],
                                                     'Capital loss':to_predict[0][6],
                                                     'Hours per week':to_predict[0][7]}, prediction = prediction)


    

if __name__ == '__main__':
    app.run()