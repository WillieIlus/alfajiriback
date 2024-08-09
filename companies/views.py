from django.shortcuts import render

from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework import status

from .models import Company
from .serializers import CompanySerializer

from accounts.models import User
from categories.models import Category
from locations.models import Location

class CategoryCompanyViewSet(ListAPIView):
    serializer_class = CompanySerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        category = Category.objects.get(slug=self.kwargs['slug'])
        return Company.objects.filter(category=category)


class CompanyListCreateAPIView(ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    lookup_field = 'slug'
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return []


class CompanyRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    lookup_field = 'slug'

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.request.method == 'DELETE' or self.request.method == 'PUT':
            return [IsAuthenticated()]
        return []
    
    def delete(self, request, *args, **kwargs):
        company = Company.objects.get(slug=self.kwargs['slug'])
        company.delete()
        return Response(status=204)
    
    def put(self, request, *args, **kwargs):
        company = Company.objects.get(slug=self.kwargs['slug'], user=request.user)
        serializer = CompanySerializer(company, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def patch(self, request, *args, **kwargs):
        company = Company.objects.get(slug=self.kwargs['slug'])
        serializer = CompanySerializer(company, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    
class CompanyLocationViewSet(ListAPIView):
    serializer_class = CompanySerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        location = Location.objects.get(slug=self.kwargs['slug'])
        return Company.objects.filter(location=location)
    
    
class CompanyCategoryViewSet(ListAPIView):
    serializer_class = CompanySerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        category = Category.objects.get(slug=self.kwargs['slug'])
        return Company.objects.filter(category=category)
    
    
class MyCompanyViewSet(ListAPIView):
    serializer_class = CompanySerializer
    lookup_field = 'slug'
    # permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user =self.request.user
        return Company.objects.filter(user=user)

        
