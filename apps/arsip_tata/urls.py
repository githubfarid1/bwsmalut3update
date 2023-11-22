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

    path(route='bundles/<int:year_date>/<int:box_number>', view=views.show_bundles, name=prefix + "show_bundles"),
    path(route='bundle_list/<int:box_id>', view=views.bundle_list, name=prefix + "bundle_list"),
    path(route='add_bundle/<int:box_id>', view=views.add_bundle, name=prefix + "add_bundle"),
    path('bundles/<int:pk>/edit', view=views.edit_bundle, name=prefix + "edit_bundle"),
    path('bundles/<int:pk>/remove', view=views.remove_bundle, name=prefix + 'remove_bundle'),

    path(route='items/<int:year_date>/<int:bundle_number>', view=views.show_items, name=prefix + "show_items"),
    path(route='item_list/<int:bundle_id>', view=views.item_list, name=prefix + "item_list"),
    path(route='add_item/<int:bundle_id>', view=views.add_item, name=prefix + "add_item"),
    path('items/<int:pk>/edit', view=views.edit_item, name=prefix + "edit_item"),
    path('items/<int:pk>/remove', view=views.remove_item, name=prefix + 'remove_item'),

]