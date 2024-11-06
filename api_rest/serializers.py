from rest_framework import serializers
from .models.callEnd import CallEnd
from .models.callStart import CallStart


class CallEndSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallEnd
        fields = '__all__'


class CallStartSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallStart
        fields = '__all__'
