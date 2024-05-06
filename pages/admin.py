import datetime
from typing import Any
from django.contrib import admin
from django.http import HttpRequest
import requests
from unfold.admin import ModelAdmin

from django.contrib.auth import get_user_model

from import_export import resources
from import_export.admin import ExportActionModelAdmin
from import_export.fields import Field

from pages.forms import BotAdminForm, TraineeAdminForm, TrainerAdminForm
from .models import Bot, Content, Messages, Cohort, Topic, Trainee, Trainer, UserNote
from django.contrib.auth.models import User

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from dadfes.admin import DfesAdminModelMixin

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
        
        
class userNoteResource(resources.ModelResource):
    
    first_name = Field(
        attribute='first_name',
        column_name='First Name'
    )
    last_name = Field(
        attribute='last_name',
        column_name='Last Name'
    )
   
    phone_number = Field(
        attribute='phone',
        column_name='Phone Number'
    )
    
    notes = Field(
        attribute='notes',
        column_name='Notes'
    )
    
    notes_type = Field(
        attribute='notes_type',
        column_name='Notes Type'
    )
    
    time_created = Field(
        attribute='time_created',
        column_name='Time Created'
    )
    
    cohort = Field(
        attribute='cohort',
        column_name='Cohort'
    )
    
    def dehydrate_notes_type(self, obj):
        try:
            return obj.notes_type
        except:
            return None
    
    def dehydrate_time_created(self, obj):
        try:
            return obj.time_created
        except:
            return None
    
    
    def dehydrate_notes(self, obj):
        try:
            return obj.notes
        except:
            return None
    
    
    def dehydrate_first_name(self, obj):
        try:
            trainee = Trainee.objects.filter(phone_number=f"+{obj.phone}").first()
            return trainee.user.first_name if trainee else ''
        except:
            return None

    def dehydrate_last_name(self, obj):
        try:
            trainee = Trainee.objects.filter(phone_number=f"+{obj.phone}").first()
            return trainee.user.last_name if trainee else '' 
        except:
            return None

    def dehydrate_phone_number(self, obj):
        try:
            phone_number = trainee.phone_number.as_e164
            trainee = Trainee.objects.filter(phone_number=f"+{obj.phone}").first()
            return trainee.phone_number.as_e164 if trainee else obj.phone
        except:
            return None
        
    def dehydrate_cohort(self, obj):
        try:
            trainee = Trainee.objects.filter(phone_number=f"+{obj.phone}").first()
            return trainee.cohort.title if trainee else '' 
        except:
            return None
        
    
    class Meta:
        model = UserNote
        fields = ("first_name", "last_name", "phone", 
                  "notes", "notes_type", "time_created", "cohort")
        

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
    
class NotesTypeFilter(admin.SimpleListFilter):

    title = 'Notes Type'
    parameter_name = 'notes_type'
    
    def lookups(self, request, model_admin):
        result = [(i.notes_type, i.notes_type) for i in model_admin.get_list(request)['items']]
        result = list(dict.fromkeys(result))
        return result
    
class TimeCreatedFilter(admin.SimpleListFilter):

    title = 'Time Created'
    parameter_name = 'time_created'
    
    def lookups(self, request, model_admin):
        return [
            ("this month", "this month"),
            ("last month", "last month"),
            ("this year", "this year"),
        ]
 

@admin.register(UserNote)
class UserNotesAdminClass(DfesAdminModelMixin, ModelAdmin, ExportActionModelAdmin):
    resource_class = userNoteResource
    list_display = ("first_name", "last_name", "phone", "notes", 
                    "notes_type", "time_created", "cohort")
    
    list_filter = (NotesTypeFilter, TimeCreatedFilter)
    
    search_fields = ("phone",)
    
    class ListAsQuerySet(list):

        def __init__(self, *args, model, **kwargs):
            self.model = model
            super().__init__(*args, **kwargs)

        def filter(self, *args, **kwargs):
            return self  # filter ignoring, but you can impl custom filter

        def order_by(self, *args, **kwargs):
            return self
        
        def distinct(self, *args, **kwargs):
            return self
        
        def values_list(self, *args, **kwargs):
            return self
    
    def get_queryset(self, request: HttpRequest) -> resources.QuerySet[Any]:
        return self.ListAsQuerySet(self.get_list(request)["items"], model=UserNote) 
    
    def has_delete_permission(self, request: HttpRequest, obj: Any | None = ...) -> bool:
        return False
    
    def get_list(self, request, page_num=0, list_per_page=0):

        search = request.GET.get('q')
        #   order_by = request.GET.get('o')
        notes_type_filter = request.GET.get('notes_type')
        time_created_filter = request.GET.get('time_created')
        url = "https://kasukuappstore.com/apptest/get_user_saved_notes.php"
        data = requests.get(url=url)
        data = {"data": data.json()}

        items = [UserNote(**i) for i in data.get("data") or []]
        
        if search:
            items = [item for item in items if item.phone.strip() == search.strip()]
            
        if  notes_type_filter:
            items = [item for item in items if 
                     item.notes_type.strip() == notes_type_filter.strip()]
            
        if time_created_filter:
            if time_created_filter == "this month":
                items = [item for item in items if 
                     datetime.datetime.strptime(item.time_created.strip().split()[0],
                                                "%Y-%m-%d").month == datetime.datetime.today().month]
                
            if time_created_filter == "last month":
                last_month = datetime.datetime.today()-datetime.timedelta(days=30)
                items = [item for item in items if 
                     datetime.datetime.strptime(item.time_created.strip().split()[0],
                                                "%Y-%m-%d").month == last_month.month]
                
            if time_created_filter == "this year":
                items = [item for item in items if 
                     datetime.datetime.strptime(item.time_created.strip().split()[0],
                                                "%Y-%m-%d").year == datetime.datetime.today().year]

        self.user_notes = items
        return {
            "total": len(items) if len(items) > 0 else 0,
            "items": items
        }
        
    def cohort(self, obj):
        trainee = Trainee.objects.filter(phone_number=f"+{obj.phone}").first()
        return trainee.cohort.title if trainee else '' 
    
    def first_name(self, obj):
        trainee = Trainee.objects.filter(phone_number=f"+{obj.phone}").first()
        return trainee.user.first_name if trainee else '' 
    
    def last_name(self, obj):
        trainee = Trainee.objects.filter(phone_number=f"+{obj.phone}").first()
        return trainee.user.last_name if trainee else '' 

    # 3. other standart django admin customization
    def get_object(self, request, object_id, *args, **kwargs):
        try:
            result = [item for i, item in enumerate(self.get_list(request)["items"]) if i+1 == int(object_id)]
            return result[0]
        except:
            return None

