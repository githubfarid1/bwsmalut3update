# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.urls import path, include  # add this

urlpatterns = [
    path('admin/', admin.site.urls),          # Django admin route
    path("", include("apps.authentication.urls")), # Auth routes - login / register

    # ADD NEW Routes HERE

    # Leave `Home.Urls` as last the last line
    path("", include("apps.home.urls")),
    path('alihmedia_inactive/', include('apps.alihmedia_inactive.urls')),
    path('alihmedia_utilities/', include('apps.alihmedia_utilities.urls')),
    path('alihmedia_vital/', include('apps.alihmedia_vital.urls')),
    path('arsip_inaktif/', include('apps.arsip_inaktif.urls')),
    # path('file_explorer/', include('apps.file_explorer.urls')),
    path('fm_pjpa/', include('apps.fm_pjpa.urls')),
    path('fm_pjsa/', include('apps.fm_pjsa.urls')),
    path('fm_opsda/', include('apps.fm_opsda.urls')),
    path('fm_balai/', include('apps.fm_balai.urls')),

]
