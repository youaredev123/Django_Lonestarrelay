from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime


from django.db import migrations

class User(AbstractUser):
    runnerid = models.IntegerField(default=False, )
    @property
    def get_runnerid(self):
        return self.runnerid
    def __str__(self):
        return self.username

class Event(models.Model):
    DateHeld = models.DateField(auto_now_add=True)
    NextStatsUpdate = models.DateTimeField(auto_now_add=True)

class Team(models.Model):
    EventID = models.ForeignKey(Event, on_delete=models.CASCADE)
    Bib = models.IntegerField()
    DiscountCode = models.TextField(max_length=200)
    IsSplitPayment = models.IntegerField()
    IsPaid = models.IntegerField()
    PaidAmount = models.IntegerField()
    CaptainID = models.IntegerField()
    ExpectedPace = models.IntegerField()
    JoinCode = models.IntegerField()
    Name = models.CharField(max_length=300)
    Song = models.CharField(max_length=300)
    Type = models.CharField(max_length=30)
    Classification = models.CharField(max_length=50)
    IsUntimed = models.IntegerField()
    StartTime = models.CharField(max_length=50)

class PromoItem(models.Model):
    Name = models.TextField(max_length=200)
    Cost = models.IntegerField()
    Image = models.TextField(max_length=300)
    IsActive = models.IntegerField()
    PaidAmount = models.IntegerField()
    Sizes = models.TextField(max_length=300)

class RegPrice(models.Model):
    EventID = models.ForeignKey(Event, on_delete=models.CASCADE)
    ThruDate = models.DateField()
    IndFee = models.IntegerField()
    IndCorpFee = models.IntegerField()
    TeamFee = models.IntegerField()
    CorpFee = models.IntegerField()

class DiscountCode(models.Model):
    EventID = models.ForeignKey(Event, on_delete=models.CASCADE)
    Code = models.TextField(max_length=300)
    NumUsesAllowed = models.IntegerField()
    NumUsesCompleted = models.IntegerField()
    ValidThru = models.DateField(auto_now_add=True)
    Type = models.TextField(max_length=300, verbose_name="PercentOff,DollarsOff,TotalCost")
    Value = models.DecimalField(max_digits=6, decimal_places=2)
    AppliesTo = models.TextField(max_length=300, verbose_name="EntireCart,RegOnly")

class TeamStats(models.Model):
    EventId = models.ForeignKey(Event, on_delete=models.CASCADE)
    TeamNumber = models.ForeignKey(Team, on_delete=models.CASCADE)
    StartTime = models.DateTimeField(auto_now_add=True, blank=True)
    CurrentLeg = models.IntegerField()
    CurrentRunner  = models.TextField(max_length=300)
    LastHandoffTime = models.DateTimeField(auto_now_add=True, blank=True)
    TotalMiles = models.DecimalField(max_digits=10, decimal_places=2)
    TotalTimeSecs = models.IntegerField()
    TotalPaceSecs = models.DecimalField(max_digits=10, decimal_places=2)
    Classification = models.TextField(max_length=30)
    Type = models.TextField(max_length=30)
    

class Order(models.Model):
    IsDelivered = models.IntegerField()
    RunnerID = models.IntegerField()
    IsPaid = models.IntegerField()
    PaidAmount =models.DecimalField(max_digits=10, decimal_places=0)
    

class Runner(models.Model):
    TeamID = models.ForeignKey(Team, on_delete=models.CASCADE)
    FirstName  = models.TextField(max_length=300)
    LastName  = models.TextField(max_length=300)
    Email  = models.TextField(max_length=300)
    Phone  = models.TextField(max_length=300)
    Street  = models.TextField(max_length=300)
    City  = models.TextField(max_length=300)
    State  = models.TextField(max_length=300)
    Zip  = models.TextField(max_length=300)
    DOB = models.DateField(auto_now_add=True)
    Pace = models.IntegerField()
    Gender  = models.TextField(max_length=30)
    ShirtSize  = models.TextField(max_length=300)
    SockSize  = models.TextField(max_length=300)
    PassHash  = models.TextField(max_length=300)
    IsPaid = models.IntegerField()
    PaidAmount = models.IntegerField()
    RulesAgreedCST = models.DateTimeField(auto_now_add=True)
    IsDeleted = models.IntegerField()
    ReferredByEntity =  models.TextField(max_length=100, null=True)
    ReferredByPerson  = models.TextField(max_length=1000, null=True)
    PushToken  = models.TextField(max_length=4096, null=True)
    IsRoadie = models.IntegerField(null=True)
    DeviceToken = models.IntegerField()


class OrderDetl(models.Model):

    OrderID = models.IntegerField(null=True)
    PromoItemID = models.IntegerField(null=True)
    Num = models.IntegerField(null=True)
    Size = models.TextField(max_length=1000, null=True)

class currentevent(models.Model):
    id = models.BigIntegerField(primary_key=True)
    DateHeld = models.DateField(auto_now_add=True)
    NextStatsUpdate = models.DateTimeField(auto_now_add=True)
    class Meta:
        managed = False
        db_table = 'currentevent'

class CurrentTeams(models.Model):
    ID = models.IntegerField()
    EventID = models.IntegerField()
    Bib = models.IntegerField()
    DiscountCode =  models.TextField(max_length=1000, null=True)
    IsSplitPayment = models.IntegerField()
    IsPaid = models.IntegerField()
    PaidAmount = models.IntegerField()
    CaptainID = models.IntegerField()
    ExpectedPace = models.IntegerField()
    JoinCode = models.IntegerField()
    StartTime = models.CharField(max_length=300)
    Name = models.CharField(max_length=500)
    Song = models.CharField(max_length=1000)
    Type = models.CharField(max_length=500)
    Classification = models.CharField(max_length=500)
    IsUntimed = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'CurrentTeams'

class currentrunners(models.Model):
    ID = models.IntegerField()
    TeamID = models.IntegerField()
    FirstName = models.TextField(max_length=1000)
    LastName = models.TextField(max_length=1000)
    Email = models.TextField(max_length=1000)
    Phone = models.TextField(max_length=1000)
    Street = models.TextField(max_length=1000)
    City = models.TextField(max_length=1000)
    State = models.TextField(max_length=1000)
    Zip = models.TextField(max_length=1000)
    DOB = models.DateField()
    Pace = models.IntegerField()
    Gender = models.TextField(max_length=1000)
    ShirtSize = models.TextField(max_length=1000)
    SockSize = models.TextField(max_length=1000)
    PassHash = models.TextField(max_length=1000)
    IsPaid = models.IntegerField()
    PaidAmount = models.IntegerField()
    RulesAgreedCST = models.DateTimeField()
    IsDeleted = models.IntegerField()
    ReferredByEntity = models.TextField(max_length=1000,  null=True)
    ReferredByPerson = models.TextField(max_length=1000,  null=True)
    DeviceToken = models.IntegerField()
    IsRoadie = models.IntegerField( null=True)
    PushToken = models.TextField(max_length=1000,  null=True)
    class Meta:
        managed = False
        db_table = 'currentrunners'

class currentorders(models.Model):
    ID = models.IntegerField()
    IsDelivered = models.IntegerField()
    RunnerID = models.IntegerField()
    IsPaid = models.IntegerField()
    PaidAmount = models.DecimalField(max_digits=10, decimal_places=0)
    FirstName = models.TextField(max_length=1000)
    LastName = models.TextField(max_length=1000)
    TeamName = models.CharField(max_length=300)
    NumOrdered = models.IntegerField(null=True)
    Sizes = models.CharField(max_length=300, null=True)
    ItemName = models.CharField(max_length=300)
    ItemCost = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'currentorders'

class currentrosterinfo(models.Model):
    
    TeamNumber = models.IntegerField()
    TeamName = models.CharField(max_length=300)
    Runner = models.TextField(max_length=1000)
    Gender = models.TextField(max_length=1000)
    Email = models.TextField(max_length=1000)
    Phone = models.TextField(max_length=1000)
    Pace = models.IntegerField()
    Street = models.TextField(max_length=1000)
    City = models.TextField(max_length=1000)
    State = models.TextField(max_length=1000)
    Zip = models.TextField(max_length=1000)
    DOB = models.DateField()
    ShirtSize = models.TextField(max_length=1000)
    SockSize = models.TextField(max_length=1000)
    class Meta:
        managed = False
        db_table = 'currentrosterinfo'


class Transactions(models.Model):
    Teamid = models.IntegerField()
    Runner = models.IntegerField()
    Email = models.TextField(max_length=1000)
    Amount = models.TextField(max_length=1000)
    PaymentMethod = models.TextField(max_length=1000)
    Status = models.IntegerField()
    Description = models.TextField(max_length=1000)
    PayDate = models.DateField(auto_now_add=True)

# ################### current event
# CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `currentevent` AS (
# select  `lonestar_event`.`id` AS `id`,  `lonestar_event`.`DateHeld` AS `DateHeld`,  `lonestar_event`.`NextStatsUpdate` AS `NextStatsUpdate` from `lonestar_event` where to_days(`lonestar_event`.`DateHeld`) - to_days(current_timestamp()) > 0 order by `lonestar_event`.`DateHeld` limit 1)

############### currentteams
# CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `currentteams` AS (
# select  `t`.`id` AS `ID`,  `t`.`EventID_id` AS `EventID`,  `t`.`Bib` AS `Bib`,  `t`.`DiscountCode` AS `DiscountCode`,  `t`.`IsSplitPayment` AS `IsSplitPayment`,  `t`.`IsPaid` AS `IsPaid`,  `t`.`PaidAmount` AS `PaidAmount`,  `t`.`CaptainID` AS `CaptainID`,  `t`.`ExpectedPace` AS `ExpectedPace`,  `t`.`JoinCode` AS `JoinCode`,  `t`.`StartTime` AS `StartTime`,  `t`.`Name` AS `Name`,  `t`.`Song` AS `Song`,  `t`.`Type` AS `Type`,  `t`.`Classification` AS `Classification`,  `t`.`IsUntimed` AS `IsUntimed` from (`lonestar_team` `t`  join `currentevent` `e`  on (`t`.`EventID_id` = `e`.`id`)))


# ############### currentrunners
# CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `currentrunners` AS (
# select  `r`.`id` AS `ID`,  `r`.`TeamID_id` AS `TeamID`,  `r`.`FirstName` AS `FirstName`,  `r`.`LastName` AS `LastName`,  `r`.`Email` AS `Email`,  `r`.`Phone` AS `Phone`,  `r`.`Street` AS `Street`,  `r`.`City` AS `City`,  `r`.`State` AS `State`,  `r`.`Zip` AS `Zip`,  `r`.`DOB` AS `DOB`,  `r`.`Pace` AS `Pace`,  `r`.`Gender` AS `Gender`,  `r`.`ShirtSize` AS `ShirtSize`,  `r`.`SockSize` AS `SockSize`,  `r`.`PassHash` AS `PassHash`,  `r`.`IsPaid` AS `IsPaid`,  `r`.`PaidAmount` AS `PaidAmount`,  `r`.`RulesAgreedCST` AS `RulesAgreedCST`,  `r`.`IsDeleted` AS `IsDeleted`,  `r`.`ReferredByEntity` AS `ReferredByEntity`,  `r`.`ReferredByPerson` AS `ReferredByPerson`,  `r`.`DeviceToken` AS `DeviceToken`,  `r`.`IsRoadie` AS `IsRoadie`,  `r`.`PushToken` AS `PushToken` from (`lonestar_runner` `r`  join `currentteams` `t`  on (`r`.`TeamID_id` = `t`.`ID`)))


# ################## currentorders
# CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `currentorders` AS (
# select  `o`.`id` AS `ID`,  `o`.`IsDelivered` AS `IsDelivered`,  `o`.`RunnerID` AS `RunnerID`,  `o`.`IsPaid` AS `IsPaid`,  `o`.`PaidAmount` AS `PaidAmount`,  `r`.`FirstName` AS `FirstName`,  `r`.`LastName` AS `LastName`,  `t`.`Name` AS `TeamName`,  `d`.`Num` AS `NumOrdered`,  coalesce(`d`.`Size`,'') AS `Sizes`,  `i`.`Name` AS `ItemName`,  `i`.`Cost` AS `ItemCost` from ((((`lonestar_order` `o`  join `currentrunners` `r`  on (`r`.`ID` = `o`.`RunnerID`))  join `currentteams` `t`  on (`t`.`ID` = `r`.`TeamID`))  join `lonestar_orderdetl` `d`  on (`d`.`OrderID` = `o`.`id`))  join `lonestar_promoitem` `i`  on (`i`.`id` = `d`.`PromoItemID`)))
# ############## currentrosterinfo
# CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `currentrosterinfo` AS (
# select  `t`.`ID` AS `id`,  `t`.`Bib` AS `TeamNumber`,  `t`.`Name` AS `TeamName`,  concat(`r`.`FirstName`,' ',`r`.`LastName`) AS `Runner`,  `r`.`Gender` AS `Gender`,  `r`.`Email` AS `Email`,  `r`.`Phone` AS `Phone`,  `r`.`Pace` AS `Pace`,  `r`.`Street` AS `Street`,  `r`.`City` AS `City`,  `r`.`State` AS `State`,  `r`.`Zip` AS `Zip`,  `r`.`DOB` AS `DOB`,  `r`.`ShirtSize` AS `ShirtSize`,  `r`.`SockSize` AS `SockSize` from ((`currentrunners` `r`  join `currentteams` `t`  on (`t`.`ID` = `r`.`TeamID`))  join `currentevent` `e`  on (`e`.`id` = `t`.`EventID`)) where `r`.`IsDeleted` = 0 order by `t`.`Bib`)