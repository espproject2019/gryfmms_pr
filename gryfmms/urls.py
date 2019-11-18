"""gryfmms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from app import views as vapp
from loans import views as vloans

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', vapp.home, name='home'),
    path('apply/', vapp.apply, name='apply'),
    path('signin/', vapp.signin, name='signin'),
    path('apply/submitApplication', vapp.submitApplication, name='submitApplication'),

    # new loans apply
    path('loans/', vloans.loans, name='loans'),
    path('loans/submitForApproval', vloans.submitForApproval, name='submitForApproval'),
]
