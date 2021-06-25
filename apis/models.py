from django.db import models


# Create your models here.

class Pizza(models.Model):
    REGULAR = 'R'
    SQUARE = 'S'
    TYPES = [(REGULAR, 'Regular'), (SQUARE, 'Square')]
    type = models.CharField(db_column = 'pizza_type', max_length = 2, choices = TYPES)
    size = models.CharField(db_column = 'pizza_size', max_length = 100)
    toppings = models.CharField(db_column = 'toppings_list', max_length = 5000)
