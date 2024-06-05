from django.views.generic import ListView, DetailView, CreateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .models import *
from .forms import *


# Create your views here.

class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'post'


class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'


class PostCreateView(LoginRequiredMixin, View):
    template_name = 'posts/post_create.html'

    def get(self, request):
        post_form = PostForm()
        return render(request, self.template_name, {'post_form': post_form})

    def post(self, request):
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
        return render(request, self.template_name, {'post_form': post_form})


class LocationCreateView(LoginRequiredMixin, CreateView):
    model = Location
    form_class = LocationForm
    template_name = 'location/location_create.html'
    success_url = reverse_lazy('post_create')


@login_required
@require_POST
def like_post(request):
    post_id = request.POST.get('post_id')
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(post=post, user=request.user)

    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    return JsonResponse({'liked': liked, 'like_count': post.like_set.count()})


class UserView(DetailView):
    model = User
    template_name = 'users/user_profile.html'
    context_object_name = 'user'
