from django.urls import path

from final_project.chat import views

urlpatterns = [
    path('', views.InboxView.as_view(), name='chat-inbox'),
    path('<int:pk>/', views.ConversationView.as_view(), name='chat-conversation'),
    path('lessons/<int:pk>/start-chat/', views.StartLessonConversationView.as_view(), name='lesson-start-chat')
]
