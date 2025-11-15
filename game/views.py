from django.shortcuts import render
import json 
import random
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

# Kein globaler Context mehr!

def main(request):
    # GET-Request für HTML-Seite
    return render(request, 'index.html')


@require_http_methods(["POST"])
def game(request):
    # Initialisiere Session-Scores beim ersten Aufruf
    if 'user_score' not in request.session:
        request.session['user_score'] = 0
        request.session['computer_score'] = 0
    
    try:
        data = json.loads(request.body)
        user = data.get('userChoice')  # Sicherer als data['userChoice']
        
        # Validierung
        choices = ['rock', 'paper', 'scissors']  # KORREKTER Name!
        if user not in choices:
            return JsonResponse({'error': 'Invalid choice'}, status=400)
        
        computer_choice = random.choice(choices)
        
        # Spiellogik
        if user == computer_choice:
            result = 'Draw'
        elif (user == 'rock' and computer_choice == 'scissors') or \
             (user == 'paper' and computer_choice == 'rock') or \
             (user == 'scissors' and computer_choice == 'paper'):
            result = 'You Win'
            request.session['user_score'] += 1
        else:
            result = 'Computer Wins'
            request.session['computer_score'] += 1
        
        # Session speichern
        request.session.modified = True
        
        return JsonResponse({
            'result': result,
            'user': request.session['user_score'],
            'computer': request.session['computer_score'],
            'computerChoice': computer_choice
        })
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'Server error'}, status=500)
    
    
    
def resetGame(request):
    request.session['user_score'] = 0
    request.session['computer_score'] = 0
    
    return  JsonResponse({
        'user': request.session['user_score'],
        'computer':request.session['computer_score'],
    })