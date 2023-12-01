from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ContactUs_module.serializers import ContactSubmissionSerializer
from .models import ContactSubmission


# Create your views here.


class ContactSubmissionView(APIView):
    def get(self, request):
        ContactSubmissions = ContactSubmission.objects.all()
        serializer = ContactSubmissionSerializer(instance=ContactSubmissions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ContactSubmissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
