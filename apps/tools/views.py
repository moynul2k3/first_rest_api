from django.shortcuts import render
from django.http import JsonResponse
from django.middleware.csrf import get_token

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import *
from .serializers import *

def get_csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})


class BannerView(APIView):
    def get(self, request):
        banners = Banner.objects.all()
        serializer = BannerSerializer(
            banners, many=True, context={'request': request})
        return Response(serializer.data)
