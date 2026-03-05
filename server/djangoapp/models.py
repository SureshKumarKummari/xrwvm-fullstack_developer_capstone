# Uncomment the following imports before adding the Model code

from django.db import models
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

# Car Make model
class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    country = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.name


# Car Model model
class CarModel(models.Model):

    # Many-to-One relationship with CarMake
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)

    dealer_id = models.IntegerField()

    name = models.CharField(max_length=100)

    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        ('HATCHBACK', 'Hatchback'),
        ('COUPE', 'Coupe'),
    ]

    type = models.CharField(max_length=10, choices=CAR_TYPES, default='SUV')

    year = models.IntegerField(
        default=2023,
        validators=[
            MaxValueValidator(2023),
            MinValueValidator(2015)
        ]
    )

    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.car_make.name} {self.name}"
