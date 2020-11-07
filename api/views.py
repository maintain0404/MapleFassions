from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from .models import Item
from .serializers import ItemSerializer
from functools import partial
# Create your views here.

class ItemListView(APIView):
    def get(self, request):
        filters = []
        category = request.GET.get('category')
        if category:
            filters.append(('category__exact', category))
        
        result = Item.objects.all()
        for x in filters:
            temp = partial(result.filter)
            temp.keywords[x[0]] = x[1]
            result = temp()
        result = result.order_by('id')

        return Response(
            JSONRenderer().render(ItemSerializer(result, many = True).data)
        )