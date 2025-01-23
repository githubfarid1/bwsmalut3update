from django.urls import path
from apps.arsip_tata import views

prefix = __package__.split('.')[1] + "_"
urlpatterns = [
    path(route='years', view=views.show_year, name=prefix + "show_year"),
    path(route='year_list', view=views.year_list, name=prefix + "year_list"),
    path(route='add_year', view=views.add_year, name=prefix + "add_year"),
    path(route='year/<int:pk>/edit', view=views.edit_year, name=prefix + "edit_year"),
    path(route='year/<int:pk>/remove', view=views.remove_year, name=prefix + 'remove_year'),

    path(route='boxes/<int:year>', view=views.show_boxes, name=prefix + "show_boxes"),
    path(route='box_list/<int:year_id>/<int:page>/<str:search>', view=views.box_list, name=prefix + "box_list"),
    path(route='add_box/<int:year_id>', view=views.add_box, name=prefix + "add_box"),
    path(route='box/<int:pk>/edit', view=views.edit_box, name=prefix + "edit_box"),
    path(route='box/<int:pk>/remove', view=views.remove_box, name=prefix + 'remove_box'),
    path(route='box/<int:pk>/sync', view=views.box_sync, name=prefix + "box_sync"),


    path(route='bundles/<int:year_date>/<str:box_number>', view=views.show_bundles, name=prefix + "show_bundles"),
    path(route='bundle_list/<int:box_id>', view=views.bundle_list, name=prefix + "bundle_list"),
    path(route='add_bundle/<int:box_id>', view=views.add_bundle, name=prefix + "add_bundle"),
    path(route='bundle/<int:pk>/edit', view=views.edit_bundle, name=prefix + "edit_bundle"),
    path(route='bundle/<int:pk>/remove', view=views.remove_bundle, name=prefix + 'remove_bundle'),
    path(route='bundle/<int:pk>/sync', view=views.bundle_sync, name=prefix + "bundle_sync"),

    # path(route='items/<int:year_date>/<int:bundle_number>', view=views.show_items, name=prefix + "show_items"),
    path(route='items/<int:bundle_id>', view=views.show_items, name=prefix + "show_items"),

    path(route='item_list/<int:bundle_id>', view=views.item_list, name=prefix + "item_list"),
    path(route='add_item/<int:bundle_id>', view=views.add_item, name=prefix + "add_item"),
    path(route='item/<int:pk>/edit', view=views.edit_item, name=prefix + "edit_item"),
    path(route='item/<int:pk>/remove', view=views.remove_item, name=prefix + 'remove_item'),
    path(route='report/<int:year>', view=views.report, name=prefix + 'report'),
    path(route='report_perbox/<int:year>/<str:box_number>', view=views.report_perbox, name=prefix + 'report_perbox'),
    path(route='label_perbox/<int:year>/<str:box_number>', view=views.label_perbox, name=prefix + 'label_perbox'),
    # path(route='label_perbundle/<int:year>/<str:bundle_number>', view=views.label_perbundle, name=prefix + 'label_perbundle'),
    path(route='label_perbundle/<int:pk>', view=views.label_perbundle, name=prefix + 'label_perbundle'),
    path(route='search_qrcode/<int:year>/<str:box_number>', view=views.search_qrcode, name=prefix + 'search_qrcode'),
    path(route='item_upload_pdf', view=views.item_upload_pdf, name=prefix + "item_upload_pdf"),
    path(route='item_download_pdf/<int:pk>', view=views.item_download_pdf, name=prefix + "item_download_pdf"),

    path(route='customers', view=views.show_customers, name=prefix + "show_customers"),
    path(route='customer_list', view=views.customer_list, name=prefix + "customer_list"),
    path(route='add_customer', view=views.add_customer, name=prefix + "add_customer"),
    path(route='customer/<int:pk>/edit', view=views.edit_customer, name=prefix + "edit_customer"),
    path(route='customer/<int:pk>/remove', view=views.remove_customer, name=prefix + 'remove_customer'),

    path(route='trans', view=views.show_trans, name=prefix + "show_trans"),
    path(route='trans_list', view=views.trans_list, name=prefix + "trans_list"),
    path(route='add_trans', view=views.add_trans, name=prefix + "add_trans"),
    path(route='trans/<int:pk>/edit', view=views.edit_trans, name=prefix + "edit_trans"),
    path(route='trans/<int:pk>/remove', view=views.remove_trans, name=prefix + 'remove_trans'),

    path(route='transdetail/<int:trans_id>', view=views.show_trans_detail, name=prefix + "show_trans_detail"),
    path(route='transdetail_list/<int:trans_id>', view=views.trans_detail_list, name=prefix + "trans_detail_list"),
    path(route='add_transdetail/<int:trans_id>', view=views.add_trans_detail, name=prefix + "add_trans_detail"),
    path(route='transdetail/<int:pk>/remove', view=views.remove_transdetail, name=prefix + 'remove_transdetail'),
    path(route='trans_form/<int:pk>', view=views.trans_form, name=prefix + 'trans_form'),

    path(route='transret', view=views.show_transret, name=prefix + "show_transret"),
    path(route='transret_list', view=views.transret_list, name=prefix + "transret_list"),
    path(route='transretdetail/<int:trans_id>', view=views.show_transret_detail, name=prefix + "show_transret_detail"),
    path(route='transretdetail_list/<int:trans_id>', view=views.transret_detail_list, name=prefix + "transret_detail_list"),
    path(route='transdetail/<int:pk>/edit', view=views.edit_transdetail, name=prefix + 'edit_transdetail'),
    path(route='transret_form/<int:pk>', view=views.transret_form, name=prefix + 'transret_form'),
   path(route='search_item', view=views.search_item, name=prefix + "search_item"),
   

]