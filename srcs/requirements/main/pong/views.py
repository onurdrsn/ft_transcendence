from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Room
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
import json
import time


@login_required
def home(request):
    rooms = Room.objects.all()
    if request.method == 'POST':
        user = request.user.username
        option = request.POST.getlist('option')[0]
        room_name = request.POST.getlist('oda_ismi')[0]
        if room_name is None:
            messages.error(request, _("oda bilgisi alınamadı oda adı {}").format(room_name))
            time.sleep(2)
            return redirect("pong:home")
        if option == '1':
            game = Room.objects.filter(room_name=room_name).first()
            if game is None:
                game = Room(game_creator=user, room_name=room_name)
                game.save()
                return redirect('/pong/' + room_name)

            if game.player_count() >= 2:
                messages.success(request, _("The room is already full or finish"))
                time.sleep(2)
                return redirect("pong:home")

        if option == '2':
            game = get_object_or_404(Room, room_name=room_name)
            if game is None:
                messages.success(request, _("The room does not exist"))
                time.sleep(2)
                return redirect("pong:home")
            if game.game_creator == user:
                return redirect('/pong/' + room_name)
            elif game.game_opponent == user and game.game_creator != user:
                return redirect('/pong/' + room_name)
            if game.player_count() >= 2:
                messages.success(request, _("The room is already full or finish"))
                time.sleep(2)
                return redirect("pong:home")
            game.game_opponent = user
            game.save()
            return redirect('/pong/' + room_name)
    return render(request, 'anasayfa.html', {'rooms': rooms})


@login_required
def room(request, room_name):
    game = get_object_or_404(Room, room_name=room_name)

    return render(request, "oda.html", {
        'room_name': room_name,
        'user': lambda: request.user.username if request.user.username == game.game_creator else game.game_opponent,
        'creator': game.game_creator,
        'opponent': game.game_opponent,
        'winner': game.winner,
        'game_over': game.is_over
        })


@login_required
def game_history(request):
    return render(request, "history.html", {'game_history': Room.objects.all()})


@login_required
def update(request, room_name):
    if request.method == 'POST':
        winner = json.loads(request.body).get('winner')
        if not winner:
            return JsonResponse({'success': False, 'error': _('Invalid request method')})
        game = get_object_or_404(Room, room_name=room_name)
        game.winner = winner
        game.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': _('Invalid request method')})


@login_required()
def fetch_rooms(request):
    rooms = Room.objects.all()
    rooms_list = [
        {
            'name': room.room_name,
            'size': room.player_count(),
            'creator': room.game_creator,
            'opponent': room.game_opponent,
            'is_over': room.is_over
        }
        for room in rooms
    ]
    # JSON yanıtını döndür
    return JsonResponse({'rooms': rooms_list})


def tournament(request):
    return render(request, 'turnuva.html')
