from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
import datetime
from .models import add_course, Content

class RegForm(forms.ModelForm):
	class Meta:
		#model = Reg
		fields = ['username', 'email_address', 'password']
		widgets = {
		'password': forms.PasswordInput()
		}


class UserRegisterForm(UserCreationForm):
	ch = [
	('ST', 'Learner'),
	('TU', 'Instructor'),
	]
	email = forms.EmailField()
	first_name = forms.CharField(max_length=100)
	last_name = forms.CharField(max_length=100)
	contact_number = forms.IntegerField()


	class Meta:
		model = User
		fields = ['username','first_name','last_name', 'email','contact_number', 'password1', 'password2']

	
	def __init__(self, *args, **kwargs):
		super(UserRegisterForm, self).__init__(*args, **kwargs)

		for fieldname in ['username', 'password1', 'password2']:
			self.fields[fieldname].help_text = None

class add_course_form(forms.ModelForm):
	class Meta:
		model = add_course

		fields = ["course_name","course_section","course_price","sale_price","course_image","details"]

class add_content_form(forms.ModelForm):
	class Meta:
		model = Content

		fields = ["module_no","chapter_no","chapter","doc","img","file","resource"]
		labels = {"chapter": "Chapter Name","doc": "Video","img": "Image", "file": "Document", "resource": "Resource to download"}
		help_texts = {"chapter": "Choose one course content type (video,img,doc or resource) at a time for better arrangement"}