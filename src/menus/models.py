from django.conf import settings # In order to import the User Model.
from django.db import models
from django.urls import reverse

from restaurants.models import RestaurantLocation # In order to associate the restaurant to a given item

# Create your models here. This is where you start after running startapp.

app_name = 'menus'
class Item(models.Model):
    # Associations
    user       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # every menu item under in a restaitem has user
    restaurant = models.ForeignKey(RestaurantLocation, on_delete=models.CASCADE)
    # Item Stuff
    name       = models.CharField(max_length=120)
    contents   = models.TextField(help_text='Separate each content by comma')
    excludes   = models.TextField(blank=True, null=True, help_text='Separate each item by comma')
    public     = models.BooleanField(default=True)
    timestamp  = models.DateTimeField(auto_now_add=True)
    updated    = models.DateTimeField(auto_now=True)
    #image_url = .... A must in the Propety model.

    def __str__(self):
        return self.name

    # For individual items..
    def get_absolute_url(self): #get_absolute_url. Use this method in item_list.html
        #return f"/restaurants/{self.slug}" Removed in order to use reverse - url resolvers
        return reverse('menus:detail', kwargs={'pk': self.pk}) #changed from restaurants-detailto us the restaurants namespace

    class Meta:
        ordering = ['-updated', '-timestamp'] # Done, add the menus(AppName) model into installed apps(SF:settings), Do migrations, then Add Model into AF:admin.py

    # Continue with get functions...
    def get_contents(self):
        return self.contents.split(",")

    def get_excludes(self):
        return self.excludes.split(",") # Do your views.py inside the app, menus!


