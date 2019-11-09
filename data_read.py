# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 23:28:44 2019

@author: Inderdeep
"""


import pandas as pd
import numpy as np
from sklearn import preprocessing 

class DataRead :

    
 temp_list=[]
 l0=[]
 l1=[]
 l2=[]
 l3=[]
 l4=[]
 l5=[]
 l6=[]
 l7=[]
 
 def reset(self):
  self.temp_list=[]
  self.l0=[]
  self.l1=[]
  self.l2=[]
  self.l3=[]
  self.l4=[]
  self.l5=[]
  self.l6=[]
  self.l7=[]

 def startEndData(self):
    
  #file = open('DATA\\AdmissionsCorePopulatedTable.txt','r')

  file = open('AdmissionsCorePopulatedTable.txt','r')
  file.readline()

  self.reset()
  for str in file:
    
    try:
     self.temp_list = file.readline().split()
     print(self.temp_list)
     self.l0.append(self.temp_list[0])
     #l1.append(temp_list.split()[1])
     self.l2.append(self.temp_list[2])
     self.l3.append(self.temp_list[3])
     self.l4.append(self.temp_list[4])
     self.l5.append(self.temp_list[5])
    except:
      print("Error :",self.temp_list)
    
  data={'Patient_ID':self.l0,'AS_Date':self.l2,'AS_time':self.l3,'AE_Date':self.l4,'AE_time':self.l5} 

  data = pd.DataFrame(data)
 
  #print(data)

  return(data)
 
 def diagnosisCorePopuTab(self) :
  #file = open('DATA\\AdmissionsDiagnosesCorePopulatedTable.txt','r')
  file = open('AdmissionsDiagnosesCorePopulatedTable.txt','r')
  file.readline()
 
  self.reset()  
  for str in file:
   
   try:    
    self.temp_list = file.readline().split()
    self.l0.append(self.temp_list[0])
    self.l1.append(self.temp_list[1])
    self.l2.append(self.temp_list[2])
    self.l3.append(" ".join(self.temp_list[3:]))      
   except:
       continue
   
  data={'Patient_ID':self.l0,'AD_ID':self.l1,'Dignoses_code':self.l2,'Description':self.l3} 
 
  data = pd.DataFrame(data)
      
   # print(data)
  return(data)

 def patientCorePopuTab(self) :
  #file = open('DATA\\PatientCorePopulatedTable.txt','r')
  file = open('PatientCorePopulatedTable.txt','r')
    
  file.readline()
 
  self.reset()  
  for str in file:
    
   try:   
    self.temp_list = file.readline().split()
    self.l0.append(self.temp_list[0])
    self.l1.append(self.temp_list[1])
    self.l2.append(self.temp_list[2])
    self.l3.append(self.temp_list[3])
    self.l4.append(self.temp_list[4])
    self.l5.append(self.temp_list[5])
    self.l6.append(self.temp_list[6])
    self.l7.append(self.temp_list[7])
   except:
      print("Error : "+self.temp_list)  
    
  data={'Patient_ID':self.l0,'P_gender':self.l1,'PDOB_Date':self.l2,'PDOB_Time':self.l3,'P_Race':self.l4,'P_MartialStatus':self.l5,'P_Lang':self.l6,'Poverty':self.l7} 

  data = pd.DataFrame(data)
  #print(data)
  return(data)
 


    
def main():
     pass

if __name__=="__main__":
    main()