from django.shortcuts import render
from rest_framework.views import APIView
from my_account.models import Vehicle,Card
from django.shortcuts import get_object_or_404
from .serializers import CalculateAndPayFareSerializer
from rest_framework.response import Response
# Create your views here.
class CalculateAndPayFare(APIView):
    def post(self,request,*args,**kwargs):
        vehicle = get_object_or_404(Vehicle,id=kwargs.get('vehicle_id'))
        card = get_object_or_404(Card,user=self.request.user)
        serializer = CalculateAndPayFareSerializer(data=request.data)
        if(serializer.is_valid(raise_exception=True)):
            if vehicle.fare_per_meter <= 0:
                return Response({'message':'Invalid, fare is set to zero'})
            total_fare = vehicle.fare_per_meter
            total_cost = total_fare * request.data.get('distance_travelled')
            if(total_cost>card.balance):
                return Response({'message':'Your card do not have sufficient amount to pay'})
            card.balance = card.balance - total_cost
            card.save()
            return Response({'message':'Fare payment successfull'})



