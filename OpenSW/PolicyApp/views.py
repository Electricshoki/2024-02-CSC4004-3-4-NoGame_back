from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Policy, PolicyImage
from .serializers import PolicySerializer, PolicyImageSerializer

from django.shortcuts import get_object_or_404

# Create your views here.

@api_view(['GET','POST'])
def policy_list_create(request):
    
    if request.method == 'GET':
        policies = Policy.objects.all()
        serializer = PolicySerializer(policies, many=True)
        return Response(data=serializer.data)
    
    if request.method == 'POST':
        policy_serializer = PolicySerializer(data=request.data)
        if policy_serializer.is_valid(raise_exception=True):
            serializer.save()
            policy = policy_serializer.save()  # Policy 객체 저장
            
            # 다중 이미지 처리
            images = request.FILES.getlist('images')
            for image in images:
                PolicyImage.objects.create(policy=policy, image=image)
            
            return Response(data=PolicySerializer(policy).data)