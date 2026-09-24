from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name='home'),
    path('login_page/',login_page,name='login_page'),
    path('login_fun/',login_fun,name='login_fun'),
    path("logout/",logout_view,name="logout_view"),
    
    # Admin Functions 
    path('admin_dashboard/',admin_dashboard,name='admin_dashboard'),
    path('add_Agent/',add_Agent,name="add_Agent"),
    path('add_agent_fun/',add_agent_fun,name='add_agent_fun'),
    path('check_username/',check_username,name='check_username'),
    path('check_contact/',check_contact,name='check_contact'),
    path('check_email/',check_mail,name='check_email'),
    path('view_agents/',view_agents,name='view_agents'),
    path('view_agent_profile/<int:id>/',view_agent_profile,name="view_agent_profile"),
    path('edit_agent_profile/<int:id>/',edit_agent_profile,name='edit_agent_profile'),
    path('delete_agent/<int:id>/',delete_agent,name='delete_agent'),
    path('add_campaign/',add_campaign,name='add_campaign'),
    path('view_campaign/',view_campaign,name='view_campaign'),
    path('edit_campaign/<int:id>/',edit_campaign,name='edit_campaign'),
    path('delete_campaign/<int:id>/',delete_campaign,name='delete_campaign'),
    path("view_clients_admin_profile/<int:id>/",view_client_admin_profile,name='view_client_admin_profile'),
    path('view_clients_by_admin/<int:id>/',view_clients_by_admin,name='view_clients_by_admin'),

    # Agent FUnctions
    path('agent_dashboard/',agent_dashboard,name='agent_dashboard'),
    path('view_my_campaigns/',view_my_campaigns,name='view_my_campaigns'),
    path('add_client/',add_client,name='add_client'),
    path('add_client_fun/',add_client_fun,name='add_client_fun'),
    path('check_aadhar/',check_aadhar,name='check_aadhar'),
    path('check_client_contact/',check_client_contact,name='check_client_contact'),
    path('check_client_email/',check_client_email,name='check_client_email'),
    path('check_pan/',check_pan,name='check_pan'),
    path('reset_pass/',reset_pass,name='reset_pass'),
    path('reset_pass_fun/',reset_pass_fun,name='reset_pass_fun'),
    path('view_clients/',view_clients,name='view_clients'),
    path('view_client_profile/<int:id>/',view_client_profile,name='view_client_profile'),
    path('view_profile/',view_profile,name='view_profile'),
    path('edit_profile/<int:id>/',edit_profile,name='edit_profile'),
    path('add_client_campaign/<int:id>/',add_client_campaign,name='add_client_campaign'),
    path('view_clients_campaign/<int:id>/',view_clients_campaign,name='view_clients_campaign'),
    path('add_client_camppage/<int:id>/',add_client_camppage,name='add_client_camppage'),
    path('edit_client_profile/<int:id>/',edit_client_profile,name='edit_client_profile'),
    path('delete_client_profile/<int:id>/',delete_client_profile,name='delete_client_profile'),
    path('view_camp_clients/<int:id>/',view_camp_clients,name='view_camp_clients')
]