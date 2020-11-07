from rest_framework.serializers import ModelSerializer
from .models import Item

class ItemSerializer(ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'category', 'tags', 'description']
        read_only_fields = ['id', 'name']