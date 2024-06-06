from django.contrib import messages
from django.contrib.auth import logout
from django.views.generic import ListView, DetailView, CreateView, View, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.views import LoginView

from .models import *
from .forms import *


# Create your views here.

class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'post'


class PostDetailView(DetailView):
    model = Post
    template_name = 'post/post_detail.html'
    context_object_name = 'post'


class PostCreateView(LoginRequiredMixin, View):
    template_name = 'post/post_create.html'

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


class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post/post_edit.html'
    context_object_name = 'post'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def handle_no_permission(self):
        return redirect('home')

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.pk})


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


class LoginView(LoginView):
    template_name = 'users/user_login.html'
    success_url = reverse_lazy('home')

    def get_success_url(self):
        return self.success_url

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            # Redirect authenticated users to another page, such as the home page
            return HttpResponseRedirect(reverse_lazy('home'))
        return super().dispatch(request, *args, **kwargs)


class CreateUserView(CreateView):
    form_class = UserCreationForm
    template_name = 'users/user_create.html'
    success_message = "User created successfully."
    success_url = reverse_lazy('user_login')

    def form_invalid(self, form):
        # Add your error message here
        messages.error(self.request, "User creation failed. Please check the form.")
        return super().form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            # Redirect authenticated users to another page, such as the home page
            return HttpResponseRedirect(reverse_lazy('home'))
        return super().dispatch(request, *args, **kwargs)


def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to the homepage after logout
