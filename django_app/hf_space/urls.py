from django.urls import path
from . import views
from django.views.generic import RedirectView

urlpatterns= [
    # Redirect root URL (/) to the default dashboard view
    path('', RedirectView.as_view(pattern_name='dashboard_default', permanent=False), name='root_redirect'),

    # Fallback route executing the default service_name defined in the view
    path('dashboard/', views.dashboard, name='dashboard_default'),

    # Dynamic route capturing the service_name parameter from the URL
    path('dashboard/<str:service_name>', views.dashboard, name='dashboard_service'),
]