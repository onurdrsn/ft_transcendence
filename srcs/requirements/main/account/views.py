from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth import login, authenticate, logout
from django.db.models import Q
from .forms import AccountForm, UserRegisterForm, AccountUpdateForm
from .models import User
from friend.models import Friend, FriendRequest
from friend.utils import get_friends_request_or_false
from friend.status import Status
from django.utils.translation import gettext_lazy as _
from .utils import last_seen, online
from django.contrib.auth.decorators import login_required


def logout_view(request):
    if not request.user.is_authenticated:
        return HttpResponse(_("Please login first."))

    logout(request)
    return redirect('/')


def login_view(request, *args, **kwargs):
    if request.user.is_authenticated:
        return redirect("/")

    context = {}

    if request.POST:
        form = AccountForm(request.POST)
        if form.is_valid():
            user = authenticate(email=request.POST['email'], password=request.POST['password'])
            if user:
                login(request, user)
                destination = get_redirect_if_exists(request)
                if destination:
                    return redirect(destination)
                return redirect("/")
    else:
        form = AccountForm()
    context['login_form'] = form
    return render(request, "html/login.html", context)


def get_redirect_if_exists(request):
    redirects = None
    if request.GET:
        if request.GET['next']:
            redirects = str(request.GET['next'])
    return redirects


def signup(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return HttpResponse(_('You\'ve already signed up. Please login again.'))

    context = {}
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')
            firstname = form.cleaned_data.get('first_name')
            lastname = form.cleaned_data.get('last_name')
            account = authenticate(email=email, password=raw_password, first_name=firstname, last_name=lastname)
            login(request, account)
            destination = get_redirect_if_exists(request)
            if destination:
                return redirect(destination)
            return redirect('/')
        else:
            context['registration_form'] = form
    return render(request, 'html/register.html', context=context)


@login_required(login_url='account:login')
def account_view(request, *args, **kwargs):
    """
    logic here is kind of tricky
    is_self -> boolean
        is_friend -> boolean
            -1: no request
            0: then sent you
            1: you sent to then
    """
    context = {}
    try:
        if kwargs['user_id']:
            # always other user
            account = User.objects.get(pk=kwargs['user_id'])
    except User.DoesNotExist:
        return HttpResponse(_("User does not exist"))

    if account:
        context['id'] = account.id
        context['username'] = account.username
        context['email'] = account.email
        context['firstname'] = account.first_name
        context['lastname'] = account.last_name
        context['profile_image'] = account.profile_image.url
        context['hide_email'] = account.hide_email
    try:
        friend_list = Friend.objects.get(user=account)
    except Friend.DoesNotExist:
        friend_list = Friend(user=account)
        friend_list.save()
    if request.user.is_authenticated:
        is_blocked = Friend.objects.get(user=request.user).is_blocked(account)
        if not is_blocked and Friend.objects.get(user=account).is_blocked(request.user):
            return HttpResponseForbidden(_("U are blocked by this {} user.").format(account))
        context['is_blocked'] = is_blocked
    friends = friend_list.friends.all()
    context['friends'] = friends
    # define state template variable
    is_self = True
    is_friend = False
    user = request.user
    request_sent = Status.NO_REQUEST_SENT.value
    friend_request = None
    if user.is_authenticated and user != account:
        is_self = False
        if friends.filter(pk=user.id):
            is_friend = True
        else:
            is_friend = False
            # case 1: request has been sent from them to u: THEM_SENT
            if get_friends_request_or_false(sender=account, receiver=user):
                request_sent = Status.THEM_SENT_TO_U.value
                context['pending_friend_request_id'] = get_friends_request_or_false(sender=account, receiver=user).pk
            # case 2: request has been sent from u to them: U_SENT
            elif get_friends_request_or_false(sender=user, receiver=account):
                request_sent = Status.U_SENT_TO_THEM.value
                context['pending_friend_request_id'] = get_friends_request_or_false(sender=user, receiver=account).pk
            # case 3: no request has been sent: NO_REQUEST
            else:
                request_sent = Status.NO_REQUEST_SENT.value
    elif not user.is_authenticated:
        is_self = False
    else:
        try:
            friend_request = FriendRequest.objects.filter(receiver=user, is_active=True)
        except FriendRequest.DoesNotExist:
            pass

    context['is_self'] = is_self
    context['is_friend'] = is_friend
    context['BASE_URL'] = settings.BASE_URL
    context['request_sent'] = request_sent
    context['friend_request'] = friend_request
    context['online'] = online(account.username)
    context['last_seen'] = last_seen(account.username)
    return render(request, "html/account.html", context)


@login_required(login_url='account:login')
def profile_search_view(request, *args, **kwargs):
    context = {}
    if request.method == "GET":
        try:
            query = request.GET.get("q")
            if len(query) > 0:
                result = User.objects.filter(Q(email__icontains=query) | Q(username__icontains=query))
                user = request.user
                accounts = []  # [(account1, True), (account2, False), ...]
                if user.is_authenticated:
                    # get the authenticated users friend list
                    auth_user_friend_list = Friend.objects.get(user=user)
                    for account in result:
                        accounts.append((account, auth_user_friend_list.is_mutual_friend(account)))
                    context['accounts'] = accounts
                else:
                    for account in result:
                        accounts.append((account, False))
                    context['accounts'] = accounts
        except Exception:
            HttpResponse(_("Invalid query"))
    return render(request, "html/search.html", context)


@login_required(login_url='account:login')
def edit_account_view(request, *args, **kwargs):
    try:
        account = User.objects.get(pk=kwargs['user_id'])
    except User.DoesNotExist:
        return HttpResponse(_("something went wrong"))
    if account.pk != request.user.pk:
        return HttpResponse(_("U cannot edit this account"))
    context = {}
    if request.POST:
        form = AccountUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            # account.profile_image.delete()
            form.save()
            return redirect("account:account_view", user_id=account.pk)
        else:
            form = AccountUpdateForm(
                initial={
                    "id": account.pk,
                    "username": account.username,
                    "email": account.email,
                    "first_name": account.first_name,
                    "last_name": account.last_name,
                    "profile_image": account.profile_image,
                    "hide_email": account.hide_email
                }
            )
            context['form'] = form
    else:
        form = AccountUpdateForm(
            initial=
            {
                "id": account.pk,
                "username": account.username,
                "email": account.email,
                "first_name": account.first_name,
                "last_name": account.last_name,
                "profile_image": account.profile_image,
                "hide_email": account.hide_email
            }
        )
        context['form'] = form
    context['DATA_UPLOAD_MEMORY_SIZE'] = settings.DATA_UPLOAD_MEMORY_SIZE
    return render(request, "html/edit_account.html", context)


def home_view(request):
    return render(request, "html/home.html")
