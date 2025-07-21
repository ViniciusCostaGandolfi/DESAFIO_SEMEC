"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import include, path

from src.common.views import render_messages_view
from src.sales.views.management import sales_list_view

urlpatterns = [
    path('admin/', admin.site.urls),

    path('sales/', include(('src.sales.urls', 'sales'))),
    path('inventory/', include(('src.inventory.urls', 'inventory'))),

    path('', include(('src.users.urls', 'users'))),

    path('', sales_list_view, name='home'),

    path('render-messages/', render_messages_view, name='render_messages'),
]
