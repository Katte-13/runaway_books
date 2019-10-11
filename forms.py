import datetime

from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from books.models import Status, Book, Author, Genre


class RenewBookModelForm(ModelForm):
     
    def clean_due_back(self):
         data = self.cleaned_data['due_back'] 
         
         if data < datetime.date.today():
             raise ValidationError(_('Data invalidă - dată aflată în trecut.'), code='invalid')
    
         if data > datetime.date.today() + datetime.timedelta(days=10):
             raise ValidationError(_('Dată invalidă - mai mult de 10 zile.'), code='invalid')
        
         return data

    class Meta:
        model = Status
        fields = ['due_back']
        labels = {'due_back': _('Dată prelungire')}
        help_texts = {'due_back': _('Introdu o dată de azi până în 10 zile.')}

          
class WishBookModelForm(ModelForm):
    status = forms.ChoiceField(choices=Status.GIVEAWAY_STATUS[:2], initial='Cu chef de ducă')
    
    class Meta:
        model = Status
        fields = ['status']

    

    
    
   

    