"""CampingPro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import url

import camping_map.views
from camping_map import *
from camping_map.views import get_nearest_sbb_station, seen_dataset, camping_dataset, sbb_dataset, \
    river_dataset, camping_dataset2, borders_dataset, get_region_ninecut, get_ninecut_matrix, \
    get_ninecut_intint, get_ninecut_intbound, get_ninecut_intext, get_ninecut_boundint, get_ninecut_boundbound, \
    get_ninecut_boundext, get_ninecut_extint, get_ninecut_extbound, get_ninecut_extext, sbb_water_dataset, routing

urlpatterns = [
    # path('admin/', admin.site.urls),
    url(r'^$', camping_map.views.home, name='home'),
    url(r'^ajax/ninecut/$', get_region_ninecut, name='ninecut'),
    url(r'^ajax/ninecut_matrix/$', get_ninecut_matrix, name='ninecut_matrix'),
    url(r'^ajax/ninecut_intint/$', get_ninecut_intint, name='ninecut_intint'),
    url(r'^ajax/ninecut_intbound/$', get_ninecut_intbound, name='ninecut_intbound'),
    url(r'^ajax/ninecut_intext/$', get_ninecut_intext, name='ninecut_intext'),
    url(r'^ajax/ninecut_boundint/$', get_ninecut_boundint, name='ninecut_boundint'),
    url(r'^ajax/ninecut_boundbound/$', get_ninecut_boundbound, name='ninecut_boundbound'),
    url(r'^ajax/ninecut_boundext/$', get_ninecut_boundext, name='ninecut_boundext'),
    url(r'^ajax/ninecut_extint/$', get_ninecut_extint, name='ninecut_extint'),
    url(r'^ajax/ninecut_extbound/$', get_ninecut_extbound, name='ninecut_extbound'),
    url(r'^ajax/ninecut_extext/$', get_ninecut_extext, name='ninecut_extext'),
    url(r'^lake_data/$', seen_dataset, name='lakes'),
    url(r'^camping_data/$', camping_dataset, name='camping'),
    url(r'^border_data/$', borders_dataset, name='border'),
    url(r'^ajax/camping_data2/$', camping_dataset2, name='camping2'),
    url(r'^ajax/routing/$', routing, name='routing'),
    url(r'^ajax/sbb_water_data/$', sbb_water_dataset, name='sbb_water'),
    url(r'^ajax/nearest_sbb/$', get_nearest_sbb_station, name='nearest_sbb'),
    url(r'^sbb_data/$', sbb_dataset, name='sbb'),
    url(r'^river_data/$', river_dataset, name='river'),
]
