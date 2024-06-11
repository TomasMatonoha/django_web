from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, DetailView, CreateView, View, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
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


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('home')


class LocationCreateView(LoginRequiredMixin, CreateView):
    model = Location
    form_class = LocationForm
    template_name = 'location/location_create.html'
    success_url = reverse_lazy('post_create')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class LocationDeleteView(LoginRequiredMixin, DeleteView):
    model = Location
    success_url = reverse_lazy('post_create')  # Redirect to the post create page after deletion


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
