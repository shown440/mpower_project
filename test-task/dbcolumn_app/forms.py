################################################################################
################################################################################
###     BRANCH MAKER
################################################################################
################################################################################

# posts/forms.py
from django import forms
from .models import HouseHoldModel

class HouseHoldForm(forms.ModelForm):

    class Meta:
        model = HouseHoldModel
        fields = ['hh_head']
 