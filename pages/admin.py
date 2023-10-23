from django.contrib import admin
from unfold.admin import ModelAdmin

from django.contrib.auth import get_user_model

from import_export import resources
from import_export.admin import ExportActionModelAdmin
from import_export.fields import Field

from pages.forms import BotAdminForm, TraineeAdminForm, TrainerAdminForm
from .models import Bot, Content, Messages, Cohort, Topic, Trainee, Trainer
from django.contrib.auth.models import User

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

User = get_user_model()

class TrainerResource(resources.ModelResource):
    
    first_name = Field(
        attribute='first_name',
        column_name='First Name'
    )
    last_name = Field(
        attribute='last_name',
        column_name='Last Name'
    )
   
    phone_number = Field(
        attribute='phone_number',
        column_name='Phone Number'
    )
    
    email = Field(
        attribute='email',
        column_name='Email'
    )
    
    def dehydrate_first_name(self, trainer):
        try:
            return trainer.user.first_name
        except:
            return None

    def dehydrate_last_name(self, trainer):
        try:
            return trainer.user.last_name
        except:
            return None
        
    def dehydrate_email(self, trainer):
        try:
            return trainer.user.email
        except:
            return None

    def dehydrate_phone_number(self, trainer):
        try:
            phone_number = trainer.phone_number.as_e164
        except:
            return None

        return phone_number
        
    class Meta:
        model = Trainer
        fields = ('first_name', 'last_name',  'phone_number', 'email')
        
class TraineeResource(resources.ModelResource):
    
    first_name = Field(
        attribute='first_name',
        column_name='First Name'
    )
    last_name = Field(
        attribute='last_name',
        column_name='Last Name'
    )
   
    phone_number = Field(
        attribute='phone_number',
        column_name='Phone Number'
    )
    
    email = Field(
        attribute='email',
        column_name='Email'
    )
    
    business_name = Field(
        attribute='business_name',
        column_name='Business Name'
    )
    
    def dehydrate_first_name(self, trainee):
        try:
            return trainee.user.first_name
        except:
            return None

    def dehydrate_last_name(self, trainee):
        try:
            return trainee.user.last_name
        except:
            return None
        
    def dehydrate_email(self, trainee):
        try:
            return trainee.user.email
        except:
            return None

    def dehydrate_phone_number(self, trainee):
        try:
            phone_number = trainee.phone_number.as_e164
        except:
            return None

        return phone_number
    
    def dehydrate_business_name(self, trainee):
        try:
            return trainee.business_name
        except:
            return None
        
    def dehydrate_cohort(self, trainee):
        try:
            return trainee.cohort.title
        except:
            return None
    
    class Meta:
        model = Trainee
        fields = ('first_name', 'last_name',  'phone_number',
                  'email', 'business_name', 'cohort')
        

@admin.register(Trainer)
class TrainerAdminClass(ModelAdmin, ExportActionModelAdmin):
    form = TrainerAdminForm
    resource_class = TrainerResource
    list_display = (
        "first_name", "last_name", "phone_number", "email")
    search_fields = ('phone_number', 'user__first_name', 'user__last_name',)
    
    def first_name(self, obj):
        return obj.user.first_name

    def last_name(self, obj):
        return obj.user.last_name
    
    def email(self, obj):
        return obj.user.email

@admin.register(Trainee)
class TraineeAdminClass(TrainerAdminClass):
    form = TraineeAdminForm
    resource_class = TraineeResource
    list_display = (
        "first_name", "last_name", "phone_number", "email", "business_name", "cohort")
    search_fields = ('phone_number', 'user__first_name', 'user__last_name', 'cohort__title')
    

@admin.register(Cohort)
class CohortAdminClass(ModelAdmin):
    list_display = (
        "title", "description", "country", "code",  "start_date", "end_date", "_trainers", "_trainees")
    search_fields = ('title', 'country')
    readonly_fields = ('code',)
   
    def _trainers(self, obj):
        return obj.trainers.count()
    
    def _trainees(self, obj):
        return Trainee.objects.filter(cohort=obj).count()
    
@admin.register(Topic)
class TopicAdminClass(ModelAdmin):
    pass

@admin.register(Messages)
class MessagingAdminClass(ModelAdmin):
    pass

@admin.register(Bot)
class BotAdminClass(ModelAdmin):
    form = BotAdminForm
    list_display = (
        "bot_code", "name", "status", "description", "cohort")

@admin.register(Content)
class ContentAdminClass(ModelAdmin):
    list_display = (
        "title", "bot", "content_order", "cohort")
    
    search_fields = ('title', 'bot', 'cohort')
    
    list_filter = ('bot',)
    
    def cohort(self, obj):
        return obj.bot.cohort
