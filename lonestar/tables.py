from django.utils.safestring import mark_safe
from django_tables2.utils import Accessor, AttributeDict
import django_tables2 as tables
from .models import currentrosterinfo
import itertools
from django.conf import settings
from .utils import tir



class MaterializeCheckColumn(tables.CheckBoxColumn):
    def render(self, value, bound_column, record):
        default = {"type": "checkbox", "name": bound_column.name, "value": value}
        if self.is_checked(value, record):
            default.update({"checked": "checked"})
        general = self.attrs.get("input")
        specific = self.attrs.get("td__input")
        attrs = tables.utils.AttributeDict(default, **(specific or general or {}))
        return mark_safe("<input %s/>" % attrs.as_html())

class CurrentTeamsInfoTable(tables.Table):
    
    TeamNumber = tables.Column(verbose_name='Number')
    Name = tables.Column(verbose_name='Team Name')
    JoinCode = tables.Column(verbose_name='JoinCode', orderable=False)
    Captain = tables.Column(verbose_name='Captain', orderable=False)
    Email = tables.Column(verbose_name='Email', orderable=False)
    Phone = tables.Column(verbose_name='Phone', orderable=False, visible=False)
    Type = tables.Column(verbose_name='Type')
    Classification = tables.Column(verbose_name='Class')
    Song = tables.Column(verbose_name='Song', orderable=False)
    IsUntimed = tables.Column(verbose_name='IsUntimed', orderable=False)
    AvgPace = tables.Column(verbose_name='AvgPace', orderable=False)
    NumRunners = tables.Column(verbose_name='# Runners')
    MS = tables.Column(verbose_name='MS', orderable=False)
    MM = tables.Column(verbose_name='MM', orderable=False)
    ML = tables.Column(verbose_name='ML', orderable=False)
    MXL = tables.Column(verbose_name='MXL', orderable=False)
    MXXL = tables.Column(verbose_name='MXXL', orderable=False)
    WS = tables.Column(verbose_name='WS', orderable=False)
    WM = tables.Column(verbose_name='WM', orderable=False)
    WL = tables.Column(verbose_name='WL', orderable=False)
    WXL = tables.Column(verbose_name='WXL', orderable=False)
    S_M = tables.Column(verbose_name='S-M', orderable=False)
    XL_L = tables.Column(verbose_name='XL-L', orderable=False)
    class Meta:
        template_name = "django_tables2/bootstrap-responsive.html"
        fields = ('TeamNumber', 'Name', 'JoinCode', 'Captain', 'Type', 'Classification', 'Song', 'IsUntimed', 'AvgPace', 'NumRunners', 'MS', 'MM', 'ML', 'MXL', 'MXXL', 'WS', 'WM', 'WL','WXL','S_M','XL_L')
        attrs = {"class": "table table-hover paleblue"}
  
    def render_Name(self, value, record):
        return mark_safe('''<a href="/team?teambib=%s">%s</a>''' % (record.TeamNumber, value.upper()))
    def render_Captain(self, value, record):
        return mark_safe('''%s<br/><a href="mailto:%s">%s</a><br/>%s''' % (value, record.Email, record.Email, record.Phone))
    def render_AvgPace(self, value, record):
        dis_time = tir.displayTime(value)
        return mark_safe('''%s''' % (dis_time))


class currentrosterinfotable(tables.Table):
   
    TeamNumber = tables.Column(verbose_name='Team #')
    TeamName = tables.Column(verbose_name='Team Name')
    Email = tables.Column(verbose_name='Email', orderable=False)
    Phone = tables.Column(verbose_name='Phone', orderable=False)
    Runner = tables.Column(verbose_name='Runner')
    Gender = tables.Column(verbose_name='Gender')
    Pace = tables.Column(verbose_name='10KPace', orderable=False)
    Street = tables.Column(verbose_name='Street')
    City = tables.Column(verbose_name='City')
    State = tables.Column(verbose_name='State')
    Zip = tables.Column(verbose_name='Zip', orderable=False)
    DOB = tables.Column(verbose_name='DOB', orderable=False)
    ShirtSize = tables.Column(verbose_name='Shirt', orderable=False)
    SockSize = tables.Column(verbose_name='Sock', orderable=False)
    
    class Meta:
        model = currentrosterinfo
        template_name = "django_tables2/bootstrap-responsive.html"
        fields = ('TeamNumber', 'TeamName', 'Runner', 'Gender', 'Email', 'Phone', 'Pace', 'Street', 'City', 'State', 'Zip', 'DOB', 'ShirtSize', 'SockSize' )
        attrs = {"class": "table table-hover paleblue"}
    def render_counter(self):
        self.row_counter = getattr(self, 'row_counter', itertools.count(1))
        return next(self.row_counter)
    def render_TeamName(self, value, record):
        return mark_safe('''<a href="/team?teambib=%s">%s</a>''' % (record.TeamNumber, value.upper()))
    def render_Email(self, value, record):
        return mark_safe('''<a href="mailto:%s">%s</a>''' % (record.Email, record.Email))
  
class currenttirgearinfotable(tables.Table):
   
    TeamNumber = tables.Column(verbose_name='Team #')
    TeamName = tables.Column(verbose_name='Team Name')
    Gear = tables.Column(verbose_name='Gear', orderable=False)
    Runner = tables.Column(verbose_name='Runner')
    Paid = tables.Column(verbose_name='Paid', orderable=False)
    Sizes = tables.Column(verbose_name='Sizes', orderable=False)
    ShirtSize = tables.Column(verbose_name='Shirt', orderable=False)
    SockSize = tables.Column(verbose_name='Sock', orderable=False)
    Phone = tables.Column(verbose_name='Phone', orderable=False)
    Email = tables.Column(verbose_name='Email', orderable=False)
    
    Street = tables.Column(verbose_name='Street')
    City = tables.Column(verbose_name='City')
    State = tables.Column(verbose_name='State')
    Zip = tables.Column(verbose_name='Zip')
    
    class Meta:
        template_name = "django_tables2/bootstrap-responsive.html"
        fields = ('TeamNumber', 'TeamName', 'Runner', 'Gear', 'Sizes','Paid', 'ShirtSize', 'SockSize', 'Phone', 'Email', 'City','Street', 'State', 'Zip')
        attrs = {"class": "table table-hover paleblue"}
  
    def render_TeamName(self, value, record):
        return mark_safe('''<a href="/team?teambib=%s">%s</a>''' % (record.TeamNumber, value.upper()))
    def render_Email(self, value, record):
        return mark_safe('''<a href="mailto:%s">%s</a>''' % (record.Email, record.Email))
