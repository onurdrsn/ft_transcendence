from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import TicTacToe
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
import json
import time


@login_required
def tictac(request):
    if request.method == 'POST':
        user = request.user.username
        option = request.POST.get('option')
        room_code = request.POST.get('room_code')
        if room_code is None:
            messages.error(request, _("oda bilgisi alınamadı oda adı {}").format(room_code))
            time.sleep(2)
            return redirect("/tictac")
        if option == '1':
            game = TicTacToe.objects.filter(room_code=room_code).first()
            if game is None:
                messages.error(request, _("Room code not found"))
                time.sleep(2)
                return HttpResponseRedirect('/tictac')

            if game.player_count() >= 2:
                messages.error(request, _("The room is already full"))
                time.sleep(2)
                return HttpResponseRedirect('/tictac')

            game.game_opponent = user
            game.save()
            return redirect('/tictac/' + room_code)

        elif option == '2':
            game = get_object_or_404(TicTacToe, room_code=room_code)
            if game is None:
                messages.success(request, _("The room does not exist"))
                time.sleep(2)
                return redirect("/tictac")
            if game.game_creator == user:
                return redirect('/tictac/' + room_code)
            elif game.game_opponent == user and game.game_creator != user:
                return redirect('/tictac/' + room_code)
            if game.player_count() >= 2:
                messages.success(request, _("The room is already full or finish"))
                time.sleep(2)
                return redirect("pong:home")
            game.game_opponent = user
            game.save()
            return redirect('/tictac/' + room_code)
    return render(request, "front.html")


@login_required
def play(request, room_code):
    game = get_object_or_404(TicTacToe, room_code=room_code)

    return render(request, "play.html", {
        'room_code': room_code,
        'user': lambda: request.user.username if request.user.username == game.game_creator else game.game_opponent,
        'creator': game.game_creator,
        'opponent': game.game_opponent,
        'winner': game.winner
        })


def game_history(request):
    return render(request, "game_history.html", {
        'game_history': TicTacToe.objects.all(),
    })


@login_required
def update_winner(request, room_code):
    if request.method == 'POST':
        winner = json.loads(request.body).get('winner')
        if not winner:
            return JsonResponse({'success': False, 'error': _('Invalid request method')})
        game = get_object_or_404(TicTacToe, room_code=room_code)
        game.winner = winner
        game.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': _('Invalid request method')})
