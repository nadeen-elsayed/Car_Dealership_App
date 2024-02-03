from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL
    path(route='', view=views.get_dealerships, name='index'),

    #path(route='/static', view=views.static_pages, name='static_pages'),
    # path for about view
    path(route='about/', view=views.about, name='about'),

    # path for contact us view
    path(route='contact/', view=views.contact, name='contact'),

    # path for registration
    path('registration/', views.registration_request, name='registration'),
    # path for login
    path('login/', views.login_request, name='login'),
    # path for logout
    path('logout/', views.logout_request, name='logout'),

    path(route='', view=views.get_dealerships, name='get_dealerships'),

    # path for dealer reviews view
    path(route='dealer/<int:dealer_id>/', view=views.get_dealer_details, name='dealer_details'),

    # path for add a review view
    path(route='dealer/<int:dealer_id>/add-review/', view=views.add_review, name="add_review")] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)