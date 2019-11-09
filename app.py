from flask import Flask,request,render_template,make_response,json,Response
from flask_restful import Resource, Api,reqparse 
import flask_restful as restful
from input_request import InputRequest 
from flask_ngrok import run_with_ngrok

app = Flask(__name__)
api = restful.Api(app)


parser = reqparse.RequestParser()

@app.before_first_request
def _settingUpModel():
    
   from data_read import DataRead
   from data_engg import DataEngg
   from model_train import ModelTrain
   from input_request import InputRequest
   
   global data,model,nlp,data1,data2,data3
   
   data = DataRead()
   
   de = DataEngg()
   
   ml = ModelTrain()
   
   data1=de.startEnd(data.startEndData())

   data2=de.patientCore(data.patientCorePopuTab())
   
   data3=de.diagnosis(data.diagnosisCorePopuTab())
   
   elixir = de.merge_data(data1,data2,data3)
   
   model=ml.los_train(elixir)
   
   nlp=ml.nlp_train(data3)
   
@app.route('/') 
def index():
 return render_template('index.html')
 #return "my Server is working"


class Results(Resource):
 def get(self):
    return {
            'Inderdeep':{
                         'name':['Inter at mirketa']
                        } 
           }
            
 def post(self):
     if request.headers['Content-type']=="application/json":
     
        json_data=request.get_json()
        
        req = InputRequest()
        request_elixir = req.inputJSON(json_data,data3,nlp)
        
        los_predictions = model.predict(request_elixir)
        
        i=0
        
        temp=[]
        for x in json_data :
            t = json_data.get(x)['uid']
            print(type(t))
            dic={}
            dic[t]=los_predictions[i]
            temp.append(dic)
            i=i+1
            
        return(json.dumps(temp))

class LosFrontEnd(Resource):
 def get(self):
    return {
            'Inderdeep':{
                         'name':['Inter at mirketa']
                        } 
           }
                 
api.add_resource(Results,'/api')