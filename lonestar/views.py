from django.shortcuts import render
from django.views import generic

import re, json, os, linecache
import random 
import math
import pytz

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.hashers import make_password

from django.conf import settings
from decimal import Decimal
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import authenticate, login, logout
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.conf import settings
from django.core import serializers
from django.db.models import Q, F
from .forms import SignupForm

from .tokens import account_activation_token
from .models import User, Event, Team, PromoItem, RegPrice, DiscountCode, TeamStats, Runner, Order, OrderDetl, currentevent, currentorders, currentrunners, CurrentTeams, currentrosterinfo, Transactions

from .tables import CurrentTeamsInfoTable, currentrosterinfotable, currenttirgearinfotable

from datetime import datetime

from .utils import tir
today = datetime.now().replace(tzinfo=pytz.UTC).date()   # tz aware datetime object

defaultpwd = make_password('texas')
paypal_access_token = "access_token$sandbox$1234567890"






# Create your views here.
class IndexView(generic.TemplateView): 
    template_name = 'root/base.html'

def go_pracicehome(request):
    return render(request, 'practicehome/content.html')

def go_BetaHomePage(request):
    return render(request, 'betahomepage/content.html')

def go_GeneralInfo(request):
    return render(request, 'generalinfo/content.html')

 
def go_AdminManager(request):

    return render(request, 'adminmanger/content.html')

# display tir info page
def get_TirInfo(request):
    return render(request, 'tirinfo/content.html')

def show_Map(request):
    return render(request, 'map/content.html')


def go_RelayResources(request):
    return render(request, 'relayresources/content.html')

def go_History(request):
    return render(request, 'history/content.html')


def get_Results(request):
    return render(request, 'results/content.html')

def get_ResultsOld(request):
    return render(request, 'results/oldcontent.html')
def get_StartTimeEmail(request):
    return render(request, 'starttimeemail/content.html')

def get_Videos(request):
    return render(request, 'videos/content.html')
   
def get_Individual_Placement(request):
    return render(request, 'individualplacement/content.html')


def go_Tirgear_Closed(request):
    return render(request, 'tirgearclosed/index.html')
  
def do_download(request):
    return render(request, 'downloads/index.html')

# @login_required
def go_faq(request):
    
    return render(request, 'faq/content.html' )


# @login_required
def go_TicTocTracking(request):
    return redirect('https://docs.google.com/spreadsheets/d/1L58KPXZsRYEdkm1NycEm4qJ50xSen0rmVEMLYQpkMSc/edit#gid=0')

# @login_required
def go_TicTocTwo(request):
    return render(request, 'tictoc/tictoc2.html' )

def go_TicTocMapVersion(request):
    return render(request, 'tictoc/mapversion.html' )

def go_TicTocExchangeForm(request):
    return render(request, 'tictoc/exchangeform.html')

# display TirResult Page
def go_TicTocResults(request, id):
    try:
        url = 'tictocresults/'+ id + '.html'
        return render(request, url)
    except:
        return render(request, 'tictocresults/index.html')

# display Tirresource Page
def get_Tirresource(request):
    return render(request, 'tirresources/content.html')

# display Merchandise
def get_Merchandise(request):
    return render(request, 'merchandise/content.html')

def open_Teams(request):
    return render(request, 'team/content.html', status=200)

def handler404(request):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)

def show_Privacy_Policy(request):
    return render(request, 'privacy_policy.html')



def account_activation_sent(request):
    return render(request, 'account_activation_sent.html')

# user sign up mail activation
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        data = {
            'content' : 'registered'
        }
        return JsonResponse(data)
    else:
        return render(request, 'account_activation_invalid.html')


def login_required(function):
    """ this function is a decorator used to authorize if a user is admin """
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return function(request, *args, **kwargs)
        else:
            return render(request, 'root/base.html')
    return wrap   

# log in function 
def log_In(request):
    email_ = request.POST.get('_email')
    pwd_ = request.POST.get('_pwd')
    print(email_, pwd_, "@@@@@@###########")
    username = User.objects.filter(email=email_).order_by('id').first()
    user = authenticate(username = username, password = pwd_)
    if user is not None: 
        login(request, user) 
        data = { 'valid' : True,
            'content' :'ok' 
        }
        
    else: 
        data = {
            'valid' : False,
            'content' : 'unregistered'
        }
    return JsonResponse(data)

def signUpfn(email, username, password,  runnerid, request):
    
    
    if request.user.is_authenticated and not request.user.is_superuser  :
        id_ = request.user.runnerid
        User.objects.filter(runnerid = id_ ).delete()
       
    user_ = User.objects.filter(username=username).order_by('id').first()
    
    if user_ is not None:
        User.objects.filter(username=username).order_by('id').update(runnerid = runnerid)
    else:
        u = User(email=email, username=username, password=make_password( password ), runnerid=runnerid)
        u.save()
    username = User.objects.filter(email=email, username=username).order_by('id').first()
    user = authenticate(username=username, password=password )
    if user is not None: 
        login(request, user) 
        return True
    return False



# log out function
def log_Out(request):
    logout(request)
    return JsonResponse({'content':'ok'})

def change_Password(request, pwd):
   
    data = {}
    error= ''
    if request.user.is_authenticated:
        data = tir.get_user_info(request.user.runnerid)
      
    else:
         return render(request, 'root/base.html')

    if pwd == 'index':   
        return render(request, 'changepwd/content.html', { "info": data , "error": error } )
    else:
        if pwd is not None and pwd is not '':

            u = User.objects.get(id = request.user.id )
            u.set_password(pwd)
            u.save()
            Runner.objects.filter(id= u.runnerid ).update( PassHash= u.password )
            user = authenticate(username=u.username, password=pwd )
            login( request, user)
            return JsonResponse({ "info": data , "error": False } )
        else:
            return JsonResponse({ "info": data , "error": 'Password undefined' })
         
         
       
   
    


# sign up function
def sign_Up(request):
    if request.method == "POST":
        role = request.POST.get("role", "linguist")
        form = SignupForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if role == 'admin':
                user.is_staff = True
                user.linguist = False
            else:
                user.is_staff = False
                user.linguist = True
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            message = loader.render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            # user.email_user(mail_subject, message)
            mail = EmailMessage('Activate your LoneStar account.', message, to=[user.email], from_email=settings.EMAIL_HOST_USER)
            mail.content_subtype = 'html'
            mail.send()
            return JsonResponse({'content':'<p>Please confirm your email address to complete the registration. </p>'})
        else:
            return JsonResponse({'content': str(form.errors)})
        
    else:
        form = SignupForm()
    return render(request, 'translator/index.html', {'form': form})

def forget_PassWord(request):
    _email = request.POST.get('_email', '')
    user = User.objects.get(email=_email)
    print(user)
    if user is not None: 
        current_site = get_current_site(request)
        message = loader.render_to_string('account_activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':account_activation_token.make_token(user),
        })
        # user.email_user(mail_subject, message)
        mail = EmailMessage('Activate your LoneStar account.', message, to=[user.email], from_email=settings.EMAIL_HOST_USER)
        mail.content_subtype = 'html'
        try:
            mail.send()
        except:
            error = 'Your email is valid'
        return JsonResponse({'content':'<p>Please confirm your email address to complete the registration. </p>', 'valid' : True})
    else:
        return JsonResponse({'content': 'current email is unregister', 'valid' : False})


def do_adminlogin(request):
    data = {}
    if request.method == "POST":
        ad_id = request.POST.get("id_")
        ad_pw = request.POST.get('pw_')
        eventid = tir.get_Event_Id()
        user = authenticate(username = ad_id, password = ad_pw)
        if user is not None:
            data['user'] = user.is_superuser
            if user.is_superuser:
                login(request, user)
                data = { 
                    'valid' : True,
                    'content' :'ok' 
                }
            else:
                data = {
                    'valid' : False,
                    'content' : 'unregistered'
                }
        return JsonResponse({'data': data, 'status' : True})
    else: 
        return render(request, 'adminlogin/content.html')
  
  

def go_AdminTeams(request):

    sort = request.GET.get('sort', 'TeamNumber')
    eventid = tir.get_Event_Id()
    print(eventid, 'eventinfo')

    print(sort, 'eventinfo')

    query = "select `e`.`id` AS `id`,`t`.`Bib` AS `TeamNumber`,`t`.`Name` AS `Name`,`t`.`JoinCode` AS `JoinCode`,concat(`r`.`FirstName`,' ',`r`.`LastName`) AS `Captain`,`r`.`Email` AS `Email`,`r`.`Phone` AS `Phone`,`t`.`Type` AS `Type`,`t`.`Classification` AS `Classification`,`t`.`Song` AS `Song`,`t`.`IsUntimed` AS `IsUntimed`,coalesce(`p`.`AvgPace`,0) AS `AvgPace`,coalesce(`p`.`NumRunners`,0) AS `NumRunners`,coalesce(`p`.`MS`,0) AS `MS`,coalesce(`p`.`MM`,0) AS `MM`,coalesce(`p`.`ML`,0) AS `ML`,coalesce(`p`.`MXL`,0) AS `MXL`,coalesce(`p`.`MXXL`,0) AS `MXXL`,coalesce(`p`.`WS`,0) AS `WS`,coalesce(`p`.`WM`,0) AS `WM`,coalesce(`p`.`WL`,0) AS `WL`,coalesce(`p`.`WXL`,0) AS `WXL`,coalesce(`p`.`S-M`,0) AS `S_M`,coalesce(`p`.`XL-L`,0) AS `XL_L` from (((`db_lonestar`.`currentteams` `t` left join (select `currentrunners`.`TeamID` AS `TeamID`,sum(coalesce(`currentrunners`.`Pace`,0)) / sum(case coalesce(`currentrunners`.`Pace`,0) when 0 then 0 else 1 end) AS `AvgPace`,count(`currentrunners`.`ID`) AS `NumRunners`,sum(case `currentrunners`.`ShirtSize` when 'MS' then 1 else 0 end) AS `MS`,sum(case `currentrunners`.`ShirtSize` when 'MM' then 1 else 0 end) AS `MM`,sum(case `currentrunners`.`ShirtSize` when 'ML' then 1 else 0 end) AS `ML`,sum(case `currentrunners`.`ShirtSize` when 'MXL' then 1 else 0 end) AS `MXL`,sum(case `currentrunners`.`ShirtSize` when 'MXXL' then 1 else 0 end) AS `MXXL`,sum(case `currentrunners`.`ShirtSize` when 'WS' then 1 else 0 end) AS `WS`,sum(case `currentrunners`.`ShirtSize` when 'WM' then 1 else 0 end) AS `WM`,sum(case `currentrunners`.`ShirtSize` when 'WL' then 1 else 0 end) AS `WL`,sum(case `currentrunners`.`ShirtSize` when 'WXL' then 1 else 0 end) AS `WXL`,sum(case `currentrunners`.`SockSize` when 'S-M' then 1 else 0 end) AS `S-M`,sum(case `currentrunners`.`SockSize` when 'XL-L' then 1 else 0 end) AS `XL-L` from `db_lonestar`.`currentrunners` where `currentrunners`.`IsDeleted` = 0 group by `currentrunners`.`TeamID`) `p` on(`p`.`TeamID` = `t`.`ID`)) join `db_lonestar`.`currentrunners` `r` on(`r`.`TeamID` = `t`.`ID` and `r`.`ID` = `t`.`CaptainID`)) join `db_lonestar`.`currentevent` `e` on(`e`.`id` = `t`.`EventID`)) where (case `t`.`IsSplitPayment` when 0 then `t`.`IsPaid` else `r`.`IsPaid` end) = 1  Order By {0} ".format(sort)
    print(query)
    table = CurrentTeamsInfoTable(CurrentTeams.objects.raw(query))

    return render(request, 'adminteams/content.html',{ 
        'teaminfotable': table  })



def go_AdminRoster(request):
    sort = request.GET.get('sort', 'TeamName')
    if sort == 'export':
        sort = 'TeamName'
    eventid = tir.get_Event_Id()
    print(eventid, 'eventinfo')

    print(sort, 'eventinfo')

    print(currentrosterinfo)
    print(currentrosterinfo.objects.all().order_by(sort))
    rostermodel = currentrosterinfo.objects.all().order_by(sort)
    table = currentrosterinfotable(currentrosterinfo.objects.all().order_by(sort))
    print(table)
  
    return render(request, 'adminroster/content.html', { 
        'runnerrostertable': table  })




def go_AdminTirgear(request):
    sort = request.GET.get('sort', 'TeamName')
    eventid = tir.get_Event_Id()
    print(eventid, 'eventinfo')
    print(sort, 'sort info')

    query = "SELECT  `t`.`ID` AS `id`,  `t`.`Bib` AS `TeamNumber`,  `t`.`Name` AS `TeamName`,  CONCAT(`r`.`FirstName`,' ',`r`.`LastName`) AS `Runner`,  COALESCE(`o`.`Gear`,'') AS `Gear`,  COALESCE(`o`.`Sizes`,'') AS `Sizes`,  COALESCE(CASE `o`.`Paid` WHEN 0 THEN 'Yes(0)' ELSE `o`.`Paid` END,'') AS `Paid`,  `r`.`ShirtSize` AS `ShirtSize`,  `r`.`SockSize` AS `SockSize`,  `r`.`Phone` AS `Phone`,  `r`.`Email` AS `Email`,  `r`.`Street` AS `Street`,  `r`.`City` AS `City`,  `r`.`State` AS `State`,  `r`.`Zip` AS `Zip` FROM ((`db_lonestar`.`currentrunners` `r`  JOIN `db_lonestar`.`currentteams` `t`  ON (`t`.`ID` = `r`.`TeamID`))  LEFT JOIN (SELECT  `o`.`RunnerID` AS `RunnerID`,  GROUP_CONCAT(CONCAT(`p`.`Name`,CASE `od`.`Num` WHEN 1 THEN '' ELSE CONCAT('(',`od`.`Num`,')') END) SEPARATOR ', ') AS `Gear`,  GROUP_CONCAT(COALESCE(`od`.`Size`,'') SEPARATOR ', ') AS `Sizes`,  MAX(`o`.`PaidAmount`) AS `Paid`  FROM ((`db_lonestar`.`lonestar_orderdetl` `od`  JOIN `db_lonestar`.`lonestar_order` `o`  ON (`o`.`id` = `od`.`OrderID`))  JOIN `db_lonestar`.`lonestar_promoitem` `p`  ON (`od`.`PromoItemID` = `p`.`id`))  WHERE `o`.`IsPaid` = 1  GROUP BY `o`.`RunnerID`) `o`  ON (`o`.`RunnerID` = `r`.`ID`)) WHERE `r`.`IsDeleted` = 0 Order By {0} ".format(sort)
    
    table = currenttirgearinfotable(CurrentTeams.objects.raw(query))
    return render(request, 'admintirgear/content.html', { 
        'tirgearinfotable': table  })



def do_CsvDownload(request):

    tbl_ = request.POST.get('tbl_')
    sort_ = request.POST.get('sort_')
    csvmodel = ''
    eventid = tir.get_Event_Id()
    if request.method == 'POST': 
        corpus_id = request.POST.get('id')
        download_filename = 'tirroster_' + str(today.year) + "_" + str(today.month) + "_" + str(today.month) + "_" + datetime.now().strftime('%H_%M_%S')+ '.csv'
       
        if tbl_ == 'roster':
            down_sentences = currentrosterinfo.objects.filter().order_by(sort_)
            down_path = os.path.join(settings.MEDIA_ROOT, download_filename)
            base_path = tir.csv_downloadFileRoster(down_path, down_sentences)
            return JsonResponse({ 'valid': True, 'url' : base_path }, status = 200)
        elif tbl_ == 'teams':
            query = "select `e`.`id` AS `id`,`t`.`Bib` AS `TeamNumber`,`t`.`Name` AS `Name`,`t`.`JoinCode` AS `JoinCode`,concat(`r`.`FirstName`,' ',`r`.`LastName`) AS `Captain`,`r`.`Email` AS `Email`,`r`.`Phone` AS `Phone`,`t`.`Type` AS `Type`,`t`.`Classification` AS `Classification`,`t`.`Song` AS `Song`,`t`.`IsUntimed` AS `IsUntimed`,coalesce(`p`.`AvgPace`,0) AS `AvgPace`,coalesce(`p`.`NumRunners`,0) AS `NumRunners`,coalesce(`p`.`MS`,0) AS `MS`,coalesce(`p`.`MM`,0) AS `MM`,coalesce(`p`.`ML`,0) AS `ML`,coalesce(`p`.`MXL`,0) AS `MXL`,coalesce(`p`.`MXXL`,0) AS `MXXL`,coalesce(`p`.`WS`,0) AS `WS`,coalesce(`p`.`WM`,0) AS `WM`,coalesce(`p`.`WL`,0) AS `WL`,coalesce(`p`.`WXL`,0) AS `WXL`,coalesce(`p`.`S-M`,0) AS `S_M`,coalesce(`p`.`XL-L`,0) AS `XL_L` from (((`db_lonestar`.`currentteams` `t` left join (select `currentrunners`.`TeamID` AS `TeamID`,sum(coalesce(`currentrunners`.`Pace`,0)) / sum(case coalesce(`currentrunners`.`Pace`,0) when 0 then 0 else 1 end) AS `AvgPace`,count(`currentrunners`.`ID`) AS `NumRunners`,sum(case `currentrunners`.`ShirtSize` when 'MS' then 1 else 0 end) AS `MS`,sum(case `currentrunners`.`ShirtSize` when 'MM' then 1 else 0 end) AS `MM`,sum(case `currentrunners`.`ShirtSize` when 'ML' then 1 else 0 end) AS `ML`,sum(case `currentrunners`.`ShirtSize` when 'MXL' then 1 else 0 end) AS `MXL`,sum(case `currentrunners`.`ShirtSize` when 'MXXL' then 1 else 0 end) AS `MXXL`,sum(case `currentrunners`.`ShirtSize` when 'WS' then 1 else 0 end) AS `WS`,sum(case `currentrunners`.`ShirtSize` when 'WM' then 1 else 0 end) AS `WM`,sum(case `currentrunners`.`ShirtSize` when 'WL' then 1 else 0 end) AS `WL`,sum(case `currentrunners`.`ShirtSize` when 'WXL' then 1 else 0 end) AS `WXL`,sum(case `currentrunners`.`SockSize` when 'S-M' then 1 else 0 end) AS `S-M`,sum(case `currentrunners`.`SockSize` when 'XL-L' then 1 else 0 end) AS `XL-L` from `db_lonestar`.`currentrunners` where `currentrunners`.`IsDeleted` = 0 group by `currentrunners`.`TeamID`) `p` on(`p`.`TeamID` = `t`.`ID`)) join `db_lonestar`.`currentrunners` `r` on(`r`.`TeamID` = `t`.`ID` and `r`.`ID` = `t`.`CaptainID`)) join `db_lonestar`.`currentevent` `e` on(`e`.`id` = `t`.`EventID`)) where (case `t`.`IsSplitPayment` when 0 then `t`.`IsPaid` else `r`.`IsPaid` end) = 1  Order By {0} ".format(sort_)
         
            down_sentences = CurrentTeams.objects.raw(query)
         
            down_path = os.path.join(settings.MEDIA_ROOT, download_filename)
            base_path = tir.csv_downloadFileTeams(down_path, down_sentences)
            return JsonResponse({ 'valid': True, 'url' : base_path }, status = 200)
        elif tbl_ == 'tirgear':
            query = "SELECT  `t`.`ID` AS `id`,  `t`.`Bib` AS `TeamNumber`,  `t`.`Name` AS `TeamName`,  CONCAT(`r`.`FirstName`,' ',`r`.`LastName`) AS `Runner`,  COALESCE(`o`.`Gear`,'') AS `Gear`,  COALESCE(`o`.`Sizes`,'') AS `Sizes`,  COALESCE(CASE `o`.`Paid` WHEN 0 THEN 'Yes(0)' ELSE `o`.`Paid` END,'') AS `Paid`,  `r`.`ShirtSize` AS `ShirtSize`,  `r`.`SockSize` AS `SockSize`,  `r`.`Phone` AS `Phone`,  `r`.`Email` AS `Email`,  `r`.`Street` AS `Street`,  `r`.`City` AS `City`,  `r`.`State` AS `State`,  `r`.`Zip` AS `Zip` FROM ((`db_lonestar`.`currentrunners` `r`  JOIN `db_lonestar`.`currentteams` `t`  ON (`t`.`ID` = `r`.`TeamID`))  LEFT JOIN (SELECT  `o`.`RunnerID` AS `RunnerID`,  GROUP_CONCAT(CONCAT(`p`.`Name`,CASE `od`.`Num` WHEN 1 THEN '' ELSE CONCAT('(',`od`.`Num`,')') END) SEPARATOR ', ') AS `Gear`,  GROUP_CONCAT(COALESCE(`od`.`Size`,'') SEPARATOR ', ') AS `Sizes`,  MAX(`o`.`PaidAmount`) AS `Paid`  FROM ((`db_lonestar`.`lonestar_orderdetl` `od`  JOIN `db_lonestar`.`lonestar_order` `o`  ON (`o`.`id` = `od`.`OrderID`))  JOIN `db_lonestar`.`lonestar_promoitem` `p`  ON (`od`.`PromoItemID` = `p`.`id`))  WHERE `o`.`IsPaid` = 1  GROUP BY `o`.`RunnerID`) `o`  ON (`o`.`RunnerID` = `r`.`ID`)) WHERE `r`.`IsDeleted` = 0 Order By {0} ".format(sort_)
            down_sentences = CurrentTeams.objects.raw(query)
            # down_sentences = currenttirgearinfo.objects.filter().order_by(sort_)
            down_path = os.path.join(settings.MEDIA_ROOT, download_filename)
            base_path = tir.csv_downloadFileTirgear(down_path, down_sentences)
            return JsonResponse({ 'valid': True, 'url' : base_path }, status = 200)
        else:
            pass
        return JsonResponse({'valid': False, 'error' : 'please give error content1'}, status = 200)         
    else:
        return JsonResponse({'valid': False, 'error' : 'please give error content2'}, status = 200)
    

def get_2019Results(request):
   
    return render(request, '2019results/index.html')
 
def get2019ResultInfo(request):
    teamsjson = {}
    isSuccess = True
    error = ''
    
    try:
        teamslist = TeamStats.objects.filter(CurrentLeg = 37,  EventId = 1).order_by('TotalPaceSecs')
        teamsjson = serializers.serialize('json', teamslist)
        print(teamsjson) 
    except:
        isSuccess = False
        error = "you have to defined error type, please show nmt_server example"
   
    data = {
        'isSuccess': isSuccess,
        "error": error,
        'teams' : teamsjson
    }
    return JsonResponse({'valid': True, 'data' : data}, status = 200)
   

def get_membersOfteam(tid):
    runnersofteam = currentrunners.objects.filter(TeamID=int(tid)).count()
    print(runnersofteam, 'num of team')
    if runnersofteam >= 12:
        return True
    else:
        return False
    

def check_Email(request):
    email_ = request.POST.get('email_')
    runnersmodel = currentrunners.objects.filter(Email=email_)
    print(runnersmodel)
    runners = []
    if runnersmodel:
        runners = tir.get_currentrunner_model_to_json(runnersmodel)

    if len(runners) > 0:
        return JsonResponse({'valid': True, 'data' : 'Current Email already exist.' }, status=200)
    else:
        return JsonResponse({'valid': True, 'data' : 'OK' }, status=200)



def do_register(request, getjoinCode):
    print('--->>>> Site User Register Start <<<<<-----')
    print(getjoinCode, ' <<<---- join code 0')
    # please check JoinCode.
    data = {
        'isevent' : False ,
        'eventid' : '',
        "event_year" : today.year,
        'islogged' : False,
        'userinfo' : '',
        'joinCode' : 0,
        "iscaptain" : True,
        'isselectedteam' : False,
        'selectedteam' : "",
        'promoitems': '',
        'is_full' : False
    }
  
    if getjoinCode != 'index':
        data['joinCode'] = getjoinCode
        data['iscaptain'] = False
    # please check next event.
    eventid = tir.get_Event_Id()
    print(eventid, '<- eventinfo')

    if eventid == False:
        return render(request, 'register/content.html',  { "data": data, 'remcol':9 } )
    else:
        data['isevent'] = True
        data['eventid'] = eventid
    
    # please get userinfo. new insert part
    userinfo = {}
    if request.user.is_authenticated:
        print(request.user.runnerid, 'this is runner id of user logged')
        userinfo = tir.get_user_info(request.user.runnerid)
        data['islogged'] = True
        data['userinfo'] = userinfo
        data['selectedteam'] = userinfo['team']
        

   
    sel_team = []
    data['isselectedteam'] = False
    if getjoinCode != 'index':
        # CurrentTeams, please use this table. ......
        selectedteam = CurrentTeams.objects.filter(EventID=int(data['eventid']), JoinCode=int(getjoinCode) ).all()
        if selectedteam:
            sel_team = tir.get_CurrentTeams_model_to_json(selectedteam)
        if sel_team:
           
            data['selectedteam'] = sel_team
            data['isselectedteam'] = True
            is_full = get_membersOfteam(sel_team[0]['id'])
            data['is_full'] = False
            print(sel_team,' this is team selected by user.')
        
            
    # If joincode is fake, render to home '/'
    if getjoinCode != 'index' and data['isselectedteam'] == False :
        return render(request, 'register/content.html',  { "data": data, 'remcol':9 } )

    #  get promoitem
    jsonprmoitems = []    
    promoItems = PromoItem.objects.filter( IsActive = 1 ).order_by('Name')
    
    if len(promoItems):
        data['promoitems'] = tir.get_PromoItem_model_to_json(promoItems)    

    return render(request, 'register/content.html',  { "data": data, 'remcol':9 } )

def displayTime(sec_):
    mins_ = math.floor(sec_ / 60)
    secs_ = math.floor(sec_ % 60)
    if secs_ < 10:
        secs_ = "0" + str(secs_)
    else:
        secs_ = str(secs_)
    return str( mins_ ) + ":" + secs_

# @login_required
def get_Team(request):
    
    userinfo = {
        'is_superuser' : False,
        'RunnerID' : '',
        'TeamID' : '',
        'TeamName' : '',
        'FirstName' : '',
        'LastName' : '',
        'TeamBib' : '',
        'iscaptain' : False,
        'ismyteam' : False,
        'admin' : False,
        'editrunner' : False,
        'editmode' : False,
        'teaminfo_or_edit_iscaption_admin' : False,
        'is_editmode_and_iscaptain_or_admin' : False
    }

    admin = False # admin info.
    if request.user.is_superuser:
        admin = True
        userinfo['admin'] = True
    # please get info of user logged.
    userinfo['RunnerID'] = request.user.runnerid
    userinfo['info'] = tir.get_user_info(request.user.runnerid)
    print(userinfo['info'], 'kjkjkjk--')
    eventid = tir.get_Event_Id()
    teambib = ''
    teamid = ''
    ismyteam = False
    # when user selece any team, you can get following value.
    # these values can use when user are going to show special team.
   
    if 'teambib' in request.GET:
        teambib = request.GET['teambib']
        
    print(teambib,'teambib-get request')
    if teambib == '' or teambib is None :
        if userinfo['info']['runner']:
           
            teamid = userinfo['info']['runner'][0]['TeamID']
            print(teamid, 'teamid-12')
            teammodel = CurrentTeams.objects.filter(ID=int(teamid) ).all()
            teaminfo = tir.get_CurrentTeams_model_to_json(teammodel)
            print(teaminfo, 'teaminfo-13')
            teambib = teaminfo[0]['Bib']
            userinfo['TeamBib'] = teambib
            userinfo['TeamID'] = teaminfo[0]['id']

    print('eventid->' , eventid, 'Bib->', teambib)
    if  (teambib == '') or ( teambib is None) :
        return render(request, 'root/base.html')

    selected_team_info = [] # this is value of team selected, 
    editmode = False
    Teammodel = {}    
    print('here 14')
    Teammodel = Team.objects.filter(EventID_id=int(eventid), Bib=int(teambib) ).all()
    print(Teammodel, 'this is team model----->>>>')
    # Get team info
    if Teammodel:
        selected_team_info = tir.get_Team_model_to_json(Teammodel)
        print(selected_team_info, '<error>==> this is selected team id')
       
    if len(selected_team_info) == 0 :
        return render(request, 'root/base.html')

    teamid = selected_team_info[0]['id']
   
    if request.user.runnerid == selected_team_info[0]["CaptainID"]:
        iscaptain = True
        userinfo['iscaptain'] = True
        ismyteam = True
        userinfo['ismyteam'] = True

    if ('edit' in request.GET) and (ismyteam or admin):
        editmode = True
        userinfo['editmode'] = True
    else:
        editmode == False
        userinfo['editmode'] = False
   
    if ('edit' in request.GET) and not editmode:
        return render(request, 'root/base.html')

    if userinfo['editmode'] and userinfo['iscaptain']:
        userinfo['is_editmode_and_iscaptain_or_admin'] = True

    if userinfo['editmode'] and userinfo['admin']:
        userinfo['is_editmode_and_iscaptain_or_admin'] = True

    if selected_team_info[0]['IsUntimed'] == 1:
        userinfo['teaminfo_or_edit_iscaption_admin'] = True
    
    if userinfo['editmode'] and userinfo['iscaptain'] :
        userinfo['teaminfo_or_edit_iscaption_admin'] = True
    if userinfo['editmode'] and  request.user.is_superuser:
        userinfo['teaminfo_or_edit_iscaption_admin'] = True

    opinions = {} 
    opinions['class'] = '<option value="Open">Open</option><option value="Masters">Masters</option><option value="Veterans">Veterans</option><option value="Corporate">Corporate</option><option value="Military">Military</option>'
    opinions['type'] ='<option value="Men">Men</option><option value="Mixed">Mixed</option><option value="Women">Women</option>'
    opinions['sock'] = '<option value="WM" >Womens M</option><option value="WS" >Womens S</option><option value="WL" >Womens L</option><option value="WXL" >Womens XL</option><option value="MS" >Mens Small</option><option value="MM" >Mens Medium</option><option value="ML" >Mens Large</option><option value="MXL" >Mens XL</option><option value="MXXL" >Mens XXL</option>'
    opinions['shirt'] ='<option value="XL-L">Mens 9 & up</option><option value="S-M">Mens 8 & down</option>'
    opinions['pace'] = '<option value="300">5:00</option><option value="315">5:15</option><option value="330">5:30</option>	<option value="345">5:45</option><option value="360">6:00</option><option value="375">6:15</option><option value="390">6:30</option>	<option value="405">6:45</option><option value="420">7:00</option><option value="435">7:15</option><option value="450">7:30</option>	<option value="465">7:45</option><option value="480">8:00</option><option value="495">8:15</option><option value="510">8:30</option>	<option value="525">8:45</option><option value="540">9:00</option><option value="555">9:15</option><option value="570">9:30</option>	<option value="585">9:45</option><option value="600">10:00</option><option value="615">10:15</option><option value="630">10:30</option>	<option value="645">10:45</option><option value="660">11:00</option><option value="675">11:15</option><option value="690">11:30</option>	<option value="705">11:45</option><option value="720">12:00</option><option value="735">12:15</option><option value="750">12:30</option>	<option value="765">12:45</option>'
 

    runnerinfo = []
    temprunnerinfo = []
    
  
    numRunnermodelC = Runner.objects.raw('Select r.id,r.FirstName,r.LastName,r.Email,r.Phone,r.Pace,r.Gender,r.ShirtSize,r.SockSize,r.IsPaid,r.PaidAmount From lonestar_runner r Inner Join `lonestar_team` t ON t.id = r.TeamID_id Where r.TeamID_id = ' + str(teamid) +' and r.IsDeleted = 0 and ((t.IsSplitPayment = 1 and r.IsPaid = 1) or (t.IsSplitPayment = 0 and t.IsPaid = 1)) order by id')
    print(numRunnermodelC, 'this is join model...------------------->>>>>>>>>')
  
    if numRunnermodelC:
        runnerinfo = tir.get_Runner_innder_Team_and_promoitem_model_to_json(numRunnermodelC)
        print(runnerinfo, 'this is runners info')
        
        for a_runner in runnerinfo:
            temp = []
            temp = a_runner
            print(a_runner, ' this is runners of team ')
            isme = False
            if userinfo['RunnerID'] == a_runner['id']:
                isme = True
            temp['isme'] = isme

            editrunner = False
            if editmode and (userinfo['iscaptain'] or isme or admin):
                editrunner = True
            temp['editrunner'] = editrunner
            temp['dis_secs'] = displayTime(a_runner['Pace'])
            

            # join model
            orpjson = []
            query = "Select od.id, od.Num, pi.`Name` ItemDesc, COALESCE(od.Size,'') `Size` From lonestar_orderdetl od Inner Join `lonestar_order` o ON o.id = od.OrderID Inner Join lonestar_promoitem pi ON od.PromoItemID = pi.id	Where o.RunnerID = {0} and o.IsPaid = 1 ORDER BY od.id ".format(int(a_runner['id']))
         
            Orpmodel = OrderDetl.objects.raw(query)
            print(Orpmodel, 'this is model')
            if Orpmodel:
                orpjson = tir.get_ORP_model_to_json(Orpmodel)
            print(orpjson)
            if len(orpjson) is not 0:
                temp['tirgearitems'] = orpjson
            print(temp)
            temprunnerinfo.append(temp) 
            print(temprunnerinfo, 'this is temprunnerinfo ---- <<<(:)--| (:+:) |--(:)>>>')

    runnerinfo = temprunnerinfo
    print(runnerinfo, 'this is runner info')
    data = {
        'userinfo': userinfo, 'runnersinfo' : runnerinfo, 'cur_team_info' : selected_team_info, 'optionlist' : opinions 
    }
 
    return render(request, 'team/content.html', data)






# calc Fee Interval Function
def calc_FeeInterval(request):
    print('= calc _fee')
    
    teamClass = request.POST.get('teamClass')
    payStyle = request.POST.get('payStyle')
    newCode = request.POST.get('newCode')
    curCode = request.POST.get('curCode')
    promoItemsId = request.POST.get('promoItemsId')
    promoItemsNum = request.POST.get('promoItemsNum')
    promoItemsSize = request.POST.get('promoItemsSize')
    joinCode = request.POST.get('joinCode', 0)

    print('request getinfo -- > : ->', teamClass, payStyle, newCode, curCode, promoItemsId, promoItemsNum, promoItemsSize, joinCode)
    
    promos = tir.get_string_to_json(promoItemsId, promoItemsNum, promoItemsSize)

    print( teamClass, payStyle, newCode, curCode, promos, joinCode )
    fee = tir.calc_FeeIntervalfn( teamClass, payStyle, newCode, curCode, promos, joinCode)
    print('fee calc=> data', fee)
    return JsonResponse({'valid': True, 'ret' : fee }, status=200)


def do_Save_Pay(request):
    #  get request data.
    formdata = {}
    formdata['first'] = request.GET.get('first')
    formdata['last'] = request.GET.get('last')
    formdata['email'] = request.GET.get('email')
    formdata['phone'] = request.GET.get('phone')
    formdata['newCode'] = request.GET.get('newCode')
    formdata['discount'] = request.GET.get('discount')
    
    formdata['street'] = request.GET.get('street')
    formdata['city'] = request.GET.get('city')
    formdata['usstate'] = request.GET.get('usstate')
    formdata['zip'] = request.GET.get('zip')
    formdata['dob'] = request.GET.get('dob')
    formdata['tenkpace'] = request.GET.get('tenkpace')
    formdata['gender'] = request.GET.get('gender')
    formdata['pw'] = request.GET.get('pw')
    formdata['teamName'] = request.GET.get('teamName')
    formdata['teamSong'] = request.GET.get('teamSong')
    formdata['teamType'] = request.GET.get('teamType')
    formdata['teamClass'] = request.GET.get('teamClass')
    formdata["fee"] = request.GET.get('fee')
    
    print(formdata['fee'], 'this value is value of form data by start')
    if formdata["fee"] is None:
        formdata["fee"] = 0
    formdata['hasReleased'] = request.GET.get('hasReleased')
    formdata['payStyle'] = request.GET.get('payStyle')
    formdata['isUntimed'] = request.GET.get('isUntimed')
    formdata['joinCode'] = request.GET.get('joinCode')
    
    # please get promose data stringified.
    formdata['promoItemsId'] = request.GET.get('promoItemsId')
    formdata['promoItemsNum'] = request.GET.get('promoItemsNum')
    formdata['promoItemsSize'] = request.GET.get('promoItemsSize')
    formdata['referredbyentity'] = request.GET.get('referredbyentity')
    formdata['referredbyperson'] = request.GET.get('referredbyperson')
    formdata['shirtsize'] = request.GET.get('shirtsize')
    formdata['socksize'] = request.GET.get('socksize')
    formdata['is_user'] = False
  
    print(formdata, 'this is data of html in frontend')
    
    promos = tir.get_string_to_json(formdata['promoItemsId'], formdata['promoItemsNum'], formdata['promoItemsSize'])
    print(promos)
    
    formdata['promoItems'] = promos
    ret = {}
    ret["success"] = False
    ret["ErrorMessage"] = ""
    freeEntry = 0
    ret['loginstate'] = False
    error = ""
    if request.user.is_authenticated:
        formdata['is_user'] = True
        # ret['loginstate'] = True

    eventid = tir.get_Event_Id()
   
    if not eventid:
        error = "Internal error finding current event. Try again."
        
    if formdata["socksize"] is None :
        formdata["socksize"] = ''
    
    if formdata["payStyle"] == "":
        error = "Pay Style is required."
    
    if error != "":
         ret["ErrorMessage"] = error
    if formdata["discount"] == None and formdata["discount"] == '':
        formdata["discount"] = 0

    ret["item"] = str(formdata["teamName"]) + " - " + str(formdata["first"]) +  " " + str(formdata["last"])
    # get correct pricing
    if ret["ErrorMessage"] == "":
    
        print(formdata["teamClass"], formdata["payStyle"], formdata['newCode'], formdata["discount"], formdata["promoItems"], formdata["joinCode"],'------98776568700--=')
        fees = tir.calc_FeeIntervalfn(formdata["teamClass"], formdata["payStyle"], formdata['newCode'], formdata["discount"], formdata["promoItems"], formdata["joinCode"])
        
        print(fees, 'this is fee value')
        if fees["codeApplied"]:
            calcFee = fees["newFee"] + fees["promoCost"] * 1
        else:
            calcFee = fees["fee"] + fees["promoCost"] * 1
        print(calcFee,'-', formdata["fee"] * 1)

        if str(calcFee) != str(formdata['fee']):
            ret["ErrorMessage"] = "Fees were not added up correctly. Please try again."
        else:
            ret["fee"] = calcFee
            if calcFee == 0:
                freeEntry = 1
    # please define none type value
    _discount = ''
    if formdata["discount"] is not None:
        _discount = formdata["discount"]

    _teamName = ''
    if formdata["teamName"] is not None:
        _teamName = formdata["teamName"]

        
    _teamSong = ''
    if formdata["teamSong"] is not None:
        _teamSong = formdata["teamSong"]
    
    _teamType = ''
    if formdata["teamType"] is not None:
        _teamType = formdata["teamType"]

    _teamClass = ''
    if formdata["teamClass"] is not None:
        _teamClass = formdata["teamClass"]  

    if formdata["joinCode"]:
        joincode = formdata["joinCode"]
    else:
        joincode = 0

    print(joincode, 'request join code')

    print('team create is not still start.')
    teamid = 0
    if ret["ErrorMessage"] == "" and  (joincode != 0) :
       
        bib = 0
        # please recode team from register.
        if formdata["payStyle"] == "indiv":
            isSplit = 1
        else:
            isSplit = 0
        if formdata["isUntimed"] == "true":
            isUntimed = 1
        else:
            isUntimed = 0

        if formdata["payStyle"] == "full" and freeEntry == 1:
            isPaid = 1
        else:
            isPaid = 0
  
        _T = Team(EventID_id=int(eventid),Bib=int(0),DiscountCode=_discount,IsSplitPayment=int(isSplit),IsPaid=int(isPaid),PaidAmount=int(0),CaptainID=int(0),ExpectedPace=int(0),JoinCode=0 ,Name=_teamName,Song=_teamSong,Type=_teamType,Classification=_teamClass,IsUntimed=isUntimed)
        _T.save()
        teamid = CurrentTeams.objects.filter(Name=str(formdata["teamName"])).order_by('-ID').first().pk
       
    
    teamType = ""
    if ret["ErrorMessage"] == '' and joincode == "0" and teamid == 0:
        ret["ErrorMessage"] = "Unknown error locating your team record."
    elif teamid == 0:
        try:
            teammodel = CurrentTeams.objects.filter(JoinCode=str(joincode))
            team = tir.get_CurrentTeams_model_to_json(teammodel)
            teamid = team[0]['id']
            teamType = team[0]['Type']
           
        except:
            ret["ErrorMessage"] = "The Team does not exist." 

    print(teamid, teamType, ' team id and team name')
    if ret["ErrorMessage"] == "" and teamid == 0:
        ret["ErrorMessage"] = "Unable to locate your team using the teamid."

    # ensure team has space for this runner
    if ret["ErrorMessage"] == "":
        # try:
        is_full = get_membersOfteam(teamid)
        if is_full:
            ret["ErrorMessage"] = "Team is already maxed out at 12 runners."

        elif teamType == "Women" and formdata["gender"] != "F":
            ret["ErrorMessage"] = "This is a female team. Please correct your gender."

    # save runner record
    runnerid = 0
    if ret["ErrorMessage"] == "":
        
        query = "Select r.id From `lonestar_runner` r Inner Join `lonestar_team` t ON t.id = r.TeamID_id Where (t.IsPaid = 1 or r.IsPaid = 1) and (r.Email = {0}) and (r.IsDeleted = 0) and (t.EventID_id = {1})".format(formdata["email"], int(eventid))
        print("\n",query,'this is join lonestar query 1 2')
     
        numRunnermodelB = Runner.objects.raw(query)
        print(numRunnermodelB)
        if len(numRunnermodelB):
            numRunner = tir.get_Runner_model_to_json(numRunnermodelB)
            runnerid = numRunner[0]['id']
    
        if runnerid != 0:
            ret["ErrorMessage"] = "Your email is already associated with a runner on a registered team."
        else:
            # try:
            hashpwd = make_password(formdata["pw"])
            if formdata["payStyle"] == "indiv" and freeEntry == 1:
                isPaid = 1
            else:
                isPaid = 0
            print(formdata["shirtsize"])
            _R = Runner(TeamID_id=int(teamid),FirstName=str(formdata["first"]),LastName=str(formdata["last"]),Email=str(formdata["email"]),Phone=str(formdata["phone"]),Street=str(formdata["street"]),City=str(formdata["city"]),State=str(formdata["usstate"]),Zip=formdata["zip"] ,ReferredByEntity=str(formdata["referredbyentity"]),ReferredByPerson=str(formdata["referredbyperson"]),DOB=str(formdata["dob"]),Pace=formdata["tenkpace"],Gender=formdata["gender"], ShirtSize=str(formdata["shirtsize"]), IsDeleted=int(0) ,SockSize=str(formdata["socksize"]),PassHash=str(hashpwd),IsPaid=int(isPaid),PaidAmount=int(0),RulesAgreedCST=today, DeviceToken=0)
            _R.save()
           
        
            try:
                runnerid = Runner.objects.filter( Email=formdata["email"],TeamID_id=int(teamid), IsDeleted=int(0)).order_by('-id').first().id
            except:
                ret["ErrorMessage"] = "SQL Error saving runner data: "
        
    
    if ret["ErrorMessage"] == "" and runnerid == 0:
        ret["ErrorMessage"] = "Unable to save your runner information."
    
    if ret["ErrorMessage"] == "" and joincode == 0:
        
        try:
            Team.objects.filter(id=teamid).update(CaptainID=runnerid)
        except:
            ret["ErrorMessage"] = "SQL Error saving captain info: "
    
    # save promo item records
    if len(formdata["promoItems"]) > 0:
       
        if ret["ErrorMessage"] == "":
            _O = Order(IsDelivered = int(0), RunnerID = runnerid, IsPaid = int(0),PaidAmount = int(0))
            _O.save()
           
        orderid = 0
        if ret["ErrorMessage"] == "":
           
            ordermodel = Order.objects.filter(RunnerID=runnerid, IsPaid=int(0)).order_by('-id')[0:1]
            if len(ordermodel):
                orderdb = tir.get_Order_model_to_json(ordermodel)
                print(orderdb)
                orderid = orderdb[0]['id']
           
        madePromoOrder = False
        if ret["ErrorMessage"] == "" and orderid > 0:
            for childpromo in formdata["promoItems"]:
                if int(childpromo["Num"]) > 0:
                   
                    _Od = OrderDetl(OrderID=int(orderid),PromoItemID=int(childpromo["Id"]),Num=int(childpromo["Num"]),Size=childpromo["Size"])
                    _Od.save()
                    madePromoOrder = True
                  
        if madePromoOrder == False:
            try:
                Order.objects.filter(id=int(orderid)).delete()
            except:
                ret["ErrorMessage"] = "SQL Error saving order delete data: 17->" 


    userinfo = False
    if ret["ErrorMessage"] == "":
        ret["success"] = True
        ret["teamid"] = teamid
        ret["runnerid"] = runnerid
        if formdata["payStyle"] == "full":
            ret["teampay"] = 1
        else:
            ret["teampay"] = 0

        if joincode == 0:
            ret["newteam"] = 1
        else:
            ret["newteam"] = 0

        ret["orderid"] = orderid
       
        print(formdata["email"], formdata["pw"], runnerid)
       
        signUpfn(formdata["email"], str(formdata["first"]) + " " + str(formdata["last"]), formdata["pw"], runnerid , request)
       

    
    if ret["ErrorMessage"] == "" and  (fees is not None) and fees["codeApplied"]:
        try:
            DiscountCode.objects.filter(Code=fees["codeApplied"]).update(NumUsesCompleted=F('NumUsesCompleted') + 1)
        except:
            ret["ErrorMessage"] = "SQL Error updata DiscountCode data"

    ret["proc"] = "saveAndPay"
    
    return JsonResponse({'valid': True, 'ret': ret, "loginstate" : 'success'}, status=200)
   



# this dbapi.php file saveanypay function is cloned
# @login_required, 

def go_Tirgear(request):

    data = {
        "event_year" : today.year,
        'currentteam' : "",
        'event' : '',
        'userteaminfo' : '',
        # "state_list" : tir.get_state_list()
    }
    currentteam = ''
    eventid = tir.get_Event_Id()
    event = tir.get_Event()
    # event = Event.objects.filter(DateHeld__lte = today )
    for e in event:
        print(e)
    data['event'] = event
    # eventjson =  serializers.serialize('json', event)
    # if event and event[0].pk :
    #     print(event[0],'==', event[0].pk, 'eventid------------')
    #     data['event'] = event
    
    jsonprmoitems = []
    Items = PromoItem.objects.filter(IsActive = 1 ).order_by('id')
    print(Items, '232------------------------232 promo items-----------------')
    if Items:
        jsonprmoitems = tir.get_PromoItem_model_to_json(Items)
        data['promoitems'] = jsonprmoitems
       
    userteaminfo = {
        "teamName":"",
        "teamSong":"",
        "teamType":"mixed",
        "teamClass":"open",
        "teamUntimed":'0',
        "teamPayStyle":"full",
        "teamBib": "",
        "iscaptain" : True,
        'joinCode' : 0
    }
    data['userteaminfo'] = userteaminfo
  
    if request.user.is_authenticated:
      
        if event and eventid :
            data['currentteam'] = tir.get_teaminfoofuser(request.user.runnerid)
            print(currentteam, 'current team info')

    print(data)
    return render(request, 'tirgear/content.html', { "data": data })


def getsaveAndPayTIRGear(request):
    ret = {
        "success": False,
        "fee" : 0,
        'ErrorMessage' : ''
    }
    runnerid = request.user.runnerid
    formdata = {}
    formdata['fee'] = request.GET.get('fee')
    payment_method_nonce = request.POST.get("payment_method_nonce")
    formdata['promoItemsId'] = request.GET.get('promoItemsId')
    formdata['promoItemsNum'] = request.GET.get('promoItemsNum')
    formdata['promoItemsSize'] = request.GET.get('promoItemsSize')
    promos = tir.get_string_to_json(formdata['promoItemsId'], formdata['promoItemsNum'], formdata['promoItemsSize'])
    formdata['promoItems'] = promos
    print(formdata)

    if ret["ErrorMessage"] == "":
        try:
            _O = Order(IsDelivered=int(0),RunnerID=int(runnerid),IsPaid=0,PaidAmount=int(0))
            _O.save()
        except:
            ret["ErrorMessage"] = "SQL Error saving order data: "
    orderid = None
    jsonorder = ''
    if ret["ErrorMessage"] == "":
       
        ordermodel = Order.objects.filter(RunnerID = int(runnerid)).order_by('id')
      
        if len(ordermodel):
            jsonorder = tir.get_Order_model_to_json(ordermodel)
            orderid = jsonorder[0]['id']
      
    madePromoOrder = False
    if ret["ErrorMessage"] == "" and orderid is not None:
            for promo in formdata["promoItems"]:
                print(promo,' this is promo value')
                if promo['Num'] is not 0 and promo['Num'] is not '':
                    try:
                        _Od = OrderDetl(OrderID=int((orderid)),PromoItemID=promo["Id"],Num=promo["Num"],Size=promo["Size"])
                        _Od.save()
                        madePromoOrder = True
                    except:
                        ret["ErrorMessage"] = "SQL Error saving promo order: "
                        madePromoOrder = False


    if madePromoOrder == False and orderid is not None:
        try:
            Order.objects.filter(id=int(orderid)).delete()
        except:
            ret["ErrorMessage"] = "SQL Error saving order data: 3"
    eventid = tir.get_Event_Id()
    currentteam = ''
    if  eventid :
        currentteam = tir.get_teaminfoofuser(runnerid)
        print(currentteam, 'current team info')
   
    if ret["ErrorMessage"] == "":
        ret["success"] = True
        ret["runnerid"] = runnerid
        ret["orderid"] = orderid
        ret["item"] = str("TIR Gear: Team ") + str( currentteam[0]["Bib"]) + ", Runner " + str( request.user.username )
        ret["fee"] = formdata["fee"]

    ret["proc"] = "saveAndPayTIRGear"

    teamid = currentteam[0]['id']
    transaction = Transactions(Runner = runnerid,Teamid = teamid,Email = request.user.email, Amount = formdata['fee'], PaymentMethod = 'paypal', Status = 1, Description = "Tir Gear", PayDate = today )
    transaction.save()
    gateway = braintree.BraintreeGateway(access_token=paypal_access_token)
    result = gateway.transaction.sale({
        "amount" : formdata['fee'],
        "merchant_account_id": "USD",
        "payment_method_nonce" : payment_method_nonce,
        "options" : {
          "paypal" : {
            "custom_field" : "PayPal custom field",
            "description" : "Tir Gear"
          },
        }
    })
    
    if result.is_success:
        Order.objects.filter(id=int(ret["orderid"])).update(IsPaid = int(1), PaidAmount=int(ret["fee"]))
        return JsonResponse({'statusCode': '1', 'data': ret }, status=200)
        
    return JsonResponse({'statusCode': '2', 'data': ret }, status=200 )


def updateOrder(request):
    orderid_ = request.GET.get('orderid')
    runnerid_ = request.user.runnerid
    amount_ = request.GET.get('fee')
    
    Order.objects.filter(id=int(orderid_)).update(IsPaid = int(1), PaidAmount=int(amount_))

    return JsonResponse({'statusCode': '2', 'data': ret }, status=200 )




def update_Team(request):
    ret = {
        "success": False,
        "ErrorMessage" : ''
    }
    runnerid = request.user.id
    formdata = {}
  
    formdata['teamid'] = request.GET.get('teamid')
    formdata['teamName'] = request.GET.get('teamName', '')
    formdata['teamSong'] = request.GET.get('teamSong', '')
    formdata['teamType'] = request.GET.get('teamType', '')
    formdata['teamUntimed'] = request.GET.get('teamUntimed', '')
    formdata['teamClass'] = request.GET.get('teamClass', '')
  
    formdata['r_id'] = request.GET.get('r_id')
    formdata['r_pace'] = request.GET.get('r_pace')
    formdata['r_sock'] = request.GET.get('r_sock')
    formdata['r_shirt'] = request.GET.get('r_shirt')
    formdata['r_phone'] = request.GET.get('r_phone')
    formdata['r_email'] = request.GET.get('r_email')
    formdata['runners'] = strToArrayfn(formdata['r_id'], formdata['r_pace'], formdata['r_phone'], formdata['r_email'],  formdata['r_shirt'],  formdata['r_sock'])

    success = True
    error = ""
    if formdata["teamName"] != '':
        Team.objects.filter(id=formdata['teamid']).update(Name=formdata["teamName"],Song=formdata["teamSong"], Type=formdata["teamType"], Classification=formdata["teamClass"], IsUntimed=formdata["teamUntimed"] )
   
    if success == True:
        ids = ""
        for runner in formdata["runners"]:
         
            if ids is None or ids == '' or ids == ' ':
                ids = str(ids) + '' + str(runner["recid"])
            else:
                ids = str(ids) + ' or ' + str(runner["recid"])
            if runner["pace"] is not "":
                try:
                    Runner.objects.filter(id=int(str(runner["recid"])), ).update(Pace=runner["pace"],ShirtSize=str(runner["shirt"]),SockSize=str(runner["sock"]), Phone=str(runner["phone"]), Email=runner["email"])
                    success = True
                except:
                    error = "Failed to save runner with email: " + str(runner["email"]) + ". Please try again.19"
                    success = False
            if not success:
                break
    
    if success and ids is not "":
        try:
         
            query = "Update lonestar_runner Set IsDeleted=1 Where TeamID_id={0} and id IN ({1})".format( formdata['teamid'] , ids)
         
            Runner.objects.raw(query)
            success = True
        except:
            success = False
            error = " Member Of Team info Error"
    
    if success:
        ret['success'] = True
    else:
        ret["ErrorMessage"] = error
                
    ret["proc"] = "updateteam"

    return JsonResponse({'valid': True, 'ret': ret}, status=200)


def paymentPaypal(request):
    runnerid = request.user.runnerid
    teamid = request.POST.get('teamid')
    payment_email = request.user.email
    amount = request.POST.get('amount')
    payment_method_nonce = request.POST.get("payment_method_nonce")
    payment_method = 'paypal'
    status = 1
    description = request.POST.get('description')
    if request.method == 'POST':
        transaction = Transactions(
            Runner = runnerid,
            Teamid = teamid,
            Email = payment_email,
            Amount = amount,
            PaymentMethod = payment_method,
            Status = status,
            Description = description,
            PayDate = today
        )
        transaction.save()
    gateway = braintree.BraintreeGateway(access_token=paypal_access_token)
    result = gateway.transaction.sale({
        "amount" : amount,
        "merchant_account_id": "USD",
        "payment_method_nonce" : payment_method_nonce,
        "options" : {
          "paypal" : {
            "custom_field" : "PayPal custom field",
            "description" : description
          },
        }
    })
    if result.is_success:
        return JsonResponse({'statusCode': '1'})
        
    return JsonResponse({'statusCode': '2'})


def get_RandJoinCode():
    
    i = int(1)  
    newcode = ''
    get_ = False
    while True:  
        newcode = random.randint(100000,999999)
        print(newcode)  
        counter = Team.objects.filter(JoinCode=newcode).count()
        counter = Team.objects.filter(JoinCode=newcode).count()
        if not counter:
            get_ = True
        i = i + 1  
        if( i > 50 or get_ ):  
            break  
    return newcode


def active_Team_Runner(request):
   
    amount = request.POST.get('amount')
    # runnerid = request.user.runnerid
    runnerid = request.POST.get('invoice')
    toemail = request.user.email
    teamid  = request.POST.get('teamid')
    teampay = request.POST.get('teampay')
    newteam  = request.POST.get('newteam')
    orderid  = request.POST.get('orderid')
    status = 1 
    if teampay == 1 and newteam == 1:
        Runner.objects.filter(id=runnerid).update(Ispaid=int(1), PaidAmount=amount)
    
    if orderid != None and orderid == '':
        Order.objects.filter(id=orderid).update(IsPaid=int(1))

    joincode_ =  get_RandJoinCode()
   
    
    if int(newteam) == int(1):
        Team.objects.filter(id=teamid).update(JoinCode=joincode_, Bib=F('id')-1000)
    
    data = tir.get_user_info(runnerid)
   
    iscaptainid = data['team'][0]["CaptainID"]
   
    current_site = get_current_site(request)
    if iscaptainid != runnerid:
        message = "Thanks so much for registering for the 2020 Texas Independence Relay - You and your team will have a GREAT time!  If you have any questions or concerns, please feel free to contact us any time by emailing jay@TexasIndependenceRelay.com or by calling 512.716.5041.  We look forward to seeing you out on the course over March 28-29th, 2020!<br><br>Please invite your teammates by sending them the following link: <a href=\""+ str(current_site) + "/register/" + str(joincode_) + "\">"+ str(current_site) + "/register/" + str(joincode_) + "</a><br>"
    else:
        message = "Thanks so much for registering for the 2020 Texas Independence Relay!  If you have any questions or concerns, please feel free to contact us any time by emailing jay@TexasIndependenceRelay.com or by calling 512.716.5041.  We look forward to seeing you out on the course over March 28-29th, 2020!<br>"
    message = message + "<br>Thanks again, <br>Jay and Joy <br>Lone Star Relays <br>512.716.5041"
   
    success = True
    if success:
        return JsonResponse({'valid' : True}, status=200)
    return JsonResponse({'valid' : False}, status=200)


