################################################################################
################################################################################
###     BRANCH MAKER
################################################################################
################################################################################
from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings

from . import views 

app_name = 'dbcolumn_app'

urlpatterns = [
    path('dbcolumn/', views.CreatePostView.as_view(), name='all tables'),
    path('api/dbcolumns/<str:mytable>/', views.TableColumnFoundView.as_view(), name='specific-table-columns'),

]
