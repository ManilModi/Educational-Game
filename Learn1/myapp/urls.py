from django.urls import path
from . import views
from .views import electricity_demand_plot_daily, electricity_demand_plot_hourly, cluster_residential_areas, electricity_demand_plot

urlpatterns = [
path('', views.p_home, name='home'),
# path('list', views.list_view, name='list_view'),
# path('<id>',views.detail_view, name='detail_view'),
# path('<id>/update',views.update_view, name='update_view'),
# path('<id>/delete',views.delete_view, name='delete_view'),
path('electricity_demand_daily/', electricity_demand_plot_daily, name='electricity-demand_daily'),
path('electricity_demand_hourly/', electricity_demand_plot_hourly, name='electricity-demand_hourly'),
path('residential-clusters/', cluster_residential_areas, name='residential_clusters'),
path('electricity_demand_plot/', electricity_demand_plot, name='electricity_demand_plot'),
path('register/', views.user_registration_view, name='user_registration'),
]