from django.shortcuts import render
from django.http.request import HttpRequest
from django.http.response import HttpResponse
# Create your views here.

def hello_world(request : HttpRequest):
    s = "<h1>Hello world!!!</h1>"
    return HttpResponse(s)

def request_details(request: HttpRequest):
    #print("request_details")
    param_a = request.GET.get("a",-1)
    param_b = request.GET.get("b","---")
    s = f"Param A:{param_a}, Param B:{param_b}<br/>Path: {request.path}"

    headers = [str(item) for item in request.headers.items()]
    headers_str = "<br/>".join(headers)
    return HttpResponse(f"{s}<br/>{headers_str}")