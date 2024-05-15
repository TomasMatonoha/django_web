from django.shortcuts import render, get_object_or_404, redirect, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import *
from .forms import PostForm, CommentForm

# Create your views here.

