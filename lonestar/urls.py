from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('practicehome', views.go_pracicehome, name='practicehome'),
    path('generalinfo', views.go_GeneralInfo, name='generalinfo'),
    path('betahomepage', views.go_BetaHomePage, name='betahomepage'),
  
    # to mange log runner
    path('log_in/', views.log_In, name='log_In'),
    path('sign_up/', views.sign_Up, name ='sign_up'), 
    path('log_out/', views.log_Out, name='log_Out'),
    path('changepw/<str:pwd>', views.change_Password, name='changedpw'),
    path('forget_Pwd/', views.forget_PassWord, name='forget_Pwd'),
    path('account_activation_sent/', views.account_activation_sent, name='account_activation_sent'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    # register new runner, new team
    path('register/<str:getjoinCode>', views.do_register, name='register'),
    # path('auto_register/', views.auto_Register, name='auto_register'),
    path('check_email/', views.check_Email, name='check_email'),
    

    #  for admin.
    path('adminlogin/', views.do_adminlogin, name='adminlogin'),
    path('adminmanager/', views.go_AdminManager, name='adminmanager'),
    path('adminteams/', views.go_AdminTeams, name='adminteams'),
    path('adminroster/', views.go_AdminRoster, name='adminroster'),
    path('admintirgear/', views.go_AdminTirgear, name='admintirgear'),
    path('csvdownload/', views.do_CsvDownload, name='csvdownload'),




    # to calc fee in register page.
    path('calcfee/', views.calc_FeeInterval, name ='calc_fee'), 
    path('save_pay/', views.do_Save_Pay, name ='save_pay'), 
    path('payment-paypal/', views.paymentPaypal, name='payment-paypal'),
    path('active_team_runner/', views.active_Team_Runner, name='active_team_runner'),


    # get tir info, map, resource
    path('tirinfo/', views.get_TirInfo, name='tir_info'),
    path('map/', views.show_Map, name='map'),
    path('relayresources/', views.go_RelayResources, name='relayresources'),
   
    path('history/', views.go_History, name='history'),
    path('results/', views.get_Results, name='results'),
    path('resultsold/', views.get_ResultsOld, name='resultsold'),
    path('starttimeemail/', views.get_StartTimeEmail, name='starttimeemail'),
    
    path('videos/', views.get_Videos, name='videos'),
    path('2019results/', views.get_2019Results, name='2019results'),

    path('get2019resultinfo', views.get2019ResultInfo, name='get2019resultinfo'),
    path('saveAndPayTIRGear/', views.getsaveAndPayTIRGear, name='saveAndPayTIRGear'),
    path('update_order/', views.updateOrder, name='update_order'),
    

    path('individualplacement/', views.get_Individual_Placement, name='individual_placement'),
    path('team/', views.get_Team, name='team'),
    path('update_team/', views.update_Team, name='update_team'),
    path('tirgear/', views.go_Tirgear, name='tirgear'),
    path('tirgear_closed/', views.go_Tirgear_Closed, name='tirgear_closed'),
    path('downloads/', views.do_download, name='downloads'),
    path('faq/', views.go_faq, name='faq'),
    path('tictoctracking/', views.go_TicTocTracking, name='tictoctracking'),
    path('tictocresults/<str:id>', views.go_TicTocResults, name='tictocresults'),
    path('tictoctwo/', views.go_TicTocTwo, name='tictoctwo'),
    path('tictocmapversion/', views.go_TicTocMapVersion, name='tictocmapversion'),
    path('tictocexchangeform/', views.go_TicTocExchangeForm, name='tictocexchangeform'),
    
    
    path('openteams/', views.open_Teams, name='openTeams'),
    # path('tircourserecords/', views.go_TirCourseRecords, name='tir_course_records'),


    path('tirresource/', views.get_Tirresource, name='tir_resource'),
    path('merchandise/', views.get_Merchandise, name='merchandise'),

    path('privacy_policy/', views.show_Privacy_Policy, name='privacy_policy'),

]