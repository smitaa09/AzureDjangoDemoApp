'''Calling all the apis here'''
import re
import csv
import os
import json
from datetime import date
from dateutil.relativedelta import relativedelta
from django.db import connection
import pandas as pd
import numpy
from multiprocessing import Lock, Process
from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User,auth
from django.conf import settings
from django.contrib.sessions.models import Session
from django.views.decorators.cache import never_cache


path_dir= os.path.abspath(os.path.dirname(__file__))
#FILE_NAME= r"\Files\\Customer Sentiments Data.xlsx"
TODAY = str(date.today())

class AccessDatabase():

    sp_get_customer_sentiment_six_month='GetCustomerSentimentSixMonthData'
    sp_get_customer_sentiment='GetCustomerSentimentData'
    sp_get_focal_sentiment='GetFocalSentimentData'
    sp_get_supportfocal_six_month = 'GetFocalSentimentSixMonthData'
    sp_get_appnames = 'GetAppNames'
    sp_save_content = 'save_content'
    sp_save_training ='save_training'
    sp_save_suggestion = 'save_suggestion'
    sp_save_aion_feedback= 'save_aion_feedback'
    sp_save_feedback = 'Savefeedback'
    sp_save_userLogs = 'SaveUserLogs'
    
    def __init__(self):
        return None

    def database_connection_string(self,sp_name,sp_param1):
        self.sp_name= sp_name
        self.sp_param1= sp_param1
        cursor= connection.cursor()
        cursor.execute("exec " + sp_name + "'" + sp_param1 + "'" )
        return cursor

    def database_connection_string_withoutparam(self,sp_name):
        self.sp_name= sp_name
        cursor= connection.cursor()
        cursor.execute("exec " + sp_name)
        return cursor

        
api_view(["GET"])
@csrf_exempt
@never_cache
def get_supportfocal_six_month_details(request):       
    '''API to get support focal six months details'''
    if request.session.get('username') is not None:
        username=request.session.get('username')
    else:
        text_details = {"responseMessage": "Session expired"}
        return JsonResponse(text_details,safe=False)
    user_logs("get_supportfocal_six_month_details Started",username,'Support focal Details','1')
    customer_name=request.GET.get('supportengineer')
    access_db= AccessDatabase()
    cursor= access_db.database_connection_string(access_db.sp_get_supportfocal_six_month,customer_name)
    df_support_focal_six_month_list=[]
    columns=[column[0] for column in cursor.description]
    for rows in cursor.fetchall():
        df_support_focal_six_month_list.append({name:rows[i] for i, name in enumerate(columns)})
    user_logs("get_supportfocal_six_month_details Completed",username,'Support focal Details','0')
    return JsonResponse(df_support_focal_six_month_list,safe=False)

api_view(["POST"]) 
@csrf_exempt
@never_cache
def get_sentiment_details(request):
    '''Method to get Sentiment Details'''
    if request.session.get('username') is not   None:
        username=request.session.get('username')
    else:
        text_details = {"responseMessage": "Session expired"}
        return JsonResponse(text_details,safe=False)
    user_logs("Classify email content details Started",username,'customer Details','1')
    customer_name=json.loads(request.body)
    customer_details= get_customer_sentiment_details(customer_name)
    user_logs("Classify email content details Completed",username,'customer Details','0')
    return JsonResponse(customer_details,safe=False)

api_view(["POST"]) 
@csrf_exempt
@never_cache
def get_customer_six_month_details(request):        
    '''API to get support focal six months details'''
    if request.session.get('username') is not   None:
        username=request.session.get('username')
    else:
        text_details = {"responseMessage": "Session expired"}
        return JsonResponse(text_details,safe=False)
    user_logs("get_supportfocal_six_month_details Started",username,'customer Details','1')
    customer_name=json.loads(request.body)
    access_db= AccessDatabase()
    cursor= access_db.database_connection_string(access_db.sp_get_customer_sentiment_six_month,customer_name)
    df_customer_six_month_list=[]
    columns=[column[0] for column in cursor.description]
    for rows in cursor.fetchall():
        df_customer_six_month_list.append({name:rows[i] for i, name in enumerate(columns)})
    if df_customer_six_month_list is not None:
        return JsonResponse(df_customer_six_month_list,safe=False)
    else:
        return JsonResponse(False,safe=False)

def get_six_month_data_sample():
    '''Method to get Sentiment Details'''

    customer_name='Adam Epps'
    
    print('six month data')
    access_db= AccessDatabase()
    cursor= connection.cursor()
    cursor.execute("exec " + sp_name)
    cursor= access_db.database_connection_string(access_db.sp_get_customer_sentiment_six_month,customer_name)    
    ci_names = cursor.fetchall()
    print(f'cinames {ci_names}')
    for rows in ci_names:
        print("data:",rows[0])
    
    cursor.close()
    user_logs("Classify email content details Completed",username,'customer Details','0')
    
def get_customer_sentiment_details(customer_name):
    access_db= AccessDatabase()
    cursor= access_db.database_connection_string(access_db.sp_get_customer_sentiment,customer_name)
    data1=cursor.fetchall()
    df_customer_rating_list=[]
    columns=[column[0] for column in cursor.description]
    for rows in data1:
        df_customer_rating_list={columns[0]:rows[0],columns[1]:rows[1],columns[2]:rows[2],columns[3]:rows[3]}
    
    cursor.nextset()
    df_customer_category_list=[]
    columns=[column[0] for column in cursor.description]
    for rows in cursor.fetchall():
        df_customer_category_list.append({name:rows[i] for i, name in enumerate(columns)})
             
    df_customer_category_list= {'categoryGraph':df_customer_category_list}
    df_customer_rating_list.update(df_customer_category_list)
    customer_details = {"customersentiments": df_customer_rating_list}
    return customer_details

def get_support_focal_details(support_focal_name):
    '''Calling Method to get support focal names and logged in support focal details'''
    access_db= AccessDatabase()
    cursor= access_db.database_connection_string(access_db.sp_get_focal_sentiment,support_focal_name)

    
    df_list1=[]
    columns=[column[0] for column in cursor.description]
    for rows in cursor.fetchall():
        df_list1.append({name:rows[i] for i, name in enumerate(columns)})    
        
    cursor.nextset()    
    columns=[column[0] for column in cursor.description]
    df_list2=[]
    for rows in cursor.fetchall():
        df_list2.append({name:rows[i] for i, name in enumerate(columns)})

    
    cursor.nextset()
    columns=[column[0] for column in cursor.description]
    df_list3=[]
    for rows in cursor.fetchall():
        df_list3.append({name: rows[i] for i,name in enumerate(columns)})      
          
       
    cursor.nextset()
    columns=[column[0] for column in cursor.description]
    df_list4=[]
    for rows in cursor.fetchall():
        df_list4.append({name:rows[i] for i, name in enumerate(columns)})

           
    cursor.nextset()
    columns=[column[0] for column in cursor.description]
    df_list5=[]
    for rows in cursor.fetchall():
        df_list5.append({name:rows[i] for i, name in enumerate(columns)})
           
    cursor.close()
    df5= pd.DataFrame(df_list5)
    df_new= pd.DataFrame()
    for i in df5['region'].unique():
        df_new = df_new.append({'region':i,'count':[{'month':df5['DateMY'][j],'count':df5['regionCount'][j]} for j in df5[df5['region']==i].index]}, ignore_index=True)
    df_new= df_new.to_dict(orient='records')
    support_focal_details = {  "firstGraphDetails": df_list1 , "secondGraphDetails" :  df_list2, "thirdGraphDetails" : df_list3, "fourthGraphDetails":df_list4 ,"fifthGraphDetails":df_new}
    return support_focal_details


    
def user_logs(message,username,page_event,flag):
    '''Method for Logging'''
    #date_stamp=pd.datetime.now().date()
    #time_stamp=pd.datetime.now().time()    
    #df_user_log= pd.DataFrame({​​​​​​​'Date': [date_stamp],'Time': [time_stamp],
                               #'Message':[message],'Session':[session],'Page Event':[page_event],'Flag':[flag]}​​​​​​​)
    #l.acquire()
    #df_user_log.to_csv('UserLogs/UserActivityLog'+"_"+TODAY+".csv" ,
                       #mode ='a' , index=False, header= None)
    access_db= AccessDatabase()
    cursor= connection.cursor()
    try:  
        cursor.execute("exec " + access_db.sp_save_userLogs + " '" + message + "','" + username+ "','" + page_event + "','" + flag + "'" )
        #string= '"exec " + access_db.sp_save_userLogs '+ "'"  message + "','" + username + "','" + page_event + "','" + str(flag) + "'" '
        #print(string)
        #cursor.execute("exec " + access_db.sp_save_userLogs + "'" + message + "','" + username + "','" + page_event + "','" + str(flag) + "'" )
        cursor.close()
    except:
        cursor.close()
    #l.release()
    return None





def get_csat_details(mail_content):
    '''Method to get CSAT Details'''
    short_description=re.search(r'Short Description: (.*?)\nDescription:', mail_content).group(1)
    description=re.search(r'Description: (.*?)\nState:', mail_content).group(1)
    caller= re.search(r'Caller: (.*?)\nPriority', mail_content).group(1)
    configuration_item= re.search(r'App Name: (.*?)\nBusiness Service:', mail_content).group(1)
    state=re.search(r'Description: (.*?)\nState:', mail_content).group(1)
    priority=re.search(r'Priority: (.*?)\nImpacted Business Group:', mail_content).group(1)
    text_details = {"priority":priority,"state":state,"shortDescription":short_description,
                    "problemDescription":description,"name":caller,
                    "appName":configuration_item}      
    return text_details

def get_resolution_details(short_description,problem_description):
    '''Method to get resolution comments'''
    print('resolution method')
    inclident_list = ["INC0003584607", "INC0003590897" , "INC0003611666"]
    df_basic = pd.DataFrame()
    df_2 = pd.DataFrame()
    df_1 = pd.DataFrame()
    user_logs("get_resolution_details",'eightnew','resolution method','1')
    user_logs("get_resolution_details",'updatenew','resolution method','1')
    user_logs(path_dir,'nine now','resolution method','1')
    
    df_basic = pd.read_excel(path_dir + r'/Files/MANDATORY COMPLIANCE.xlsx',
                             sheet_name='Source Sheet')
    user_logs(df_basic,'eight','resolution method','1')
    user_logs("get_resolution_details",'two','df_basic','1')
    
    for data in inclident_list:
        df_1=df_basic.loc[df_basic['Incident ID*+'] == data]
        df_2 = df_2.append(df_1)
    title= "Inco terms location error"
    df_2=df_2[['Incident ID*+',"Resolution Notes","Assignee+"]]
    df_2= df_2.rename(columns={"Incident ID*+": "incident", "Resolution Notes": "resolution"
                             ,"Assignee+": "resolvedByName"})

    df_2["date"]= TODAY
    df_2["title"]= title
    user_logs("get_resolution_details",'three','df2','1')
    resolution_details = df_2.to_dict(orient='records')
    print('resolution method completed')
    print(resolution_details)
    user_logs("get_resolution_details",'four','resolution_details','1')
    return resolution_details

api_view(["GET"])
@csrf_exempt
@never_cache
def get_selected_support_focal_details(request):
    '''API to get Selected support focal details'''
    if request.session.get('username') is not   None:
        username=request.session.get('username')
    else:
        text_details = {"responseMessage": "Session expired"}
        return JsonResponse(text_details,safe=False)
    user_logs("Selected Support focals details succesfully",username,"my csat dashboard","1")
    support_focal_name= request.GET.get('supportengineer')
    df_main = pd.DataFrame()
    cursor= connection.cursor()
    support_focal_details = get_support_focal_details(support_focal_name)
    print(support_focal_details)
    if not support_focal_details:        
        text_details = support_focal_details.to_dict(orient='records')
        return JsonResponse(support_focal_details,safe=False)
    else:
        user_logs("Reading agent data succesfully",username,"my csat dashboard","0")          
        return JsonResponse(support_focal_details,safe=False) 
         
api_view(["POST"])
@csrf_exempt
@never_cache
def login(request):
    '''API to Login'''
    if(request.method=='POST'):
        user_logs("User logged in page loaded successfully",'','login','1')
        req=json.loads(request.body)
        app_name  = req.get('username')
        app_pwd  = req.get('password')
        try:
            print('inside try method')
            user=auth.authenticate(username=app_name,password=app_pwd)
            print(user)
        except Exception as e:
            if e and len(e.args) > 0:
                print(f'exception {e}')
                user_logs("User logged in Failed",app_name,'login','0')
        if user is not None:
            username=request.session.get('username')
            support_focal_details1 = {"responseMessage": "data"}            
            user_logs("User logged in succesfully",username,'login','0')
            request.session["username"]= app_name
            return JsonResponse(support_focal_details1,safe=False)
        else:
            text_details = {"responseMessage": "error"}
            user_logs("User does not exist Failed ",'','login','0')            
            return JsonResponse(text_details,safe=False)

api_view(["POST"])
@csrf_exempt
@never_cache
def sentiment_details(request):
    '''Api for Sentiment Details'''
    print('sentiment_details')
    if request.session.get('username') is not None:
        username=request.session.get('username')
    else:
        text_details = {"responseMessage": "Session expired"}
        return JsonResponse(text_details,safe=False)
    user_logs("retrive resolution and customer details started",username,'ticketInsights','1')
    req=json.loads(request.body)
    name = req.get('callerName')
    short_description = req.get('shortDescription')
    problem_description = req.get('problemDescription')
    user_logs("Retrived customer details succesfully",username,'ticketInsights','0')
    print('calling resolution method')
    user_logs("retrieving resolution details started",username,'ticketInsights','0')
    user_logs(short_description,username,'ticketInsights','0')
    resolution = get_resolution_details(short_description,problem_description)
    print('calling resolution method completed')
    user_logs("Retrived resolution details succesfully",username,'ticketInsights','0')
    sentiment_details_data = {"resRecommendations":resolution}
    return JsonResponse(sentiment_details_data,safe=False)

api_view(["POST"])
@csrf_exempt
@never_cache
def customer_details(request):
    '''Api for Customer Details'''
    if request.session.get('username') is not   None:
        username=request.session.get('username')
    else:
        text_details = {"responseMessage": "Session expired"}
        return JsonResponse(text_details,safe=False)
    user_logs("retrive customer details started",username,'customer Details','1')    
    req=json.loads(request.body)
    mail_content = req
    csat_details= get_csat_details(mail_content)    
    user_logs("retrived customer details completed succesfully",username,'customer Details','0')
    return JsonResponse(csat_details,safe=False)
   
api_view(["GET"])
@csrf_exempt
@never_cache
def get_ci_names(request):
    '''Api for Email Content'''
    print('ci_names')
    print(request.session.get('username'))
    if request.session.get('username') is not   None:
        username=request.session.get('username')
    else:
        text_details = {"responseMessage": "Session expired"}
        return JsonResponse(text_details,safe=False)
    user_logs("CiNames fetching Started",username,'ci-names','1')
    access_db= AccessDatabase()
    cursor= access_db.database_connection_string_withoutparam(access_db.sp_get_appnames)    
    ci_names = cursor.fetchone()
    if ci_names is not None:
        ci_names= ci_names[0]
        user_logs("CiNames fetching completed succesfully",username,'ci-names','0')
    else:
        user_logs("No CiNames available",username,'ci-names','0')    
    return JsonResponse(json.loads(ci_names),safe=False)

api_view(["POST"])
@csrf_exempt
@never_cache
def save_aion_feedback(request):
    '''Api to Save Feedback'''
    if request.session.get('username') is not   None:
        username=request.session.get('username')
        user_logs("Saving AIONFeedback Started",username,'aion-user-feedback','1')
        feedback_parameters = json.loads(request.body)
        know_resolution  = feedback_parameters.get('knowResolution')
        enrich_me  = feedback_parameters.get('enrichMe')
        title  = feedback_parameters.get('title')
        resolution  = feedback_parameters.get('resolution')
        other  = feedback_parameters.get('other')
        cursor= connection.cursor()
        access_db= AccessDatabase()
        try:
            cursor.execute("exec " + access_db.sp_save_aion_feedback + " '" + str(know_resolution) + "','" + str(enrich_me) + "','" + title + "','" + resolution + "','" + other + "'" )
            user_logs("Saving AIONFeedback Completed",username,'aion-user-feedback','0')
            cursor.close()
            return JsonResponse(True,safe=False)
        except:
            cursor.close()
            user_logs("Saving AIONFeedback Failed",username,'aion-user-feedback','0')
            return JsonResponse(False,safe=False)
    else:
        text_details = {"responseMessage": "Session expired"}
        return JsonResponse(text_details,safe=False)      
    
api_view(["POST"])
@csrf_exempt
@never_cache
def save_feedback(request):
    '''Api to Save Feedback'''
    print(request.session.get('username'))
    if request.session.get('username') is not   None:        
        username=request.session.get('username')
        user_logs("Saving Resolution Started",username,'recommendation-feedback','1')
        feedback_parameters = json.loads(request.body)
        #Get UserName and Password parameters
        problem_description  = feedback_parameters.get('problemDescription')
        user  = feedback_parameters.get('user')
        recommendation_details  = feedback_parameters.get('recommendationDetails')
        is_helpful  = feedback_parameters.get('isHelpful')
        is_outdated  = feedback_parameters.get('isOutdated')
        is_irrelevant  = feedback_parameters.get('isIrrelevant')
        isincomplete  = feedback_parameters.get('isIncomplete')
        cursor= connection.cursor()
        access_db= AccessDatabase()
        try:
            cursor.execute("exec " + access_db.sp_save_feedback + " '" + problem_description + "','" + user + "','" + str(json.dumps(recommendation_details),) +  "','" + str(is_helpful) +  "','" + str(is_outdated) +  "','" + str(is_irrelevant) + "','" + str(isincomplete) + "'")
            user_logs("Saving Feedback Completed",username,'recommendation-feedback','0')
            cursor.close()
            return JsonResponse(True,safe=False)
        except:
            cursor.close()
            user_logs("Saving Feedback Failed",username,'recommendation-feedback','0')
            return JsonResponse(False,safe=False)
    else:
        text_details = {"responseMessage": "Session expired"}
        return JsonResponse(text_details,safe=False)


api_view(["POST"])
@csrf_exempt
@never_cache
def save_suggestions(request):
    '''Api to Save Suggestions'''
    if request.session.get('username') is not   None:
        username=request.session.get('username')
        user_logs("Saving Suggestions Started",username,'aion-suggestions','1')
        feedback_parameters = json.loads(request.body)
        title  = feedback_parameters.get('title')
        description  = feedback_parameters.get('description')
        cursor= connection.cursor()
        access_db= AccessDatabase()
        try:
            cursor.execute("exec " + access_db.sp_save_suggestion + "'" + title + "','" + description  + "'" )
            user_logs("Saving Suggestions Completed",username,'aion-suggestions','0')
            cursor.close()
            return JsonResponse(True,safe=False)
        except:
            cursor.close()
            user_logs("Saving Suggestions Failed",username,'aion-suggestions','0')
            return JsonResponse(False,safe=False)
    else:
        text_details = {"responseMessage": "Session expired"}
        return JsonResponse(text_details,safe=False)

api_view(["POST"])
@csrf_exempt
@never_cache
def save_content(request):
    '''Api to Save Content'''
    if request.session.get('username') is not   None:
        username=request.session.get('username')
        user_logs("Saving Content Started",username,'aion-content','1')
        feedback_parameters = json.loads(request.body)
        #Get UserName and Password parameters
        title  = feedback_parameters.get('title')
        resolution  = feedback_parameters.get('resolution')
        cursor= connection.cursor()
        access_db= AccessDatabase()
        try:
            cursor.execute("exec " + access_db.sp_save_content + "'" + title + "','" + resolution  + "'" )
            cursor.close()
            user_logs("Saving Content Failed",username,'aion-content','0')
            return JsonResponse(True,safe=False)
        except:
            cursor.close()
            user_logs("Saving Content Failed",username,'aion-content','0')
            return JsonResponse(False,safe=False)
    else:
        text_details = {"responseMessage": "Session expired"}
        return JsonResponse(text_details,safe=False)

api_view(["POST"])
@csrf_exempt
@never_cache
def save_training(request):
    '''Api to Save Training Data'''
    if request.session.get('username') is not   None:
        username=request.session.get('username')
        user_logs("Saving Training Started",username,'aion-training','1')
        feedback_parameters = json.loads(request.body)
        #Get UserName and Password parameters
        domain  = feedback_parameters.get('domain')
        training_type  = feedback_parameters.get('trainingType')
        training_title  = feedback_parameters.get('trainingTitle')
        training_resolution  = feedback_parameters.get('trainingResolution')
        cursor= connection.cursor()
        access_db= AccessDatabase()
        try:
            cursor.execute("exec " + access_db.sp_save_training + "'" + domain + "','" + training_type + "','" + training_title + "','" + training_resolution + "'" )
            cursor.close()
            user_logs("Saving Training Completed",username,'aion-training','0')
            return JsonResponse(True,safe=False)
        except:
            cursor.close()
            user_logs("Saving Training Failed",username,'aion-training','0')
            return JsonResponse(False,safe=False)
    else:
        text_details = {"responseMessage": "Session expired"}
        return JsonResponse(text_details,safe=False)

api_view(["POST"])
@csrf_exempt
@never_cache
def log_feedback(request):
    '''Api to Log Feedback Open Page'''
    req=json.loads(request.body)
    user_name=request.session.get('username')
    page_name=req.get('componentName')
    comments=req.get('eventTriggered')
    user_logs(comments,user_name,page_name,'1')    
    return JsonResponse(False,safe=False)

api_view(["GET"])
@csrf_exempt
@never_cache
def logout(request):
    '''Api for Logout'''
    username=request.session.get('username')
    user_logs("Log out Started",username,'logout','1')
    tmp_logout = auth.logout(request)
    if tmp_logout is None :
        return JsonResponse(True,safe=False)
    else :
        text_details = {"responseMessage": "Session expired"}
        return JsonResponse(text_details,safe=False)

api_view(["POST"])
@csrf_exempt
@never_cache
def register():
    if(request.method=='POST'):
        first_name=request.session.get('first_name')
        last_name=request.session.get('last_name')
        username=request.session.get('username')
        password=request.session.get('password')
        email_id=request.session.get('email')
        user=User.objects.create_user(username=username,password=password,email=email_id,first_name=first_name,last_name=last_name)
        user.save()
        return None
    
api_view(["GET"])
@csrf_exempt
@never_cache
def home(request):
    '''Method for Home Page'''
    #Loads Login Page
    return render(request,"index.html")
