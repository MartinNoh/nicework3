from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from common.models import MyUser


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('email', 'realname', 'phonenum', 'rank', 'department', 'effcdate', 'openingtime', 'closingtime')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("비밀번호가 일치하지 않습니다.")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    RANK_CHOICES = (('AS', '주임'), ('SN', '대리'), ('PC', '책임'), ('CF', '수석'))
    rank = forms.ChoiceField(choices=RANK_CHOICES)
    DEPARTMENT_CHOICES = (('DEV', '개발팀'), ('KNG', '지식큐레이션팀'))
    department = forms.ChoiceField(choices=DEPARTMENT_CHOICES)
    effcdate = forms.DateField(widget=forms.widgets.DateInput(format="%Y-%m-%d"))
    openingtime = forms.TimeField(widget=forms.widgets.TimeInput(format="%H:%M:%S"))
    closingtime = forms.TimeField(widget=forms.widgets.TimeInput(format="%H:%M:%S"))

    class Meta:
        model = MyUser
        fields = ('realname', 'phonenum', 'rank', 'department', 'effcdate', 'openingtime', 'closingtime', 'adminmemo')


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'realname', 'effcdate', 'openingtime', 'closingtime', 'is_active', 'is_manager', 'is_admin', 'is_sbstt', 'is_over80p')
    list_filter = ('is_active', 'is_manager', 'is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('realname', 'phonenum', 'department', 'rank', 'effcdate', 'openingtime', 'closingtime')}),
        ('Permissions', {'fields': ('is_active', 'is_manager', 'is_admin',)}),
        ('Memo', {'fields': ('is_sbstt', 'is_over80p', 'adminmemo',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'realname', 'phonenum', 'department', 'rank', 'effcdate', 'openingtime', 'closingtime', 'password1', 'password2'),
        }),
    )
    search_fields = ('realname',)
    ordering = ('openingtime', 'realname')
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(MyUser, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)