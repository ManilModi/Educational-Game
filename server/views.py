from django.shortcuts import render
from django.http import JsonResponse
from .gemini_api import get_gemini_price

def gemini_price_view(request, symbol):
    try:
        price = get_gemini_price(symbol)
        return JsonResponse({'symbol': symbol, 'price': price})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
