from django.urls import path
from .views import Tasklist , TaskDetail , TaskCreate, TaskEdit , TaskDelete , CustomLoginView , RegisterUser
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/',CustomLoginView.as_view(), name='login'),
    path('logout/',LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterUser.as_view(), name = 'register'),
    path('',Tasklist.as_view(), name='task'),
    path('task/<int:pk>/',TaskDetail.as_view(), name='tasks'),
    path('create-task/',TaskCreate.as_view(), name='create-task'),
    path('edit-task/<int:pk>/',TaskEdit.as_view(), name='edit-task'),
    path('delete-task/<int:pk>/',TaskDelete.as_view(), name='delete-task'),
]
 