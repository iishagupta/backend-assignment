from django.urls import path
from .views import TeamMemberListView

app_name = "teammembers" # helps do a reverse lookup later

urlpatterns = [
    path('teammembers/', TeamMemberListView.as_view()),
    path('teammembers/<int:pk>', TeamMemberListView.as_view()),
]