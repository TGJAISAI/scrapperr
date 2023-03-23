import requests
import pandas as pd
import numpy as np
import json
import xlsxwriter

u1="https://www.nmc.org.in/MCIRest/open/getPaginatedData?service=getPaginatedDoctor&draw=1&columns%5B0%5D%5Bdata%5D=0&columns%5B0%5D%5Bname%5D=&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=true&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=1&columns%5B1%5D%5Bname%5D=&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=true&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=2&columns%5B2%5D%5Bname%5D=&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=true&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=3&columns%5B3%5D%5Bname%5D=&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=true&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=4&columns%5B4%5D%5Bname%5D=&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=true&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=5&columns%5B5%5D%5Bname%5D=&columns%5B5%5D%5Bsearchable%5D=true&columns%5B5%5D%5Borderable%5D=true&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B6%5D%5Bdata%5D=6&columns%5B6%5D%5Bname%5D=&columns%5B6%5D%5Bsearchable%5D=true&columns%5B6%5D%5Borderable%5D=true&columns%5B6%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B6%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=0&order%5B0%5D%5Bdir%5D=asc&start="
u2="&length=500&search%5Bvalue%5D=&search%5Bregex%5D=false&name=&registrationNo=&smcId=36&year=&_=1676354340048"



main_df=pd.DataFrame()



for j in range(0,35):
  try:
    df = pd.DataFrame()
    print('we are on page.... %s' %j)
    end_url = u1+str(j*500)+u2
    res = requests.get(end_url)
    js = res.json()
    data = js['data']
    data_df=pd.DataFrame(data, columns=['No','year','id','state','first name','name','code'])
    data_df=data_df.reset_index()
    c=0
  except:
    print('exception.....')
  for ele in data_df['code']:
    try:
      ele=ele.replace('<a href="javascript:void(0);" onclick="openDoctorDetailsnew(',' ')
      ele=ele.replace(')">View</a>',' ')
      ele=ele.replace("'",'')
      data_df['code'][c]=ele.strip()
      data_df[['idno','regno']]=data_df['code'].str.split(',',expand=True)
      data_df['regno']=data_df['regno'].str.strip()
      # data_df.drop(['code'], axis=1,inplace=True)
      c=c+1
    except:
      print('exception...')
  df = df.append(data_df)
  url="https://www.nmc.org.in/MCIRest/open/getDataFromService?service=getDoctorDetailsByIdImr"
  for i in range(len(df['idno'])):
    print('page number..%s index number... %s' %(j,i))
    try:
      payload={"doctorId": df['idno'][i], "regdNoValue": df['regno'][i]}
      res=requests.post(url, json=payload)
      js = res.json()
      new = pd.DataFrame.from_dict([js])
      new=new.dropna(axis=1)
      main_df=main_df.append(new)
    except:
      print('exception....')
  writer = pd.ExcelWriter('madras.xlsx', engine="openpyxl", mode="a", if_sheet_exists="overlay",)
  main_df.to_excel(writer, index=False, sheet_name = 'madras')
  writer.save()
  