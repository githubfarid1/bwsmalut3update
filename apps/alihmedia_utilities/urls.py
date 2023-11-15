from django.urls import path
from .views import inactive
prefix = __package__.split('.')[1] + "_"
urlpatterns = [
    path(route='inactive', view=inactive, name=prefix + "inactive"),



]