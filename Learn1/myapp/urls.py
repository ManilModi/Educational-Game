from django.urls import path
from . import views

urlpatterns = [
path('', views.p_home, name='home'),
path('electricity_demand_daily/', views.electricity_demand_plot_daily, name='electricity-demand_daily'),
path('residential_clusters/', views.residential_clusters, name='residential_clusters'),
path('electricity_demand_plot/', views.electricity_demand_plot, name='electricity_demand_plot'),
path('electricity_demand_prediction/', views.electricity_demand_prediction, name='electricity_demand_prediction'),
path('register/', views.user_register, name='user_registration'),
path('login/', views.user_login, name='login'),
path('logout/', views.user_logout, name='logout'),
path('about/', views.about, name='about'),
path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
path('govt_dashboard/', views.govt_dashboard, name='govt_dashboard'),
path('normal_dashboard/', views.normal_dashboard, name='normal_dashboard'),
path('entrepreneur_dashboard/', views.entrepreneur_dashboard, name='entrepreneur_dashboard'),
path('researcher_dashboard/', views.researcher_dashboard, name='researcher_dashboard'),
path('createroles/', views.creatRroles, name='create_roles'),
path('admin_create_user/', views.admin_create_user, name='admin_create_user'), 
path('unauthorized/', views.unauthorized_access, name='unauthorized_access'),
path('update_credentials/', views.update_credentials, name='update_credentials'),
path('update_upperlevel/', views.update_upperlevel, name='update_upperlevel'),
path('delete_user/', views.delete_user, name='delete_user'),
path('electricity_demand_plot_daily/', views.electricity_demand_plot_daily, name='electricity_demand_plot_daily'),
path('electricity_demand_plot_monthly/', views.electricity_demand_plot_monthly, name='electricity_demand_plot_monthly'),
path("chatbot/", views.chatbot_ui, name="chatbot_ui"),
path("query/", views.chatbot_view, name="chatbot_query"),
]