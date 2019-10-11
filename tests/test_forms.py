import datetime

from django.test import TestCase
from django.utils import timezone

from books.forms import RenewBookModelForm

class RenewBookFormTest(TestCase):
    
    def test_renew_form_date_in_past(self):
        date = datetime.date.today() - datetime.timedelta(days=1)
        form = RenewBookModelForm(data={'due_back': date})
        self.assertFalse(form.is_valid())
    
    def test_renew_form_date_too_far_in_future(self):
        date = datetime.date.today() + datetime.timedelta(days=11)
        form = RenewBookModelForm(data={'due_back': date})
        self.assertFalse(form.is_valid())
        
    def test_renew_form_day_today(self):
        date = datetime.date.today()
        form = RenewBookModelForm(data={'due_back': date})
        self.assertTrue(form.is_valid())
        
    def test_renew_form_day_max(self):
        date = timezone.now() + datetime.timedelta(days=10)
        form = RenewBookModelForm(data={'due_back': date})
        self.assertTrue(form.is_valid())
        