from rest_framework import serializers

class CalculateAndPayFareSerializer(serializers.Serializer):
    distance_travelled = serializers.FloatField()



