from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from viewer.forms import RegisterForm, GifsSearch
from viewer.models import UserGifs


def gif_page(request):
    obj = UserGifs.objects.order_by('-date_time')[:5]
    if request.GET.get('q'):
        import requests
        q = request.GET.get('q')
        user = request.GET.get('user')
        form = UserGifs(search_text=q, user_id_id=user)
        form.save()
        q = nlu(q)
        context = []
        for i in q:
            payload = {'api_key': 'bNkBDN7vEC0i6O6Wewbvveu77uxbI7KM', 'q': i, 'limit': '1', 'offset': '',
                       'rating': 'g',
                       'lang': 'en'}
            r = requests.get('https://api.giphy.com/v1/gifs/search', params=payload)
            if len(r.json()['data']) >= 1:
                context.append(r.json()['data'][0]['images']['original'])
        return render(request, 'GIF.html', {
            'context': context,
            'obj': obj
        })
    return render(request, 'GIF.html', {
        'obj': obj
    })

#
def nlu(text: str):
    import json
    from ibm_watson import NaturalLanguageUnderstandingV1
    from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
    from ibm_watson.natural_language_understanding_v1 import Features, KeywordsOptions, EntitiesOptions
    nlu_text_str = []
    api_key = 'XwUTqUc9s_447RocxcT7tMOLE7iEJ6V0XvFTUvjWAD5a'
    url = 'https://api.eu-de.natural-language-understanding.watson.cloud.ibm.com/instances/6c94ff95-22cc-4c85-bfb7-d6f55e1f3522'
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2021-03-25',
        authenticator=authenticator)

    natural_language_understanding.set_service_url(url)

    response = natural_language_understanding.analyze(
        text=text, language='en',
        features=Features(
            entities=EntitiesOptions(emotion=True, sentiment=True, limit=6),
            keywords=KeywordsOptions(emotion=True, sentiment=True, limit=6))).get_result()
    res = json.loads(json.dumps(response, indent=2))
    for e,i in res.items():
        if e == 'keywords':
            for x in res[e]:
                nlu_text_str.append(x['text'])
            break
    return nlu_text_str


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request, ('there was an error'))
            return redirect('login')
    else:
        return render(request, 'authentication/login.html',{})


def register_user(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            messages.success(request, ('there was an error'))
            return render(request, 'register.html', {'form': form})
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def log_out(request):
    logout(request)
    return redirect('login')

def gif_search(request, pk):
    p = request.GET.get('q')
    form = UserGifs(search_text=p, user_id_id=pk)
    form.save()
    context = UserGifs.objects.all()[:5]
    return render(request, 'GIF.html', {
        'obj': context
    })


class GifView(LoginRequiredMixin, ListView):
    model = User
    login_url = 'login/'
    template_name = 'authentication/login.html'
