from http.client import HTTPResponse
from itertools import permutations
from urllib import request
from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpResponse
import requests
from django.core.paginator import Paginator
# Create your views here.
from price.models import bitcoin_price

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
#class price(APIView):
from datetime import datetime
from pytz import timezone
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.authtoken.models import Token as t
from django.contrib.auth.models import User
from .serializers import *
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class price(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
    
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        parameters = {
        'start':'1',
        'limit':'5',
        'convert':'USD'
        }
        headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY':'8dd845c2-097b-47a3-8924-a0f5f65a43a8'
        }

        session = Session()
        session.headers.update(headers)
        json = requests.get(url, params = parameters ,headers=headers).json()
        coins = json['data']
        s = ""
        p = ""
        t = ""
        t1 = ""
        t2 = ""
        for x in coins:
            if x['symbol'] == "BTC":
                symbol = x['symbol']
                s = symbol
                price = x['quote']['USD']['price']
                p = price
                time = x['quote']['USD']['last_updated']
                t = timezone.now()
                
                b = bitcoin_price(Symbol=symbol, price=price, time = timezone.now() )
                t1 = t.date
                t2 = t.time
                b.save()

        return Response({'name':s, 'price':p, 'time':t}, status=status.HTTP_200_OK)

    


class price_list(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        authentication_classes = [TokenAuthentication]
        permission_classes = [IsAuthenticated]
        all_price_list = bitcoin_price.objects.all().order_by('id').reverse()
        paginator = Paginator(all_price_list, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'price/home.html', {'price': page_obj})


class RegisterUser(APIView):
    def post(self, request):
        serializer = UserSerializer(data = request.data)

        if not serializer.is_valid():
            return Response({'status' : 403, 'errors' : serializer.errors, 'message' :"something went wrong"})
        serializer.save()

        user = User.objects.get(username = serializer.data['username'])

        token_obj, _  = t.objects.get_or_create(user    = user)

        return Response({'status':200, 'payload':serializer.data, 'token':str(token_obj), 'message' : "your data is saved"})

    