# django imports
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

# app level imports
from .models import User


class UserCreationForm(forms.ModelForm):
    """
    Form for creating new users.
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = '__all__'

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Password Do Not Match')

        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = '__all__'

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]





# class SetPasswordForm(forms.ModelForm):
#     """
#     A form that lets a user change set their password without entering the old
#     password
#     """
#     error_messages = {
#         'password_mismatch': _("The two password fields didn't match."),
#     }
#     new_password1 = forms.CharField(label=_("New password"),
#                                     widget=forms.PasswordInput)
#     new_password2 = forms.CharField(label=_("New password confirmation"),
#                                     widget=forms.PasswordInput)

#     def __init__(self, user, *args, **kwargs):
#         self.user = user
#         super(SetPasswordForm, self).__init__(*args, **kwargs)

#     def clean_new_password2(self):
#         password1 = self.cleaned_data.get('new_password1')
#         password2 = self.cleaned_data.get('new_password2')
#         if password1 and password2:
#             if password1 != password2:
#                 raise forms.ValidationError(
#                     self.error_messages['password_mismatch'],
#                     code='password_mismatch',
#                 )
#         return password2


# class PasswordChangeForm(SetPasswordForm):
#     """
    
#     """
#     error_messages = dict(SetPasswordForm.error_messages, **{
#         'password_incorrect': _("Your old password was entered incorrectly. "
#                                 "Please enter it again."),
#     })
#     old_password = forms.CharField(label=_("Old password"),
#                                    widget=forms.PasswordInput)

#     def clean_old_password(self):
#         """
#         Validates that the old_password field is correct.
#         """
#         old_password = self.cleaned_data["old_password"]
#         if not self.user.check_password(old_password):
#             raise forms.ValidationError(
#                 self.error_messages['password_incorrect'],
#                 code='password_incorrect',
#             )
#         return old_password


# PasswordChangeForm.base_fields = OrderedDict(
#     (k, PasswordChangeForm.base_fields[k])
#     for k in ['old_password', 'new_password1', 'new_password2']
# )






















# class changePassForm(forms.ModelForm):
#     old_password_flag = True #Used to raise the validation error when it is set to False
#     old_password = forms.CharField(label="Old Password", min_length=6, widget=forms.PasswordInput)
#     new_password = forms.CharField(label="New Password", min_length=6, widget=forms.PasswordInput)
#     re_new_password = forms.CharField(label="Re-type New Password", min_length=6, widget=forms.PasswordInput)

# def set_old_password_flag(self): 

# #This method is called if the old password entered by user does not match the password in the database, which sets the flag to False

#     self.old_password_flag = False

#     return 0

# def clean_old_password(self, *args, **kwargs):
#     old_password = self.cleaned_data.get('old_password')

#     if not old_password:
#         raise forms.ValidationError("enter your old password.")

#     if self.old_password_flag == False:
#     #It raise the validation error that password entered by user does not match the actucal old password.

#         raise forms.ValidationError("The old password that you have entered is wrong.")

#     return old_password
