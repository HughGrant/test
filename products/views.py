# from django.shortcuts import render
from django.http import JsonResponse
from products.models import Keyword
from django.views.generic import View


class KeywordView(View):

    def post(self, request):
        print(request.POST)

    def get(self, request):
        return JsonResponse({'msg': 'hello word'})
