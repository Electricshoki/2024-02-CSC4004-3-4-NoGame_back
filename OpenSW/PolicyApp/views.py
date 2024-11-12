from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Policy
from .serializers import PolicySerializer

from django.shortcuts import get_object_or_404

# Create your views here.

@api_view(['GET','POST'])
def policy_list_create(request):
    
    if request.method == 'GET':
        policies = Policy.objects.all()
        serializer = PolicySerializer(policies, many=True)
        return Response(data=serializer.data)
    
    if request.method == 'POST':
        serializer = PolicySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data)