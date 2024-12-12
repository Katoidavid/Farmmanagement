from rest_framework import serializers

from farm_app.models import Visitorsmessage


class VisitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visitorsmessage
        fields = ['name', 'email', 'phone_number', 'gender', 'age']


