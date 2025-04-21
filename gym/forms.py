from django import forms
from .models import ApplicantDetail ,QueryDoubt ,Trainer ,Gym

class ApplicantDetailForm(forms.ModelForm):
    class Meta:
        model = ApplicantDetail  # Specify the model
        fields = ['gym_id','name', 'phone', 'email', 'about_user', 'user_cv']
        # or if you want to include all except 'date', you can leave this out
        # exclude = ['date']

          # Create a ChoiceField for gym selection
    gym_id = forms.ChoiceField(
        choices=[(gym.gym_id, gym.gym_name) for gym in Gym.objects.all()],
        widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select Gym'}),
        required=True,
        label="Select Gym",
    )

    # Define other widgets as before with added improvements
    widgets = {
        'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name', 'required': True}),
        'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number', 'required': True}),
        'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address', 'required': True}),
        'about_user': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Tell us about yourself', 'rows': 2, 'required': True}),
        'user_cv': forms.FileInput(attrs={'class': 'form-control', 'required': True}),
    }

class  UserQuery(forms.ModelForm):
    class Meta:
        model = QueryDoubt #define the model name
        fields = '__all__'
        exclude =["member","question_date","answer","answer_date"]

        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control' , 'placeholder':'Enter YOur Name'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Subject'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}),
            'question': forms.Textarea(attrs={'class': 'form-control','placeholder':'Ask your Questions','rows':3}),
        } 

class TrainerForm(forms.ModelForm):
    class Meta:
        model = Trainer
        fields = ['name', 'email', 'gender', 'city', 'specialization', 'experience', 'about_trainer', 'trainer_pic']
        widgets = {
             'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Name'}),        
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}),
            'gender': forms.Select(attrs={'class': 'form-control'}, choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")]),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter City'}),
            'specialization': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Specialization'}),
            'experience': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Experience', 'rows': 3}),
            'about_trainer': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter About Trainer', 'rows': 3}),
            'trainer_pic': forms.FileInput(attrs={'class': 'form-control', 'required': True}),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Trainer.objects.filter(email=email).exists():
            raise forms.ValidationError("A trainer with this email already exists.")
        return email


