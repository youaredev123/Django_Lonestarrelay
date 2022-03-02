import requests
import json
import os
import csv
from base64 import b64encode
import urllib.parse
from lonestar.models import User, Event, Team, PromoItem, RegPrice, DiscountCode, TeamStats, Runner, currentevent, currentorders, currentrunners, CurrentTeams, currentrosterinfo
from django.core import serializers
import math
from datetime import datetime
import pytz
from django.db.models import Q, F
today = datetime.now().replace(tzinfo=pytz.UTC).date()   # tz aware datetime object


def get_Event():
    eventmodel = currentevent.objects.all()
    jsonitems = []
    for i, item in enumerate(eventmodel):
        Item_one = {}
        Item_one['id'] = getattr(item, 'id')
        Item_one['DateHeld'] = getattr(item, 'DateHeld')
        Item_one['NextStatsUpdate'] = getattr(item, 'NextStatsUpdate')
        jsonitems.append(Item_one)

    return jsonitems

def get_Event_Id():
    event = currentevent.objects.all()
    eventjson =  serializers.serialize('json', event)
    if len(eventjson):
        try:
            print(event[0].pk)
            if event and event[0].pk :
                print( event[0].pk, 'eventid------------')
                return event[0].pk
            else:
                return False
        except:
            return False
    
    return False
def get_teaminfoofuser(id):
    teaminfo = []
    Runnermodel = Runner.objects.filter(id=int(id), IsDeleted=0)
    if Runnermodel:
        jsonRunner = get_Runner_model_to_json(Runnermodel)
        print(jsonRunner)
        teamid = jsonRunner[0]['TeamID_id']
        teambibmodel = Team.objects.filter(id=int(teamid) ).all()
        print(teambibmodel, 'this is team model----->>>>')
        if teambibmodel:
            teaminfo = get_Team_model_to_json(teambibmodel)
            print(teaminfo)
    return teaminfo

def get_state_list():
    state_list = {
        "alabama":"AL",
        'alaska':"AK",
        'arizona':"AZ",
        'arkansas':"AR",
        'california':"CA",
        'colorado':"CO",
        'connecticut':"CT",
        'delaware':"DE",
        'florida':"FL",
        'georgia':"GA",
        'hawaii':"HI",
        'idaho':"ID",
        'illinois':"IL",
        'indiana':"IN",
        'iowa':"IA",
        'kansas':"KS",
        'kentucky':"KY",
        'louisiana':"LA",
        'maine':"ME",
        'maryland':"MD",
        'massachusetts':"MA",
        'michigan':"MI",
        'minnesota':"MN",
        'mississippi':"MS",
        'missouri':"MO",
        'montana':"MT",
        'nebraska':"NE",
        'nevada':"NV",
        'new hampshire':"NH",
        'new jersey':"NJ",
        'new mexico':"NM",
        'new york':"NY",
        'north carolina':"NC",
        'north dakota':"ND",
        'ohio':"OH",
        'oklahoma':"OK",
        'oregon':"OR",
        'pennsylvania':"PA",
        'rhode island':"RI",
        'south carolina':"SC",
        'south dakota':"SD",
        'tennessee':"TN",
        'TEXAS':"TX",
        'utah':"UT",
        'vermont':"VT",
        'virginia':"VA",
        'washington':"WA",
        'west virginia':"WV",
        'wisconsin':"WI",
        'wyoming':"WY"
    }
    return state_list



def applyCode(curFee, codeRow):
    if codeRow["Type"] == "PercentOff":
        return curFee * ((100 - int(codeRow["Value"])) / 100 )
    elif codeRow["Type"]=="DollarsOff":
        return (curFee - codeRow["Value"])
    elif codeRow["Type"] == "TotalCost":
        return (1.0 * codeRow["Value"])
    else:
    	return curFee 

def get_RegPrice_model_to_json(modeldata):
    jsonitems = []
    for i, item in enumerate(modeldata):
        Item_one = {}
        Item_one['id'] = getattr(item, 'id')
        Item_one['ThruDate'] = getattr(item, 'ThruDate')
        Item_one['IndFee'] = getattr(item, 'IndFee')
        Item_one['IndCorpFee'] = getattr(item, 'IndCorpFee')
        Item_one['TeamFee'] = getattr(item, 'TeamFee')
        Item_one['CorpFee'] = getattr(item, 'CorpFee')
        Item_one['EventID_id'] = getattr(item, 'EventID_id')
        jsonitems.append(Item_one)

    return jsonitems

def get_DiscountCode_model_to_json(modeldata):
    jsonitems = []
    for i, item in enumerate(modeldata):
        Item_one = {}
        Item_one['id'] = getattr(item, 'id')
        Item_one['Code'] = getattr(item, 'Code')
        Item_one['NumUsesAllowed'] = getattr(item, 'NumUsesAllowed')
        Item_one['NumUsesCompleted'] = getattr(item, 'NumUsesCompleted')
        Item_one['ValidThru'] = getattr(item, 'ValidThru')
        Item_one['Type'] = getattr(item, 'Type')
        Item_one['Value'] = getattr(item, 'Value')
        Item_one['AppliesTo'] = getattr(item, 'AppliesTo')
        Item_one['EventID_id'] = getattr(item, 'EventID_id')
        jsonitems.append(Item_one)

    return jsonitems
def get_PromoItem_model_to_json(modeldata):
    jsonitems = []
    for i, item in enumerate(modeldata):
        Item_one = {}
        Item_one['id'] = getattr(item, 'id')
        Item_one['Name'] = getattr(item, 'Name')
        Item_one['Cost'] = getattr(item, 'Cost')
        Item_one['IsActive'] = getattr(item, 'IsActive')
        Item_one['PaidAmount'] = getattr(item, 'PaidAmount')
        Item_one['Sizes'] = getattr(item, 'Sizes')
        jsonitems.append(Item_one)

    return jsonitems

def get_Team_model_to_json(modeldata):
    jsonitems = []
    for i, item in enumerate(modeldata):
        Item_one = {}
        Item_one['id'] = getattr(item, 'id')
        Item_one['Name'] = getattr(item, 'Name')
        Item_one['Bib'] = getattr(item, 'Bib')
        Item_one['DiscountCode'] = getattr(item, 'DiscountCode')
        Item_one['IsSplitPayment'] = getattr(item, 'IsSplitPayment')
        Item_one['PaidAmount'] = getattr(item, 'PaidAmount')
        Item_one['CaptainID'] = getattr(item, 'CaptainID')
        Item_one['ExpectedPace'] = getattr(item, 'ExpectedPace')
        Item_one['JoinCode'] = getattr(item, 'JoinCode')

        Item_one['Song'] = getattr(item, 'Song')
        Item_one['Type'] = getattr(item, 'Type')
        Item_one['Classification'] = getattr(item, 'Classification')
        Item_one['IsUntimed'] = getattr(item, 'IsUntimed')
        Item_one['StartTime'] = getattr(item, 'StartTime')
        Item_one['EventID_id'] = getattr(item, 'EventID_id')
        if getattr(item, 'IsSplitPayment') == 1:
            Item_one['teamPayStyle'] = "indev"
        else:
            Item_one['teamPayStyle'] = "full"

        # Item_one['Bib'] = getattr(item, 'Bib')
        # Item_one['teamInfoSet'] = True
        jsonitems.append(Item_one)

    return jsonitems

def get_CurrentTeams_model_to_json(modeldata):
    jsonitems = []
    for i, item in enumerate(modeldata):
        Item_one = {}
        Item_one['id'] = getattr(item, 'ID')
        Item_one['EventID_id'] = getattr(item, 'EventID')
        Item_one['Bib'] = getattr(item, 'Bib')
        Item_one['DiscountCode'] = getattr(item, 'DiscountCode')
        Item_one['IsSplitPayment'] = getattr(item, 'IsSplitPayment')
        Item_one['IsPaid'] = getattr(item, 'IsPaid')
        Item_one['PaidAmount'] = getattr(item, 'PaidAmount')
        Item_one['CaptainID'] = getattr(item, 'CaptainID')
        Item_one['ExpectedPace'] = getattr(item, 'ExpectedPace')
        Item_one['JoinCode'] = getattr(item, 'JoinCode')
        Item_one['StartTime'] = getattr(item, 'StartTime')
        Item_one['Name'] = getattr(item, 'Name')
        Item_one['Song'] = getattr(item, 'Song')
        Item_one['Type'] = getattr(item, 'Type')
        Item_one['Classification'] = getattr(item, 'Classification')
        Item_one['IsUntimed'] = getattr(item, 'IsUntimed')
        
        if getattr(item, 'IsSplitPayment') == 1:
            Item_one['PayStyle'] = "indev"
        else:
            Item_one['PayStyle'] = "full"
        jsonitems.append(Item_one)

    return jsonitems

def get_Runner_model_to_json(modeldata):
    jsonitems = []
    for i, item in enumerate(modeldata):
        Item_one = {}
        Item_one['id'] = getattr(item, 'id')
        Item_one['FirstName'] = getattr(item, 'FirstName')
        Item_one['LastName'] = getattr(item, 'LastName')
        Item_one['Email'] = getattr(item, 'Email')
        Item_one['Street'] = getattr(item, 'Street')
        Item_one['Phone'] = getattr(item, 'Phone')
        Item_one['City'] = getattr(item, 'City')
        Item_one['State'] = getattr(item, 'State')
        Item_one['Zip'] = getattr(item, 'Zip')
        Item_one['DOB'] = getattr(item, 'DOB')
        Item_one['Pace'] = getattr(item, 'Pace')
        Item_one['Gender'] = getattr(item, 'Gender')
        Item_one['ShirtSize'] = getattr(item, 'ShirtSize')
        Item_one['SockSize'] = getattr(item, 'SockSize')
        Item_one['PassHash'] = getattr(item, 'PassHash')
        Item_one['PaidAmount'] = getattr(item, 'PaidAmount')
        Item_one['RulesAgreedCST'] = getattr(item, 'RulesAgreedCST')
        Item_one['IsDeleted'] = getattr(item, 'IsDeleted')
        Item_one['ReferredByEntity'] = getattr(item, 'ReferredByEntity')
        Item_one['ReferredByPerson'] = getattr(item, 'ReferredByPerson')
        Item_one['PushToken'] = getattr(item, 'PushToken')
        Item_one['IsRoadie'] = getattr(item, 'IsRoadie')
        Item_one['DeviceToken'] = getattr(item, 'DeviceToken')
        Item_one['TeamID_id'] = getattr(item, 'TeamID_id')

        jsonitems.append(Item_one)

    return jsonitems



def get_currentrunner_model_to_json(modeldata):
    jsonitems = []
    for i, item in enumerate(modeldata):
        Item_one = {}
        Item_one['id'] = getattr(item, 'id')
        Item_one['FirstName'] = getattr(item, 'FirstName')
        Item_one['LastName'] = getattr(item, 'LastName')
        Item_one['Email'] = getattr(item, 'Email')
        Item_one['Street'] = getattr(item, 'Street')
        Item_one['Phone'] = getattr(item, 'Phone')
        Item_one['City'] = getattr(item, 'City')
        Item_one['State'] = getattr(item, 'State')
        Item_one['Zip'] = getattr(item, 'Zip')
        Item_one['DOB'] = getattr(item, 'DOB')
        Item_one['Pace'] = getattr(item, 'Pace')
        Item_one['Gender'] = getattr(item, 'Gender')
        Item_one['ShirtSize'] = getattr(item, 'ShirtSize')
        Item_one['SockSize'] = getattr(item, 'SockSize')
        Item_one['PassHash'] = getattr(item, 'PassHash')
        Item_one['PaidAmount'] = getattr(item, 'PaidAmount')
        Item_one['RulesAgreedCST'] = getattr(item, 'RulesAgreedCST')
        Item_one['IsDeleted'] = getattr(item, 'IsDeleted')
        Item_one['ReferredByEntity'] = getattr(item, 'ReferredByEntity')
        Item_one['ReferredByPerson'] = getattr(item, 'ReferredByPerson')
        Item_one['PushToken'] = getattr(item, 'PushToken')
        Item_one['IsRoadie'] = getattr(item, 'IsRoadie')
        Item_one['DeviceToken'] = getattr(item, 'DeviceToken')
        Item_one['TeamID'] = getattr(item, 'TeamID')

        jsonitems.append(Item_one)

    return jsonitems

def get_Order_model_to_json(modeldata):
    jsonitems = []
    for i, item in enumerate(modeldata):
        Item_one = {}
        Item_one['id'] = getattr(item, 'id')
        Item_one['IsDelivered'] = getattr(item, 'IsDelivered')
        Item_one['RunnerID'] = getattr(item, 'RunnerID')
        Item_one['IsPaid'] = getattr(item, 'IsPaid')
        Item_one['PaidAmount'] = getattr(item, 'PaidAmount')
        jsonitems.append(Item_one)

    return jsonitems


def displayTime(sec_):
    mins_ = math.floor(sec_ / 60)
    secs_ = math.floor(sec_ % 60)
    if secs_ < 10:
        secs_ = "0" + str(secs_)
    else:
        secs_ = str(secs_)
    return str( mins_ ) + ":" + secs_


def get_Runner_innder_Team_and_promoitem_model_to_json(modeldata):
    jsonitems = []
    for i, item in enumerate(modeldata):
      
        Item_one = {}
        Item_one['id'] = getattr(item, 'id')
        Item_one['FirstName'] = getattr(item, 'FirstName')
        Item_one['LastName'] = getattr(item, 'LastName')
        Item_one['Email'] = getattr(item, 'Email')
        Item_one['Phone'] = getattr(item, 'Phone')
        Item_one['Street'] = getattr(item, 'Street')
        Item_one['Pace'] = getattr(item, 'Pace')
        Item_one['Gender'] = getattr(item, 'Gender')
        Item_one['ShirtSize'] = getattr(item, 'ShirtSize')
        Item_one['SockSize'] = getattr(item, 'SockSize')
        Item_one['IsPaid'] = getattr(item, 'IsPaid')
        Item_one['PaidAmount'] = getattr(item, 'PaidAmount')
        Item_one['IsDeleted'] = getattr(item, 'IsDeleted')
        Item_one['IsPaid'] = getattr(item, 'IsPaid')
        # Item_one['IsSplitPayment'] = getattr(item, 'IsSplitPayment')
        print(Item_one)
        jsonitems.append(Item_one)

    return jsonitems


def get_ORP_model_to_json(modeldata):
    jsonitems = []
    for i, item in enumerate(modeldata):
        Item_one = {}
        Item_one['id'] = getattr(item, 'id')
        Item_one['Num'] = int(getattr(item, 'Num'))
        Item_one['ItemDesc'] = getattr(item, 'ItemDesc')
        Item_one['Size'] = int(getattr(item, 'Size'))
        
        jsonitems.append(Item_one)

    return jsonitems



def get_user_info(id):
    print(id, 'this is runnner id of user tbl')

    teamid = 0
    userinfo = {}
    user_runnerinfo = [] # insert user runnder info
    user_teaminfo = [] #  insert user team info
   
    Runnerusermodel = currentrunners.objects.filter(ID=id, IsDeleted=0).order_by('-ID')[0:1]
    print(Runnerusermodel, 'get_user_info function runner model.')
    if Runnerusermodel:
        user_runnerinfo = get_currentrunner_model_to_json(Runnerusermodel)
    
    print(user_runnerinfo)
   
    if len(user_runnerinfo):
        teamid = user_runnerinfo[0]['TeamID']

    print('teamid->', teamid)
    if teamid:
        teammodel = Team.objects.filter(id=teamid).order_by('-id')[0:1]
        print(teammodel,'this is user team model')
        if teammodel:
            user_teaminfo = get_Team_model_to_json(teammodel)
            print(user_teaminfo, 'this is user team info')
    userinfo = {
        'runner' : user_runnerinfo,
        'team' : user_teaminfo
    }
    return userinfo



def calc_FeeIntervalfn(teamClass, payStyle, newCode, curCode, promos, joinCode):
    print( teamClass, payStyle, newCode, curCode, promos, joinCode, '@')
    eventid = get_Event_Id()
    if not curCode :
        curCode = 0
    if not newCode :
        newCode = 0

    print( teamClass, payStyle, newCode, curCode, promos, joinCode)
    data = {}
    data['Evid'] = str(eventid)
    data['teamClass'] = teamClass
    data['payStyle'] = payStyle
    data['newCode'] = newCode
    data['curCode'] = curCode
    data['promos'] = promos
    data['joinCode'] = joinCode
    
    print(data, 'calculate Pay ')
    ret = {}
    ret['promoCost'] = 0
    ret['fee'] = 0
    codes = []
    # please set default.
    ret["codeApplied"] = False
    ret["ErrorMessage"] = ""
    classField = ""
    if data['teamClass'] == "Corporate":
        if data['payStyle'] == "full":
            classField = "CorpFee"
        else:
            classField = "IndCorpFee"
    else:
        if data['payStyle'] == "full":
            classField = "TeamFee"
        else:
            classField = "IndFee"
   
    if classField != "":
        paid = False
        if data['joinCode'] != "":
            resultscount = Team.objects.filter(JoinCode = int(data['joinCode']), IsPaid=1 ).count()
            if resultscount > 0:
                paid = True
            
        fee = ""
        if paid:
            fee = 0
            ret['fee'] = 0
            ret["success"] = True
        else:
        
            feedataofpricemodel = RegPrice.objects.filter( ThruDate__gte = today, EventID_id=int(eventid) ).order_by('ThruDate')[0:1]
            feedataofprice = get_RegPrice_model_to_json(feedataofpricemodel)
            # this part have to insert limit 1
         
            if len( feedataofprice) > 0:
                fee = feedataofprice[0][str(classField)]
                ret['fee'] = feedataofprice[0][str(classField)]
                ret["success"] = True
            
        if fee == "":
            ret["ErrorMessage"] = "The fee was not found for this scenario."

        if ret["ErrorMessage"] is not "":
            return ret 

        query = "Select id, Code,`Type`,Value,AppliesTo From lonestar_discountcode Where EventID_id='{0}' and (Code='{1}' or Code='{2}') and NumUsesAllowed > NumUsesCompleted and ValidThru >= CURDATE() order by id ".format(int(eventid), data["curCode"], data["newCode"])
      
        codeRow = DiscountCode.objects.raw(query)

       
        codes = get_DiscountCode_model_to_json(codeRow)
        if len(codes) > 0:
          
            if len(codes) == 1:
             
                newFee = applyCode(fee, codes[0])
            
                if newFee >= 0 and newFee < fee:
                    ret["codeApplied"] = codes[0]["Code"]
                    ret["newFee"] = newFee
            else:
                curIndex = 0
                if str(codes[0]["Code"]) == str(data["curCode"]):
                    curIndex = 1
                  
                newIndex = 1 - curIndex
                curNewFee = applyCode(fee, codes[curIndex])
                newNewFee = applyCode(fee, codes[curIndex])
                usedIndex = int(-1)
            
                if int(curNewFee) < 0 or int(curNewFee) >= fee:
                  
                    if int(newNewFee) >= 0 and int(newNewFee) < fee:
                        usedIndex = newIndex
                    else:
                        usedIndex = curIndex
                        
                if int(newNewFee) < 0 or int(newNewFee) >= int(fee):
                
                    usedIndex = int(curIndex)
                else:
                    if int(curNewFee) < int(newNewFee):
                    
                        usedIndex = int(curIndex)
                    else:
                        usedIndex = newIndex
                    
                
                if usedIndex > -1:
              
                    ret["codeApplied"] = codes[usedIndex]["Code"]
                    if usedIndex == curIndex:
                     
                        ret["newFee"] = curNewFee
                    else:
                        ret["newFee"] = newNewFee
                     
            if codes[0]["Code"] == "DATLON":
                if ret["fee"] > 0:
                    ret["codeApplied"] = codes[0]["Code"]
                    ret["newFee"] = 0.05
	
        
   
        if len(promos) > 0:
            sqlsuccess = False
            promoDB = []
            promoRow = PromoItem.objects.filter(IsActive = 1)
            if promoRow:
                promoDB = get_PromoItem_model_to_json(promoRow)
            else:
                ret["ErrorMessage"] = "SQL Error finding promo items "

            promoCost = int(0)
            for promoOrder in promos:
                promoFound = False
                for dbItem in promoDB:
                 
                    if int(promoOrder["Id"]) == dbItem["id"]:
                        promoFound = True
                        if promoOrder["Num"] == '':
                            promoOrder["Num"] = 0
                          
                        promoCost = promoCost * 1 + (1 * (dbItem["Cost"]) * int(promoOrder["Num"]) * 1)
                       
                if promoFound == False:
                    ret["promoMissing"] = True
            
            # this is exmples
            if len(codes) > 0 :
                if(codes[0]["Code"]=="DATLON" and promoCost>0) :
                    promoCost = 0
                    ret["codeApplied"] = codes[0]["Code"]

            ret["promoCost"] = promoCost
        else:
            ret["promoCost"] = 0
    print(ret)
    return ret

def get_string_to_json(a, b, c):
    json_List = []
    Ids = a.split(',')
    Nums = b.split(',')
    Sizes = c.split(',')
    l = 0
    for k in Ids:
        j = {}
        j['Id'] = Ids[l]
        j['Num'] = Nums[l]
        j['Size'] = Sizes[l]
        json_List.append(j)
        l = l + 1
    return json_List


def csv_downloadFileRoster(fileurl, sentences):
    with open(fileurl, 'a', encoding='utf-8') as csvfile:
        writeCSV = csv.writer(csvfile, delimiter=',', dialect='excel')
        writeCSV.writerow(["Team #", "Team Name", "Runner", "Gender", "Email", "Phone", "10KPace", "Street", "City", "State", "Zip", "DOB","ShirtSize","SockSize"])
        for sentence in sentences:
            writeCSV.writerow([sentence.TeamNumber, sentence.TeamName, sentence.Runner, sentence.Gender, sentence.Email, sentence.Phone, sentence.Pace, sentence.Street, sentence.City, sentence.State, sentence.Zip, sentence.DOB, sentence.ShirtSize, sentence.SockSize])
        csvfile.close()
    return os.path.basename(fileurl)



def csv_downloadFileTeams(fileurl, sentences):
    with open(fileurl, 'a', encoding='utf-8') as csvfile:
        writeCSV = csv.writer(csvfile, delimiter=',', dialect='excel')
        writeCSV.writerow(["Number", "Team Name", "JoinCode", "Captain", "Email", "Phone", "Type", "Class", "Song", "IsUntimed", "AvgPace", "# Runners"	,"MS","MM","ML","MXL","MXXL","WS","WM","WL","WXL","S-M","XL-L"])
        for sentence in sentences:
            writeCSV.writerow([sentence.TeamNumber, sentence.Name, sentence.JoinCode, sentence.Captain, sentence.Email, sentence.Phone, sentence.Type, sentence.Classification, sentence.Song, sentence.IsUntimed, sentence.AvgPace, sentence.NumRunners, sentence.MS, sentence.MM, sentence.ML, sentence.MXL, sentence.MXXL, sentence.WS, sentence.WM, sentence.WL, sentence.WXL, sentence.S_M, sentence.XL_L])
        csvfile.close()
    return os.path.basename(fileurl)



def csv_downloadFileTirgear(fileurl, sentences):
    with open(fileurl, 'a', encoding='utf-8') as csvfile:
        writeCSV = csv.writer(csvfile, delimiter=',', dialect='excel')
        writeCSV.writerow(["Team #", "Team Name", "Runner", "Gear", "Sizes", "Paid", "Shirt", "Sock", "Phone", "Email", "Street", "City", "State", "Zip"])
        for sentence in sentences:
            writeCSV.writerow([sentence.TeamNumber, sentence.TeamName, sentence.Runner, sentence.Gear, sentence.Sizes, sentence.Paid, sentence.ShirtSize, sentence.SockSize, sentence.Phone, sentence.Email, sentence.Street, sentence.City, sentence.State, sentence.Zip])
        csvfile.close()
    return os.path.basename(fileurl)