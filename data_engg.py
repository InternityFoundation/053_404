# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 12:02:14 2019

@author: Inderdeep
"""
from datetime import datetime
from datetime import time
import pandas as pd
from sklearn import preprocessing
import nltk
from nltk.tokenize import word_tokenize
import string
import nltk as nltk
import math



from data_read import DataRead

class DataEngg:
    
    def startEnd(self,df):

        #print(df.head())
      
        days=[]
        end=[]
        start=[]
        los=[]

        def time(str):
         temp = str.split(":")
         print(temp)
    
        #subtracting for LOS
        temp=df['AE_Date'].count()

        for i in range(0,temp) :
          d1=df['AS_Date'][i] 
          d2=df['AE_Date'][i]
          d1=datetime.strptime(d1, '%Y-%m-%d')
           
          start.append(d1)
          d2=datetime.strptime(d2, '%Y-%m-%d')
          end.append(d2)
          d=d2-d1
          los.append(d) 
      
        
        for i in los:
         days.append(i.days)
    
    
        temp = {'Patient_ID':df['Patient_ID'],'Start':start , 'End':end , 'days':los}
        plotFrame = pd.DataFrame(temp)
       
        temp = {'Start':start , 'End':end , 'days':days}     
        plotFrame = pd.DataFrame(temp)
        
        plotFrame.insert(0,"Patient_ID",df['Patient_ID'],True)

        return(plotFrame)
        
    def patientCore(self,patientFrame):
          
          temp=[]
          
          for i in patientFrame['P_gender'] :
  
           if i=='Male':
             temp.append(1) 
           elif i=="Female" :
             temp.append(2)
           else:
             temp.append(0)
             
             
          # dropping some columns
          patientFrame.drop(['P_gender'],axis=1,inplace=True)

          patientFrame.insert(1,"Gender",temp,True)

          patientFrame


          #ENCODING 
          label_encoder = preprocessing.LabelEncoder() 
  
          patientFrame['P_Race'] = label_encoder.fit_transform(patientFrame['P_Race'])
          patientFrame['P_MartialStatus'] = label_encoder.fit_transform(patientFrame['P_MartialStatus'])
          patientFrame['P_Lang'] = label_encoder.fit_transform(patientFrame['P_Lang'])


          patientFrame


          patientFrame['Poverty'] = patientFrame['Poverty'].replace(to_replace ='English|Icelandic|Spanish|Unknown', value = '0', regex = True) 

          patientFrame['Poverty']
 

          patientFrame['Poverty']=patientFrame['Poverty'].astype('float')
      
          # replacing zero
          patientFrame['Poverty'] = patientFrame['Poverty'].replace(to_replace =0, value =patientFrame['Poverty'].mean() , regex = True) 


          #AGE
          i=0

          for x in patientFrame['PDOB_Date'] :
           patientFrame['PDOB_Date'][i] = datetime.strptime(x,'%Y-%m-%d')
           i+=1
           
          return patientFrame 


    def diagnosis(self,data):
        print("__________ NLTK ______")
        
        data_list=[]
        
        nltk.download('punkt')
        nltk.download('stopwords')
        
        for i in data["Description"]:
          str=""  
          i=word_tokenize(i)
          #fd = nltk.FreqDist(i)

          i = [w.lower() for w in i] #lower
  
          table = str.maketrans('', '', string.punctuation)
          stripped = [w.translate(table) for w in i]
  
          # remove remaining tokens that are not alphabetic
          words = [word for word in stripped if word.isalpha()]
  
          # filter out stop words
  
          from nltk.corpus import stopwords
          stop_words = set(stopwords.words('english')) 
          words = [w for w in words if not w in stop_words]
          data_list.append(words)
          
          
        Di_code=[]
       
        for i in range(0,len(data)):
          Di_code.append(data["Dignoses_code"][i][0])
          
        Di_series=pd.Series(Di_code)
        
        Train_Df = pd.DataFrame()

        temp=[]
        
        str=" "

        for i in data_list:
         temp.append(str.join(i))
  
        encoder = preprocessing.LabelEncoder()

        Di_series = encoder.fit_transform(Di_series)

    
        Train_Df["text"]=temp
        Train_Df["label"]=Di_series

        Train_Df.insert(0,"Patient_ID",data['Patient_ID'],True)
        
        return Train_Df
            
    def merge_data(self,data1,data2,data3):

      elixire=pd.merge(data1,data2,on="Patient_ID",how="inner")
      elixire=pd.merge(elixire,data3,on="Patient_ID",how="inner")

      #AGE calculating
      age=[]

      for i in range(0,len(elixire)) :
         age.append(((elixire['Start'][i]-elixire['PDOB_Date'][i])/365).days)


      #print(age)


      elixire.insert(5,"Age",age,True)

      # removing NaN
      #print(elixire["Age"].mean())

      for i in range(0,len(elixire)) :
       if math.isnan(elixire["Age"][i]):
        elixire["Age"][i]=elixire["Age"].mean()
     
      elixire["Age"]

      # converting into days and month
      day=[]
      month=[]
      year=[]

      for x in elixire["Start"] :
       day.append(x.day)
       month.append(x.month)
       year.append(x.year)
  
  
      #putting into the df
      elixire.insert(1,"SDay",day,True)
      elixire.insert(2,"Smonth",month,True)
      elixire.insert(3,"SYear",year,True)

      elixire.drop("Start",axis=1,inplace=True) 
      elixire.drop("PDOB_Time",axis=1,inplace=True) 
      elixire.drop("PDOB_Date",axis=1,inplace=True) 

 
      elixire  

      #dropping end
      elixire.drop("End",axis=1,inplace=True)
      #droping ID
      elixire.drop("Patient_ID",axis=1,inplace=True)
      elixire

      elixire.dtypes

      #changing to LOS
      LOS=[]
      
      for i in elixire["days"]:
        LOS.append(i)

      elixire.insert(4,"LOS",LOS,True)
      elixire.drop(["days"],axis=1,inplace=True)

      LOS=[]

      for i in day:
       if isinstance(i,int):
        LOS.append(i)
       else:
        LOS.append(0)
    
    
      elixire.insert(3,'LOSDAY',LOS,True)
      elixire.drop("LOS",axis=1,inplace=True)
      elixire.drop("text",axis=1,inplace=True)
      elixire.dtypes    
  

      return elixire
