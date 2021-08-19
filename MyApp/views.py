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
from django.contrib.auth.models import User,auth,Group
from django.conf import settings
from django.contrib.sessions.models import Session
from django.views.decorators.cache import never_cache
from django.utils.html import escape
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from MyApp.Loader import PickleLoader,ExcelLoader
from MyApp.Cleaner import DescriptionCleaner
from MyApp.Bm25TrainModel import BM25Model

#from .forms import CreateUserForm

path_dir= os.path.dirname(os.path.realpath(__file__))
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
    sp_save_glossary = 'SaveGlossary'
    sp_get_incident_insights = 'getIncidentInsights'
    sp_save_application_dump = 'SaveApplicationDump'
    
    def __init__(self):
        return None

    def database_connection_string(self,sp_name,sp_param1):
        self.sp_name= sp_name
        self.sp_param1= sp_param1
        cursor= connection.cursor()
        cursor.execute("exec %s %s", [sp_name,sp_param1])
        return cursor

    def database_connection_string_withoutparam(self,sp_name):
        self.sp_name= sp_name
        cursor= connection.cursor()
        cursor.execute("exec %s ", [sp_name])
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
    if request.session.get('username') is not None:
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
    if request.session.get('username') is not None:
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
    cursor= connection.cursor()
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
    access_db= AccessDatabase()
    cursor= connection.cursor()
    try:        
        cursor.execute("exec " + access_db.sp_save_userLogs + " @message= %s , @username =%s, @page_event = %s,@flag = %s",[message,username,page_event,flag])
        #cursor.execute("exec " + access_db.sp_save_userLogs + " '" + message + "','" + username+ "','" + page_event + "','" + flag + "'" )
    except Exception as e:
        cursor.close()
    else:
        cursor.close()
    return None

def get_csat_details(mail_content):
    '''Method to get CSAT Details'''
    short_description=re.search(r'Short Description: (.*?)\nDescription:', mail_content).group(1)
    description=re.search(r'Description: (.*?)\nState:', mail_content).group(1)
    caller= re.search(r'Caller: (.*?)\nPriority', mail_content).group(1)
    configuration_item= re.search(r'Configuration Item: (.*?)\nBusiness Service:', mail_content).group(1)
    state=re.search(r'Description: (.*?)\nState:', mail_content).group(1)
    priority=re.search(r'Priority: (.*?)\nImpacted SBG:', mail_content).group(1)
    text_details = {"priority":priority,"state":state,"shortDescription":short_description,
                    "problemDescription":description,"name":caller,
                    "appName":configuration_item}    
    return text_details
##
##def get_resolution_details_copy(short_description,problem_description,appName):
##    '''Method to get resolution comments'''
##    inclident_list = ['INC0003564917','INC0003575564']
##    inclident_list1 = ",".join(inclident_list)
##    
##    access_db= AccessDatabase()
##    cursor= connection.cursor()
##    try:
##
##        cursor.execute("exec " + access_db.sp_get_incident_insights + " @incidentList= %s" ,[inclident_list1])
##        resolution_details = []
##        columns=[column[0] for column in cursor.description]
##        for rows in cursor.fetchall():
##            resolution_details.append({name:rows[i] for i, name in enumerate(columns)})
##        
##        resolution_details= pd.DataFrame(resolution_details)
##        resolution_details = resolution_details.to_dict(orient='records')
##        cursor.close()
##        
##        return resolution_details
##
##    except Exception as e:
##        cursor.close()
##        return False

def get_resolution_details(short_description,problem_description,appName,assignment_group):
    '''Method to get resolution comments'''
    #Load Files
    print(f'inside resolution {assignment_group} is')
    excel_obj = ExcelLoader(path_dir + "\\Files", assignment_group)
    pickle_obj = PickleLoader(path_dir + "\\Files\modelFiles", "Bm25" + assignment_group)
    df_data= excel_obj.loadFile()

    access_db = AccessDatabase()
    cursor = connection.cursor()
    
    rows= cursor.execute("exec " + access_db.sp_get_incident_insights + " @assignment_group= %s" ,[assignment_group])
    #columns = [column[0] for column in cursor.description]
    df = pd.DataFrame.from_records(rows, columns=[x[0] for x in cursor.description])
    #df= pd.DataFrame(cursor.fetchall())
    
    bm25_pickle_data = pickle_obj.loadFile()
    #Select Valid Columns
    df_data= df_data[["Number","Resolution_notes","Assigned_to","Created","Description"]]
    
    #print(bm25_pickle_data)
    
    #Clean Query
    cleaner_obj = DescriptionCleaner()    
    cleaned_description_query = cleaner_obj.apply_regex(problem_description)
    cleaned_description_query = cleaner_obj.preprocess(cleaned_description_query)
    
   
    #Calculate Score
    doc_scores = bm25_pickle_data.get_scores(cleaned_description_query)
    doc_scores=sorted(doc_scores,reverse=True)
    print(f'docscores : {doc_scores[:11]}')

    #Get Top matching searched data
    results = bm25_pickle_data.get_top_n(cleaned_description_query, df_data.values, n=10) #get search results
    resolution_recommendation= pd.DataFrame(results,columns=['incident','resolution', 'resolvedByName','date','title']) #Convert search results to dataFrame
    resolution_details = resolution_recommendation.to_dict(orient='records')#Convert Dataframe to Dictionary
    
    return resolution_details
    
api_view(["GET"])
@csrf_exempt
@never_cache
def get_selected_support_focal_details(request):
    '''API to get Selected support focal details'''
    if request.session.get('username') is not None:
        username=request.session.get('username')
    else:
        text_details = {"responseMessage": "Session expired"}
        return JsonResponse(text_details,safe=False)
    user_logs("Selected Support focals details succesfully",username,"my csat dashboard","1")
    support_focal_name= request.GET.get('supportengineer')
    df_main = pd.DataFrame()
    #cursor= connection.cursor()
    support_focal_details = get_support_focal_details(support_focal_name)
    if not support_focal_details:        
        support_focal_details = support_focal_details.to_dict(orient='records')
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
        user_name  = str(req.get('username'))
        user_pwd  = req.get('password')
        
        try:
            user=auth.authenticate(username=user_name,password=user_pwd)
        except Exception as e:
            if e and len(e.args) > 0:
                user_logs("User logged in Failed",user_name,'login','0')
        if user is not None:
            username=request.session.get('username')
            support_focal_details1 = {"responseMessage": "data"}            
            user_logs("User logged in succesfully",username,'login','0')            
            request.session["username"]= user_name
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
    if request.session.get('username') is not None:
        username=request.session.get('username')
        assignment_group=request.session.get('assignment_group')
    else:
        text_details = {"responseMessage": "Session expired"}
        return JsonResponse(text_details,safe=False)
    user_logs("retrive resolution and customer details started",username,'ticketInsights','1')
    req=json.loads(request.body)
    name = req.get('callerName')
    appName = req.get('appName')
    short_description = req.get('shortDescription')
    problem_description = req.get('problemDescription')
    user_logs("Retrived customer details succesfully",username,'ticketInsights','0')
    resolution = get_resolution_details(short_description,problem_description,appName,assignment_group)
    user_logs("Retrived resolution details succesfully",username,'ticketInsights','0')
    
    sentiment_details_data = {"resRecommendations":resolution}
    return JsonResponse(sentiment_details_data,safe=False)

    
api_view(["POST"])
@csrf_exempt
@never_cache
def customer_details(request):
    '''Api for Customer Details'''
    if request.session.get('username') is not None:
        username=request.session.get('username')
    else:
        text_details = {"responseMessage": "Session expired"}
        return JsonResponse(text_details,safe=False)
    
    user_logs("retrive customer details started",username,'customer Details','1')    
    #req=json.loads(request.body)
    mail_content= (str(json.loads(request.body)))
    
    assignment_group = re.search(r'Assignment Group: (.*?)\nComments:', mail_content).group(1)
    assignment_group = re.sub('[^A-Za-z0-9]+', ' ', assignment_group)
    
    csat_details= get_csat_details(mail_content)
    request.session['assignment_group'] =  assignment_group
    user_logs("retrived customer details completed succesfully",username,'customer Details','0')
    return JsonResponse(csat_details,safe=False)
   
api_view(["GET"])
@csrf_exempt
@never_cache
def get_ci_names(request):
    '''Api for Email Content'''
    if request.session.get('username') is not None:
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
    if request.session.get('username') is not None:
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
            cursor.execute("exec " + access_db.sp_save_aion_feedback + " @knowresolution= %s , @Enrichme =%s, @Title = %s,@Resolution = %s,@OtherSuggestion=%s",[know_resolution,str(enrich_me),title,resolution,other])
            #cursor.execute("exec %s %s %s %s %s %s ", [access_db.sp_save_aion_feedback,str(),str(enrich_me),title,resolution,other])
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
    if request.session.get('username') is not None:        
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
        is_incomplete  = feedback_parameters.get('isIncomplete')
        cursor= connection.cursor()
        access_db= AccessDatabase()
        try:            
            #cursor.execute("exec %s %s %s %s ", [access_db.sp_save_feedback,problem_description,user,str(json.dumps(recommendation_details),)])
            cursor.execute("exec " + access_db.sp_save_feedback + " @ProblemDescription= %s , @user =%s, @RecommendationDetails = %s,@IsHelpful = %s,@IsOutdated=%s, @IsIrrelevant= %s , @IsIncomplete= %s ",[problem_description,user,str(json.dumps(recommendation_details)),is_helpful,is_outdated,is_irrelevant,is_incomplete])
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
    if request.session.get('username') is not None:
        username=request.session.get('username')
        user_logs("Saving Suggestions Started",username,'aion-suggestions','1')
        feedback_parameters = json.loads(request.body)
        title  = feedback_parameters.get('title')
        description  = feedback_parameters.get('description')
        cursor= connection.cursor()
        access_db= AccessDatabase()
        try:
            #cursor.execute("exec %s %s %s ", [access_db.sp_save_suggestion,title,description])
            cursor.execute("exec " + access_db.sp_save_suggestion + " @title= %s , @description =%s",[title,description])
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
    if request.session.get('username') is not None:
        username=request.session.get('username')
        user_logs("Saving Content Started",username,'aion-content','1')
        feedback_parameters = json.loads(request.body)
        #Get UserName and Password parameters
        title  = feedback_parameters.get('title')
        resolution  = feedback_parameters.get('resolution')
        cursor= connection.cursor()
        access_db= AccessDatabase()
        try:
            #cursor.execute("exec %s %s %s ", [access_db.sp_save_content,title,resolution])
            cursor.execute("exec " + access_db.sp_save_content + " @title= %s , @resolution =%s",[title,resolution])
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
    if request.session.get('username') is not None:
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
            #cursor.execute("exec %s %s %s %s %s", [access_db.sp_save_training,domain,training_type,training_title,training_resolution])
            cursor.execute("exec " + access_db.sp_save_training + " @domain= %s , @trainingType =%s , @trainingTitle= %s, @trainingResolution= %s",[domain,training_type,training_title,training_resolution])
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
def save_glossary(request):
    '''Api to Save Content'''
    if request.session.get('username') is not None:
        username=request.session.get('username')
        user_logs("Saving Glossary Started",username,'enrichme','1')
        appName= request.GET.get('appName')
        incorrect_glossary= request.GET.get('inpIncorrectGlossary')
        correct_glossary= request.GET.get('inpCorrectGlossary')
        cursor= connection.cursor()
        access_db= AccessDatabase()
        sql= "exec " + access_db.sp_save_glossary + " @appName= %s , @incorrect_glossary =%s, @correct_glossary = %s"
        prm= [appName,incorrect_glossary,incorrect_glossary]
        try:
            cursor.execute(sql,prm)
            cursor.close()
            user_logs("Saving Glossary Completed",username,'enrichme','0')
            return JsonResponse(True,safe=False)
        except Exception as e:
            #print(e)
            cursor.close()
            user_logs("Saving Glossary Failed",username,'enrichme','0')
            return JsonResponse(False,safe=False)
    else:
        text_details = {"responseMessage": "Session expired"}
        return JsonResponse(text_details,safe=False)


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
from MyApp.forms import SignUpForm

def registerPage(request):
    form= SignUpForm()
    if request.method == 'POST':
        form= SignUpForm(request.POST)
       
        if form.is_valid():
            username= form.cleaned_data.get('username')
            messages.success(request,"Account created succesfully for : " + username)
            form.save()
    context = {'form': form}
    return render(request, 'register.html',context)


api_view(["GET"])
@csrf_exempt
@never_cache
def home(request):
    '''Method for Home Page'''
    #Loads Login Page
    return render(request,"index.html")

dT = pd.read_excel(path_dir + '\\' + 'pred_data_with_domain.xlsx',index_col=0)
api_view(["GET"])
@csrf_exempt
@never_cache
def ticket_prediction(request):
	return render(request, "predict.html", {"flag":1})

def domain_data(request):
	domains_list = dT['Domain'].unique()
	#domains_list = domains_list.tolist()
	d={}
	for i in domains_list:
		var=dT.loc[dT['Domain'] == i]
		total=sum(var['Total'])
		d[i]=total
	return JsonResponse(d)
	
api_view(["GET"])
@csrf_exempt
@never_cache
def app_prediction(request):
	App=request.GET['App']
	result=dT.iloc[dT.index==App]
	out1=result['Total']
	total1=int(out1)
	return render(request, 'predict.html', {'result1':total1,'App':App, 'flag':3})
    
api_view(["GET"])
@csrf_exempt
@never_cache	
def domain_prediction(request):
    Domain=request.GET['Domain']
    res=dT.loc[dT['Domain'] == Domain]
    out=sum(res['Total'])
    total=int(out)
    return render(request, 'predict.html', {'result':total,'domain':Domain, 'flag':2})

api_view(["GET"])
@csrf_exempt
@never_cache
def bm25model_training(request):
    from icecream import ic
    ic()
    path= r"C:\Users\avneet\Desktop\SampleProject - LocalHost\SampleProject\MyApp\Files"
    path_dir= r"C:\Users\avneet\Desktop\SampleProject - LocalHost\SampleProject\MyApp\Files\modelFiles"
    filename= "ticketData"
    excel_obj = ExcelLoader(path, filename)
    pickle_obj = PickleLoader(path_dir, "Bm25" )
    cleaner_obj = DescriptionCleaner()
    BM25Model_obj = BM25Model(excel_obj)
    BM25Model_obj.bm25model_training(cleaner_obj,pickle_obj)
        
    return None
