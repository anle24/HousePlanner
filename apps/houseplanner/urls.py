from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index), # renders splash page
    url(r'^login$', views.login), # renders login page
    url(r'^process_logreg$', views.process_logreg), # processes login and registration
    url(r'^dashboard$', views.dashboard), # renders dashboard page
    url(r'^join_create$', views.join_create), # renders join or create page after successful registration
    url(r'^create_house/(?P<code>\w+)$', views.create_house), # creates a house
    url(r'^join_house$', views.join_house), # joins a user to an exisiting house
    url(r'^logout$', views.logout), # logs user off
    url(r'^calendar$', views.calendar), # renders calendar page
    url(r'^group_charge$', views.group_charge), # renders group charge page
    url(r'^create_transaction$', views.create_transactions), # create transaction in model
]
