from django.contrib.auth.decorators import login_required # login decorator, forces u to login before u see form!
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView

from .forms import RestaurantCreateForm, RestaurantLocationCreateForm
from .models import RestaurantLocation


class RestaurantListView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        return RestaurantLocation.objects.filter(owner=self.request.user) # owner being the logged in user!


class RestaurantDetailView(LoginRequiredMixin, DetailView):
    def get_queryset(self):
        return RestaurantLocation.objects.filter(owner=self.request.user) #.filter(category__iexact='asian') # fitler by user

class RestaurantCreateView(LoginRequiredMixin, CreateView):
    form_class = RestaurantLocationCreateForm
    login_url = '/login/'
    template_name = 'form.html'
    #success_url = '/restaurants/' Removed so we can do get_absolute_url

    def form_valid(self, form):
        instance = form.save(commit=False) # first avoid saving...
        instance.owner = self.request.user # LoginRequiredMixin ensures request.user is authenticated
        return super(RestaurantCreateView, self).form_valid(form) # similar to form.save() in the FBV --- Saving here

    def get_context_data(self, *args, **kwargs): # Replicated in menu app for share of form.html
        context = super(RestaurantCreateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Add Restaurant'
        return context

class RestaurantUpdateView(LoginRequiredMixin, UpdateView):
    form_class = RestaurantLocationCreateForm
    login_url = '/login/'
    template_name = 'restaurants/detail-update.html'
    #success_url = '/restaurants/' Removed so we can do get_absolute_url

    def get_context_data(self, *args, **kwargs): # Replicated in menu app for share of form.html
        context = super(RestaurantUpdateView, self).get_context_data(*args, **kwargs)
        name = self.get_object().name
        context['title'] = f'Update Restaurant: {name}' # In order to have the tittle/name of the respective restaurant.
        return context

    def get_queryset(self):
        return RestaurantLocation.objects.filter(owner=self.request.user)
