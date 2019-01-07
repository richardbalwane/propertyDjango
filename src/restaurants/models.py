from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.urls import reverse

from .utils import unique_slug_generator
from .validators import validate_category


User = settings.AUTH_USER_MODEL

class RestaurantLocationQueryset(models.query.QuerySet):
    def search(self,query): # RestaurantLocation.objects.all().search(query) # RestaurantLocation.obects.filter(something).search()
        if query:
            query = query.strip()
            return self.filter(
                Q(name__icontains=query)|
                Q(location__icontains=query)|
                Q(location__iexact=query)|
                Q(category__icontains=query)|
                Q(category__iexact=query)|
                Q(item__name__icontains=query)|
                Q(item__contents__icontains=query)
                ).distinct()
        return self

class RestaurantLocationManager(models.Manager): #Model Manager to handle filters in user.html searches...
    def get_queryset(self):
        return RestaurantLocationQueryset(self.model,using=self._db)

    def search(self, query): #RestaurantLocation.objects.search()
        return self.get_queryset().search(query)

class RestaurantLocation(models.Model):
    owner      = models.ForeignKey(User, on_delete=models.CASCADE) # class_instance.model_set.all()
    name       = models.CharField(max_length=120)
    location   = models.CharField(max_length=120, null=True, blank=True)
    category   = models.CharField(max_length=120, null=True, blank=True, validators=[validate_category])
    timestamp  = models.DateTimeField(auto_now_add=True)
    updated    = models.DateTimeField(auto_now=True)
    slug       = models.SlugField(null=True, blank=True)

    objects = RestaurantLocationManager() # add Model.objects.all()

    def __str__(self):
        return self.name

    def get_absolute_url(self):

        return reverse('restaurants:detail', kwargs={'slug': self.slug})
    @property
    def title(self):
	    return self.name #object.title

def rl_pre_save_receiver(sender, instance, *args, **kwargs):
    instance.category = instance.category.capitalize()
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(rl_pre_save_receiver, sender=RestaurantLocation)
