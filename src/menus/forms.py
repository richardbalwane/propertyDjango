from django import forms

# For the queryset that we need to get the user we add to the fields here
from restaurants.models import RestaurantLocation
from .models import Item

class ItemForm(forms.ModelForm):  # check whether "ItemForm" it's not a Python class
    class Meta:
        model = Item
        fields = [
            'restaurant',
            'name',
            'contents',
            'excludes',
            'public'
        ]  # Now, go import this in your views.py

    def __init__(self, user=None, *args, **kwargs):
        #print(kwargs.pop('user')) ... comment since we've included user=None
        print(user)
        print(kwargs)
        super(ItemForm, self).__init__(*args, **kwargs) # We've passed in a user into the item form, in a registered window.
        # Now update the form fields with the user that is coming in with the foreign key.
        self.fields['restaurant'].queryset = RestaurantLocation.objects.filter(owner=user) #.exclude(item__isnull=False) #...New Restaurant doesn't show in drop down , the swap! filter(owner=user)
