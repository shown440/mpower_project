################################################################################
################################################################################
###     BRANCH MAKER
################################################################################
################################################################################

# posts/forms.py
from django import forms
from .models import HOUSEHOLDModel

class HouseHoldForm(forms.ModelForm):

    class Meta:
        model = HOUSEHOLDModel
        fields = ['hh_head']
 