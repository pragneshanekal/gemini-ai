from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.apps import apps
from django.http import JsonResponse
from .models import UserSession
from chatbot.services import get_response
import json

@csrf_exempt # Remove this decorator during production
@require_http_methods(["POST"]) # Ensure only that POST requests are accepted
def chat_view(request):

    # Extract message from JSON body of the POST request
    data = json.loads(request.body)
    message = data.get('message', '')
    session_id = data.get('session_id', None)
    user_session = UserSession.objects.filter(session_id=session_id).first()

    if user_session:
        history = get_response(message, user_session.history)
    else:
        user_session = UserSession.objects.create(session_id=session_id)
        history = get_response(message)
    
    response = history[len(history)-1]['parts'][0]

    user_session.history = history
    user_session.save()

    return JsonResponse({'response': response})

# Create your views here.
def index_view(request):
    return render(request, 'index.html')