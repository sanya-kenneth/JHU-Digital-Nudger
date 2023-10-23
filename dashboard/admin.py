from datetime import datetime
from django.contrib import admin
from django.http import HttpRequest
from unfold.admin import ModelAdmin
from django.db.models.functions import TruncDay
from django.db.models import Count
from django.core.serializers.json import DjangoJSONEncoder

import json
import requests

from dashboard.models import Dashboard
from pages.models import Cohort, Trainee, Trainer

current_year = datetime.today().year


@admin.register(Dashboard)
class DashboardAdminClass(ModelAdmin):
    list_display = ("name",)
    
    def has_add_permission(self, request: HttpRequest) -> bool:
        return False
    
    def has_change_permission(self, request: HttpRequest) -> bool:
        return False
    
    def retrieve_goal_analytics(self):
        try:
            url = "https://kasukuappstore.com/apptest/analytics.php"
            
            response = requests.get(url=url)
            return json.loads(response._content)
        except Exception as e:
            ...
            
    def goal_details(self):
        try:
            url = "https://kasukuappstore.com/apptest/get_user_events.php"
            
            response = requests.get(url=url)
            return json.loads(response._content)
        except Exception as e:
            ...
    
    def changelist_view(self, request, extra_context=None):
        # Aggregate new trainers per day
        trainer_data = (
            Trainer.objects.annotate(date=TruncDay("user__date_joined"))
            .values("date")
            .annotate(y=Count("id"))
            .order_by("-date")
        )
        
        trainee_data = (
            Trainee.objects.annotate(date=TruncDay("user__date_joined"))
            .values("date")
            .annotate(y=Count("id"))
            .order_by("-date")
        )
        
        cohort_data = (
            Cohort.objects.annotate(date=TruncDay("created_on"))
            .values("date")
            .annotate(y=Count("id"))
            .order_by("-date")
        )
        
        month_data = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, 
                      '6': 0, '7': 0, '8': 0, '9': 0, '10': 0, 
                      '11': 0, '12': 0}
        
        trainer_months = month_data.copy()
        for data in trainer_data:
            for key, _month_data in trainer_months.items():
                if data['date'].month == int(key):
                    trainer_months[key] = trainer_months[key]+data['y']
        trainer_data = [trainer_months[f'{x}'] for x in range(1, 12)]
        
        trainee_months = month_data.copy()
        for data in trainee_data:
            for key, _month_data in trainee_months.items():
                if data['date'].month == int(key):
                    trainee_months[key] = trainee_months[key]+data['y']
        trainee_data = [trainee_months[f'{x}'] for x in range(1, 12)]
        
        cohort_months = month_data.copy()
        for data in cohort_data:
            for key, _month_data in cohort_months.items():
                if data['date'].month == int(key):
                    cohort_months[key] = cohort_months[key]+data['y']
        cohort_data = [cohort_months[f'{x}'] for x in range(1, 12)]
        
        goal_dt = self.goal_details()
        
        sense_list = []
        act_list = []
        shift_list = []
        
        for goal in goal_dt:
            if goal['goal_type'].lower() == 'sense':
                sense_list.append(goal)
            if goal['goal_type'].lower() == 'act':
                act_list.append(goal)
            if goal['goal_type'].lower() == 'shift':
                shift_list.append(goal)
                
        sense_months = month_data.copy()
        for data in sense_list:
            _date = datetime.strptime(data['date'], '%Y-%m-%d')
            for key, _month_data in sense_months.items():
                if _date.month == int(key):
                   
                    sense_months[key] = sense_months[key] + 1
        sense_data = [sense_months[f'{x}'] for x in range(1, 12)]
        
        act_months = month_data.copy()
        for data in act_list:
            _date = datetime.strptime(data['date'], '%Y-%m-%d')
            for key, _month_data in act_months.items():
                if _date.month == int(key):
                   
                    act_months[key] = act_months[key] + 1
        act_data = [act_months[f'{x}'] for x in range(1, 12)]
        
        shift_months = month_data.copy()
        for data in shift_list:
            _date = datetime.strptime(data['date'], '%Y-%m-%d')
            for key, _month_data in shift_months.items():
                if _date.month == int(key):
                   
                    shift_months[key] = shift_months[key] + 1
        shift_data = [shift_months[f'{x}'] for x in range(1, 12)]
      
        trainers = Trainer.objects.count()
        trainees = Trainee.objects.count()
        cohort = Cohort.objects.count()
        
        model_analytics  = {"trainers": trainers,
                            "trainees": trainees,
                            "cohorts": cohort}
        
        # Serialize and attach the chart data to the template context
        trainer_as_json = json.dumps(list(trainer_data), cls=DjangoJSONEncoder)
        trainee_as_json = json.dumps(list(trainee_data), cls=DjangoJSONEncoder)
        cohort_as_json = json.dumps(list(cohort_data), cls=DjangoJSONEncoder)
    
        extra_context = extra_context or {"trainer_data": trainer_as_json,
                                          "trainee_data": trainee_as_json,
                                          "cohort_data": cohort_as_json,
                                          "dashboard": True,
                                          "goal_analytics": self.retrieve_goal_analytics(),
                                          "model_analytics": model_analytics,
                                          "sense_data": sense_data,
                                          "shift_data": shift_data,
                                          "act_data": act_data}

        return super().changelist_view(request, extra_context=extra_context)
