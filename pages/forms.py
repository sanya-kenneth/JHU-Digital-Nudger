from pages.models import *
from django import forms
from django.core.validators import validate_email

from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from unfold.widgets import BASE_INPUT_CLASSES, INPUT_CLASSES, SELECT_CLASSES


class TrainerAdminForm(forms.ModelForm):
    """Simplified form to register a trainer"""
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    email = forms.CharField(max_length=50)
    phone_number = forms.CharField(max_length=15)

    def __init__(self, *args, **kwargs):
        super(TrainerAdminForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = False

        trainer = kwargs.get('instance')
        self.fields["first_name"].widget.attrs["class"] = " ".join(
            INPUT_CLASSES)
        self.fields["last_name"].widget.attrs["class"] = " ".join(
            INPUT_CLASSES)
        self.fields["email"].widget.attrs["class"] = " ".join(INPUT_CLASSES)
        self.fields["phone_number"].widget.attrs["class"] = " ".join(
            INPUT_CLASSES)
        if hasattr(trainer, 'user'):
            self.fields['first_name'].initial = trainer.user.first_name
            self.fields['last_name'].initial = trainer.user.last_name
            self.fields['email'].initial = trainer.user.email if trainer.user.email else ''

    class Meta:
        model = Trainer
        fields = ('first_name', 'last_name', 'phone_number', 'email')

    def clean(self):
        cleaned_data = super().clean()
        if self.instance.pk and self.cleaned_data['email'] and \
            (self.instance.user.email != self.cleaned_data['email']):
            try:
                validate_email(self.cleaned_data['email'])
            except Exception:
                self.add_error('', 'Sorry. The email is not valid')
                return

    def save(self, commit=True):
        trainer = super().save(False)
        try:
            has_user = self.instance.user
        except Exception:
            has_user = None

        # Prepare system user
        underlying_user, _ = User.objects.get_or_create(
            username=self.data['phone_number'])
        underlying_user.first_name = self.data['first_name']
        underlying_user.last_name = self.data['last_name']
        underlying_user.email = self.data['email'] if 'email' in self.data else ''
        underlying_user.save()

        # Create trainer
        trainer.user = underlying_user
        trainer.phone_number = self.data['phone_number']
        trainer.save()
        return trainer


class TraineeAdminForm(TrainerAdminForm):
    """Simplified form to register a trainee"""

    def __init__(self, *args, **kwargs):
        super(TraineeAdminForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = False
        self.fields['notes'].required = False

    class Meta:
        model = Trainee
        fields = ('first_name', 'last_name', 'phone_number', 'email', 'business_name', 'cohort', 'notes')

    def save(self, commit=True):
        trainee = super().save(False)

        # Prepare system user
        underlying_user, _ = User.objects.get_or_create(
            username=self.data['phone_number'])
        underlying_user.first_name = self.data['first_name']
        underlying_user.last_name = self.data['last_name']
        underlying_user.email = self.data['email'] if 'email' in self.data else ''
        underlying_user.save()

        # Create trainer
        trainee.user = underlying_user
        trainee.phone_number = self.data['phone_number']
        trainee.business_name = self.data['business_name']
        trainee.cohort = Cohort.objects.filter(id=self.data['cohort']).first()
        trainee.notes = self.data['notes']
        trainee.save()
        return trainee
    
class TraineeSignupForm(forms.ModelForm):
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    email = forms.CharField(max_length=50)
    phone_number = forms.CharField(max_length=15)
    
    def __init__(self, *args, **kwargs):
        super(TraineeSignupForm, self).__init__(*args, **kwargs)
        self.fields['notes'].required = False
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    
    class Meta:
        model = Trainee
        fields = ('first_name', 'last_name', 'phone_number', 
                  'email', 'business_name', 'cohort', 'notes')
        
    def save(self, commit=True):
        trainee = super().save(False)

        # Prepare system user
        underlying_user, _ = User.objects.get_or_create(
            username=self.data['phone_number'])
        underlying_user.first_name = self.data['first_name']
        underlying_user.last_name = self.data['last_name']
        underlying_user.email = self.data['email'] if 'email' in self.data else ''
        underlying_user.save()

        # Create trainer
        trainee.user = underlying_user
        trainee.phone_number = self.data['phone_number']
        trainee.business_name = self.data['business_name']
        trainee.cohort = Cohort.objects.filter(id=self.data['cohort']).first()
        trainee.notes = self.data['notes']
        trainee.save()
        return trainee


class BotAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BotAdminForm, self).__init__(*args, **kwargs)
    class Meta:
        model = Bot
        fields = ('bot_code', 'name', 'description', 
                  'status', 'cohort')