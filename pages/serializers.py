from rest_framework import serializers
from pages.models import Content, Trainee


class InfoBipContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        depth = 2
        fields = (
            "title",
            "description",
            "bot_response"
        )
        
class InfoBipContentRequestSerializer(serializers.Serializer):
    bot_code = serializers.CharField(max_length=5)
    title = serializers.CharField(max_length=3000)
    
    
class TraineeSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    
    def  get_first_name(self, obj):
        return obj.user.first_name
    
    def get_last_name(self, obj):
        return obj.user.last_name
    class Meta:
        model = Trainee
        depth = 2
        fields = (
            "first_name",
            "last_name",
            "cohort",
            "business_name"
        )
        
