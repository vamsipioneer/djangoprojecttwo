import json
import urllib
import requests
import datetime
from pytz import timezone
from dateutil import parser
from jenkinsapi.jenkins import Jenkins
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from jenkinsapi.jenkins import Jenkins


#  LDAP AUTHENTICATION8
from ldap3 import Connection, Server, SIMPLE, SYNC, SUBTREE, ALL


def ldapAuthentication(request):
    try:
        username = str(request.POST.get('user')).strip()
        password = str(request.POST.get('pwd')).strip()
        server = Server(r'ldap://***********.com', use_ssl=True)
        conn = Connection(server, r'td\{}'.format(username), password, auto_bind=True)
        query_filter = '(samAccountName=*****)'
        base_dn = 'DC=****,DC=*******,DC=COM'
        status = conn.search(search_base=base_dn, search_filter=query_filter, search_scope=SUBTREE, attributes=['*'])
        if status:
            result = conn.response_to_json()
            data = json.loads(result)
            displayName = data['entries'][0]['attributes']['displayName']
            department = data['entries'][0]['attributes']['department']
            manager = data['entries'][0]['attributes']['manager']
            employeeNumber = data['entries'][0]['attributes']['employeeNumber']
            mail = data['entries'][0]['attributes']['mail']
            quicklook = data['entries'][0]['attributes']['sAMAccountName']
            data = {
                'user': displayName, 'status': 200
            }
            request.session['name'] = quicklook
            return HttpResponseRedirect('/jira/')
        else:
            data = {
                'error': 'user not exist', 'status': 400
            }
            raise Exception(data)
    except Exception as e:
        print ("user does not exist")


def validate_username(request):
    username = request.GET.get('Qid', None)
    default_headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    url = 'https://*******.com/jira/rest/api/2/user?username={}'.format(username)
    ret = requests.get(url, headers=default_headers, auth=('*****', '*****'))
    output = ret.json()
    if ret.status_code == 200:
        data = {
            'user' : output['displayName'] , 'status' : 200
        }
    else:
        data = {
            'error': 'user not exist', 'status': 400
        }
    return JsonResponse(data)


def authenticateUser(request):
    try:
        username = request.POST.get('Qid')
        password = request.POST.get('pwd')
        default_headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        url = 'https://**********/jira/rest/api/2/myself'
        ret = requests.get(url, headers=default_headers, auth=(username, password))
        output = ret.json()
        if ret.status_code == 200:
            user = output['name']
            request.session['name'] = user
            return HttpResponseRedirect('/jira/')
        else:
            raise Exception()
    except Exception as e:
        print("User Credentials are wrong")
        return render(request, 'login/login.html',{'error_message': "InValid Credentials"})


def loginView(request):
    return render(request, 'login/login.html', {})

def logoutView(request):
    if request.session['name']:
        del request.session['name']
    return render(request, 'login/login.html', {})



def jiradata(request):
    user = request.session['name']
    default_headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    quoteStringHandler = urllib.parse.quote_plus
    l = 'project="etools" and assignee ="{}" and status in  (open, Closed, "In Progress")'.format(user)
    result = quoteStringHandler(l)
    url = 'https://********************/jira/rest/api/2/search?jql={}'.format(result)
    ret = requests.get(url, headers=default_headers, auth=('', ''))
    output = ret.json()
    issuelist = {}
    for pos, issue in enumerate(output['issues'], 0):
        packedItem = []
        packedItem.append(issue['key'])
        packedItem.append(issue['fields']['summary'])
        # packedItem.append(issue['fields']['issuetype']['name'])
        packedItem.append(issue['fields']['priority']['name'])
        packedItem.append(issue['fields']['status']['name'])
        issueupdated = parser.parse(issue['fields']['updated'])
        issueupdated = (issueupdated.astimezone(timezone('US/Pacific'))).strftime("%Y-%m-%d")
        packedItem.append(issueupdated)
        issuelist[pos] = packedItem
    data = {
        'issues': issuelist, 'row': len(issuelist), 'col': 5
    }
    return JsonResponse(data)



def jenkinsdata(request):
    jenkins_url = 'https://****************.com/'
    JenkinObj = Jenkins(jenkins_url, '****', '******')
    listofjobs = JenkinObj.get_jobs()

    data = {}
    # Job details
    for pos, job in enumerate(listofjobs):
        job = job[0]
        data[pos] = {}
        Job = JenkinObj[job]
        data[pos]['jobname'] = Job
        Job_isActive = str(job.is_enabled())
        data[pos]['Job_isActive'] = Job_isActive
        Job_isRunning = str(job.is_running())
        data[pos]['Job_isRunning'] = Job_isRunning
        Job_status = job.get_last_build().get_status()
        data[pos]['jobstatus'] = Job_status
        Job_url = job.get_last_build().baseurl
        data[pos]['Job_url'] = Job_url
        Job_lastbuild = job.get_last_build()
        data[pos]['Job_lastbuild'] = Job_lastbuild
        Job_executionInMin = job.get_last_build().get_duration().total_seconds()/60
        data[pos]['Job_executionInMin'] = Job_executionInMin
        Job_lastBuildtimeInIST = job.get_last_build().get_timestamp().astimezone(timezone('Asia/Calcutta')).strftime("%Y-%m-%d %H:%M:%S")
        data[pos]['Job_lastBuildtimeInIST'] = Job_lastBuildtimeInIST
    data = {
        'Jenkinsdata': data, 'row': len(data), 'col': 5
    }
    return JsonResponse(data)


def jenkinsdata():
    try:
        jenkins_url = 'https://***************.com/'
        JenkinObj = Jenkins(jenkins_url, '', '')
        listofjobs = JenkinObj.get_jobs()

        data = {}


        for pos, job in enumerate(listofjobs):
            job = job[0]
            Job = JenkinObj[job]
            try:
                jenkins_data = []
                if Job.get_last_build():
                    Job_isActive = Job.is_enabled()
                    Job_isRunning = Job.is_running()
                    Job_status = Job.get_last_build().get_status()
                    Job_url = Job.get_last_build().baseurl
                    Job_lastbuild = Job.get_last_build()
                    Job_executionInMin = Job.get_last_build().get_duration().total_seconds() / 60
                    Job_lastBuildtimeInIST = Job.get_last_build().get_timestamp().astimezone(
                        timezone('Asia/Calcutta')).strftime("%Y-%m-%d %H:%M:%S")
                    jenkins_data.append(Job.name)
                    jenkins_data.append(str(Job_isActive))
                    jenkins_data.append(str(Job_isRunning))
                    jenkins_data.append(Job_status)
                    jenkins_data.append(Job_url)
                    jenkins_data.append(Job_executionInMin)
                    jenkins_data.append(Job_lastBuildtimeInIST)
                    data[pos] = jenkins_data

            except Exception as e:
                jenkins_data.append(Job.name)
                jenkins_data.append('')
                jenkins_data.append('')
                jenkins_data.append('')
                jenkins_data.append('')
                jenkins_data.append('')
                jenkins_data.append('')
                data[pos] = jenkins_data
        return JsonResponse(data)
    except Exception as e:
        print(e)



def jenkinsView(request):
    try:
        request.session['name']
        user = request.session['name']

        Jenkins.No


        return render(request, 'login/jenkinspage.html', {'user': user})
    except KeyError as e:
        return render(request, 'login/login.html', {'error_message': "User should Login to Application."})



def jiraView(request):
    try:
        request.session['name']
        user = request.session['name']
        return render(request, 'login/jirapage.html', {'user': user})
    except KeyError as e:
        return render(request, 'login/login.html', {'error_message': "User should Login to Application."})


def check(request):
    return render(request, 'login/home.html', {})

def paginate(request):
    return render(request, 'login/pagination.html', {})






















