from django.http.request import HttpRequest

def show_ua(request : HttpRequest):
    return {
        "user_agent" : request.headers.get("User-Agent")
    }