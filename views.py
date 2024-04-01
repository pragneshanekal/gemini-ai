from django.shortcuts import render
import json
from django.http import HttpResponse, JsonResponse
from .utils import serialize_chat_history
from .models import UserSession
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import google.generativeai as genai
import os

@csrf_exempt # Remove this decorator during production
@require_http_methods(["POST"]) # Ensure only that POST requests are accepted
def chat_view(request):
    # Extract message from JSON body of the POST request
    data = json.loads(request.body)
    message = data.get('message', '')
    session_id = data.get('session_id', None)

    genai.configure(api_key=os.environ['API_KEY'])
    model = genai.GenerativeModel('gemini-pro')

    if session_id:
        user_session = UserSession.objects.filter(session_id=session_id).first()
    
    if user_session:
        chat = model.start_chat(history=user_session.history)
    else:
        user_session = UserSession.objects.create(session_id=session_id)
        chat = model.start_chat()
    
    response = chat.send_message(message)
    user_session.history = serialize_chat_history(chat.history)
    user_session.save()
    
    return JsonResponse({'response': response.text})

def index_view(request):
    return render(request, 'index.html')