from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import User, Team,  PromoItem, RegPrice, DiscountCode, TeamStats, Order, Runner, OrderDetl, Transactions


class LoneStarUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
class LoneStarUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

class LoneStarUserAdmin(UserAdmin):
    form = LoneStarUserChangeForm
    add_form = LoneStarUserCreationForm
    fieldsets = ((None, {'fields': ('username', 'password')}), 
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'runnerid')}), 
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}), 
        ('Important dates', {'fields': ('last_login', 'date_joined')}),)

admin.site.unregister(Group)
admin.site.register(User, LoneStarUserAdmin)
admin.site.register(Team)
admin.site.register(PromoItem)
admin.site.register(RegPrice)
admin.site.register(DiscountCode)
admin.site.register(TeamStats)
admin.site.register(Order)
admin.site.register(Runner)
admin.site.register(OrderDetl)
admin.site.register(Transactions)