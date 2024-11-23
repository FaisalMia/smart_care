from django.shortcuts import render
from rest_framework import viewsets,filters
from .import models
from .import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from .import serializers

# Create your views here.
class SpecializationViewSet(viewsets.ModelViewSet):
    queryset = models.Specialization.objects.all()
    serializer_class = serializers.SpecializationSerilizer
    
class DesignationViewSet(viewsets.ModelViewSet):
    queryset = models.Designation.objects.all()
    serializer_class = serializers.DesignationSerilizer
    
class AvailableTimeForSpecificDoctor(filters.BaseFilterBackend):
    def filter_queryset(self, request, query_set, view):
        doctor_id = request.query_params.get("doctor_id")
        if doctor_id:
            return query_set.filter(doctor = doctor_id)
        return query_set
     
class AvailableTimeViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = models.AvailableTime.objects.all()
    serializer_class = serializers.AvailableTimeSerilizer
    filter_backends = [AvailableTimeForSpecificDoctor]
    
class DoctorPagination(PageNumberPagination):
        page_size = 1 # item per page
        page_size_query_param = page_size
        max_page_size = 100

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = models.Doctor.objects.all()
    serializer_class = serializers.DoctorSerializer
    filter_backends = [filters.SearchFilter]
    pagination_class = DoctorPagination
    search_fields = ['user__first_name', 'user__email', 'designation__name', 'specialization__name']
    
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     print(self.request.query_params)
    #     doctor_id = self.request.query_params.get('doctor_id')
    #     if doctor_id:
    #         queryset = queryset.filter(doctor_id=doctor_id)
    #     return queryset
    
class ReviewViewSet(viewsets.ModelViewSet):
    
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerilizer