from django import forms
from .models import ProblemReport
from .models import Worker
from django.core.exceptions import ValidationError
from .models import Employer
from .models import JobPost
from .models import Application
from .models import SupportMessage

class ProblemReportForm(forms.ModelForm):
    class Meta:
        model = SupportMessage
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-3 py-2 border rounded'}),
            'message': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border rounded h-32'}),
        }
class WorkerRegistrationForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ['name', 'id_card_number', 'phone', 'location', 'profile_picture', 'skill', 'experience', 'is_available']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input-field'}),
            'id_card_number': forms.TextInput(attrs={'class': 'input-field'}),
            'phone': forms.TextInput(attrs={'class': 'input-field'}),
            'location': forms.TextInput(attrs={'class': 'input-field'}),
            'skill': forms.TextInput(attrs={'class': 'input-field'}),
            'experience': forms.Textarea(attrs={'class': 'input-field', 'rows': 3}),
            'is_available': forms.CheckboxInput(attrs={'class': 'checkbox-field'}),
        }
    def clean_id_card_number(self):
        id_card = self.cleaned_data.get('id_card_number')
        if Worker.objects.filter(id_card_number=id_card).exists():
            raise ValidationError("This ID card number is already registered.")
        return id_card
    
    from django import forms
from .models import Employer  # Make sure you have this import too

class EmployerSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-field'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-field'}))

    class Meta:
        model = Employer
        fields = ['name', 'id_card_number', 'email', 'password']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input-field'}),
            'id_card_number': forms.TextInput(attrs={'class': 'input-field'}),
            'email': forms.EmailInput(attrs={'class': 'input-field'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")

        return cleaned_data
    
class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = ['title', 'description', 'location', 'skill_required']

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Optional message to employer...'})
        }
class JobApplicationForm(forms.Form):
    
    message = forms.CharField(widget=forms.Textarea, required=False, label='Message (optional)')
    
class WorkerForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ['name', 'phone', 'skill', 'location']  