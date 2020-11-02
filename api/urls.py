

from django.urls import path

from api import views

urlpatterns = [
    path('book/', views.BookAPIView.as_view()),
    path('book/<id>/', views.BookAPIView.as_view()),

    path('books/', views.BookGenericAPIView.as_view()),
    path('books/<id>/', views.BookGenericAPIView.as_view()),

    path('study/', views.BookGenerics.as_view()),
    path('study/<id>/', views.BookGenerics.as_view()),

    path('user/', views.UserAPIView.as_view({"post":"register"})),
    path('user/<id>/', views.UserAPIView.as_view({"post":"register"})),

    path('login/', views.UserAPIView.as_view({"post":"login"})),
    path('login/<id>/', views.UserAPIView.as_view({"post":"login"})),
]
