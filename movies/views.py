from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .models import Movie, Comment
from .forms import MovieForm, CommentForm

# Create your views here.
def index(request):
    movies = Movie.objects.all()
    context = {'movies':movies,}
    return render(request, 'movies/index.html', context)

def create(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = MovieForm(request.POST)
            if form.is_valid():
                movie = form.save(commit=False)
                movie.user = request.user
                movie.save()
                return redirect('movies:detail', movie.pk)
        else:
            form = MovieForm()
        context = {'form':form,}
        return render(request, 'movies/create.html', context)
    return redirect('accounts:login')

def detail(request, pk):
    movie = Movie.objects.get(pk=pk)
    comment_form = CommentForm()
    comments = movie.comment_set.all()
    context = {
        'movie':movie,
        'comment_form':comment_form,
        'comments':comments,
        }
    return render(request, 'movies/detail.html', context)

def update(request, pk):
    if request.user.is_authenticated:
        movie = Movie.objects.get(pk=pk)
        if request.user == movie.user:
            if request.method == 'POST':
                form = MovieForm(request.POST, instance=movie)
                if form.is_valid():
                    form.save()
                    return redirect('movies:detail', movie.pk)
            else:
                form = MovieForm(instance=movie)
        else:
            return redirect('movies:index')
        context = {'form':form, 'movie':movie}
        return render(request, 'movies/update.html', context)
    return redirect('accounts:login')

@require_POST
def delete(request, pk):
    movie = Movie.objects.get(pk=pk)
    if request.user.is_authenticated:
        if request.user == movie.user:
            movie.delete()
            return redirect('movies:index')
    else:
        return redirect('movies:detail', movie.pk)
    
def comments_create(request, pk):
    if request.user.is_authenticated:
        movie = Movie.objects.get(pk=pk)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.movie = movie
            comment.user = request.user
            comment.save()
        return redirect('movies:detail', movie.pk)
    return redirect('accounts:login')

def comments_delete(request, movie_pk, comment_pk):
    if request.user.is_authenticated:
        comment = Comment.objects.get(pk=comment_pk)
        if request.user == comment.user:
            comment.delete()
    return redirect('movies:detail', movie_pk)

@require_POST
def likes(request, pk):
    if request.user.is_authenticated:
        movie = Movie.objects.get(pk=pk)
        if movie.like_users.filter(pk=request.user.pk).exists():
            movie.like_users.remove(request.user)
        else:
            movie.like_users.add(request.user)
        return redirect('movies:index')
    return redirect('accounts:login')