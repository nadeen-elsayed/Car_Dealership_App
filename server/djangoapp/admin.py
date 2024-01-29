from django.contrib import admin
# from .models import related models
from .models import CarMake, CarModel

# Register your models here.
admin.site.register(CarMake)
admin.site.register(CarModel)
# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel 
    extra = 5
# CarModelAdmin class
class CourseAdmin(admin.ModelAdmin):
    fields = ['pub_date', 'name', 'description']
    
# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    fields = ['dealer_id', 'name', 'car_type', 'year']
    inlines = [CarModelInline]
# Register models here
