from rest_framework import serializers
from .models import *



class PolicyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolicyImage
        fields = ['id', 'image']

class PolicySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Policy
        fields = '__all__'
        
        
        