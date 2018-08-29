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
    url(r'^add_event$', views.add_event), # add event to calendar 
    url(r'^calendar_events$', views.calendarEvents), # grabs events turns to json for fullcalendar
    url(r'^event/(?P<id>\d+)$', views.event_info), # updates event when dragged and dropped
    url(r'^delete_event/(?P<id>\d+)$', views.delete_event), # deletes an event
    url(r'^post_message$', views.post_message), #posts a message
    url(r'^post_comment/(?P<id>\d+)$', views.post_comment), # posts a comment
    url(r'^message/(?P<id>\d+)$', views.view_message), # goes to message page
    url(r'^delete_message/(?P<id>\d+)$', views.delete_message), # deletes message
    url(r'^delete_comment/(?P<id>\d+)$', views.delete_comment), # deletes comment
    # editing users does not work######################
    url(r'^edit_user$', views.edit_user),
    url(r'^change_info$', views.change_info),
    # url(r'^change_password$', views.change_password),
    ###################################################
    url(r'^expenses$', views.expense_history), # render expense page
    url(r'^delete_expense/(?P<id>\d+)$', views.delete_expense), # deletes expense transaction history
]
