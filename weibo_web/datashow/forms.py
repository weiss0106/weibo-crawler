from django import forms
# from polls import models
from django.core.exceptions import ValidationError


class UserConfigForm(forms.Form):  # 定义表单
    ch_list = (
        '原创微博','全部微博'
    )
    Form_uid = forms.CharField(max_length=200)
    Form_since_date = forms.DateField(widget=forms.Select())
    Form_filter=forms.Select(choices=ch_list)
    Form_o_p_download = forms.IntegerField(widget=forms.Select(choices=(0,1)))
    Form_r_p_download = forms.IntegerField(widget=forms.Select(choices=(0, 1)))
    Form_o_v_download=forms.IntegerField(widget=forms.Select(choices=(0, 1)))
    Form_r_v_download=forms.IntegerField(widget=forms.Select(choices=(0,1)))