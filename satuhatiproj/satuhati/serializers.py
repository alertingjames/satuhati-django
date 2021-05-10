from rest_framework import serializers
from .models import SatuhatiMember, Music, Like

class SatuhatiMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = SatuhatiMember
        fields = ('__all__')

class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = ('__all__')

