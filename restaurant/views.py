from django.shortcuts import render
from restaurant.models import Restaurant
from restaurant.serializers import RestaurantSerializer
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response


class RestaurantViewSet(viewsets.ModelViewSet):
	queryset = Restaurant.objects.all()
	serializer_class = RestaurantSerializer