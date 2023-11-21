from django.urls import path
from apps.arsip_tata import views

prefix = __package__.split('.')[1] + "_"
urlpatterns = [
    path(route='years', view=views.show_year, name=prefix + "show_year"),
    path(route='year_list', view=views.year_list, name=prefix + "year_list"),
    path(route='add_year', view=views.add_year, name=prefix + "add_year"),
    path('years/<int:pk>/edit', view=views.edit_year, name=prefix + "edit_year"),
    path('years/<int:pk>/remove', view=views.remove_year, name=prefix + 'remove_year'),

    path(route='boxes/<int:year>', view=views.show_boxes, name=prefix + "show_boxes"),
    path(route='box_list/<int:year_id>', view=views.box_list, name=prefix + "box_list"),
    path(route='add_box/<int:year_id>', view=views.add_box, name=prefix + "add_box"),
    path('boxes/<int:pk>/edit', view=views.edit_box, name=prefix + "edit_box"),
    path('boxes/<int:pk>/remove', view=views.remove_box, name=prefix + 'remove_box'),

]