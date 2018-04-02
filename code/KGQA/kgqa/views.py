from django.shortcuts import render
import sys
from kgqa.KB_query import query_main

# Create your views here.

def search_post(request):
    ctx = {}
    if request.POST:
        question = request.POST['query']
        ctx['result'] = query_main.query_function(question)
        print(ctx['result'])
    return render(request, "post.html", ctx)
