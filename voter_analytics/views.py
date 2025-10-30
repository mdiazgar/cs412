from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Voter

# Create your views here.

class VotersListView(ListView):
    model = Voter
    template_name = "voter_analytics/voters_list.html"
    context_object_name = "voters"
    paginate_by = 100
    ordering = ["last_name", "first_name"]
    
    
