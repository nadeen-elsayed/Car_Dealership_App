import sys
from django.utils.timezone import now
try:
    from django.db import models
except Exception:
    print("There was an error loading django modules. Do you have django installed?")
    sys.exit()

from django.conf import settings
import uuid

# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object

class CarMake(models.Model):
    name = models.CharField(null=False, max_length=30, default='none')
    desc = models.CharField(null=False, max_length=30, default='none')
    
    
    # Create a toString method for object string representation
    def __str__(self):
        return "Car Name: " + self.name + " Description: " + self.desc

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object

class CarModel(models.Model):
    SUV = 'SUV'
    SEDAN = 'Sedan'
    WAGON = 'Wagon'
    CAR_CHOICES = [
        (SUV, 'SUV'),
        (SEDAN, 'Sedan'),
        (WAGON, 'Wagon')
    ]
    car_type = models.CharField(
        null=False,
        max_length=20,
        choices=CAR_CHOICES,
        default=SUV
    )
    name = models.CharField(null=False, max_length=30, default='none')
    dealer_id =models.IntegerField()
    car_make = models.ForeignKey(CarMake, null=True, on_delete=models.CASCADE)
    year = models.DateField(null=True)

        # Create a toString method for object string representation
    def __str__(self):
        return "Car Name: " + self.name + " Car Type: " + self.car_type 
# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
