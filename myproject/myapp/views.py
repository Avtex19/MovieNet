import requests
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView
from .models import Movie
from .forms import MovieForm
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='login')
def home(request):
    movie_data = []

    if request.method == 'POST':
        if 'submit-name' in request.POST:
            movie = request.POST.get('name')
            url = f'http://www.omdbapi.com/?t={movie}&apikey=e2fb3558'

            if movie:
                movie_name = requests.get(url).json()
                if movie_name.get('Response') == 'False':
                    messages.error(request, 'Invalid movie name')
                else:
                    movie_descr = {
                        'name': movie_name['Title'],
                        'year': movie_name['Year'],
                        'released': movie_name['Released'],
                        'genre': movie_name['Genre'],
                        'director': movie_name['Director'],
                        'actors': movie_name['Actors'],
                        'plot': movie_name['Plot'],
                        'imdb_rating': movie_name['imdbRating'],
                    }
                    #if any values of the API is blank, than we write N/A(Not Available)
                    for key,value in movie_descr.items():
                            if value == '':
                                movie_descr[key] = 'N/A'
                    movie_data.append(movie_descr)

        else:
            if request.method == 'POST':
                movie_name = request.POST.get('movieName')
                if movie_name:
                    # Check if the movie is already in favorites
                    if Movie.objects.filter(user=request.user, name=movie_name).exists():
                        message = 'Movie is already in favorites.'
                    else:
                        # Add the movie to favorites
                        movie = Movie(user=request.user, name=movie_name)
                        movie.save()
                        message = 'Movie added to favorites.'

                    response_data = {'message': message}
                    return JsonResponse(response_data)
                    
    context = {
        'movie_info': movie_data
    }

    return render(request, 'home.html', context)




class CustomLoginView(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterView, self).form_valid(form)

    def form_invalid(self, form):
        for errors in form.errors.values():
            for error in errors:
                messages.error(self.request, error)
        return super(RegisterView, self).form_invalid(form)

    # we block authenticated user from register page
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterView, self).get(*args, **kwargs)


@login_required(login_url='login')
def favorites(request):
    favorite_movies = Movie.objects.filter(user=request.user)
    context = {
        'favorite_movies': favorite_movies
    }
    return render(request, 'personal.html', context)
