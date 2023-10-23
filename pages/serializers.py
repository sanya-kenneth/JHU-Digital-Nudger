from rest_framework import serializers
from pages.models import Content


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
