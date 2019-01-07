from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView

from.forms import ItemForm
from .models import Item

# Create your views here.

class HomeView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, "home.html", {})

        user = request.user
        is_following_user_ids = [x.user.id for x in user.is_following.all()]
        # same as...
        # for x in user.is_following.all():
        #    list_.append(x.user.id)
        qs = Item.objects.filter(user__id__in=is_following_user_ids, public=True).order_by("-updated")[:3]
        return render(request, "menus/home-feed.html", {'object_list': qs})

class ItemListView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)

class ItemDetailView(LoginRequiredMixin, DetailView):
    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)

class ItemCreateView(LoginRequiredMixin, CreateView):
    template_name = 'form.html'
    form_class = ItemForm

    # To avoid: IntegrityError at /items/create/ ....NOT NULL constraint failed: menus_item.user_id
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        return super(ItemCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(ItemCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs #Args to pass into our ItemForm form_class, so we can tie entries to a particulat user!
        # Handle these args inside forms.py!
        # Since this opens the form in the incognito window, we need to ensure required login with Mixins!

    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)

    def get_context_data(self, *args, **kwargs): # Shared form.html
        context = super(ItemCreateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Create Item'
        return context

class ItemUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'menus/detail-update.html'
    form_class = ItemForm

    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)

# The last two require a form, create forms.py in the app folder, menus!
# Wrap these views in your app urls, create urls.py in your app folder, menus!

    def get_context_data(self, *args, **kwargs): # Shared form.html
        context = super(ItemUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Update Item'
        return context

    # The same arguments in the ItemCreateView, lest the Restaurant field inthe form is empty
    def get_form_kwargs(self):
        kwargs = super(ItemUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
