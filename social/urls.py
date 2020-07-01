from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.login,name="login"),
    path('signup/',views.signup,name="signup"),
    path('',views.index,name="index"),
    path('add-post/',views.addPost,name="addPost"),
    path('add-comment/',views.addComment,name="addComment"),
    path('logout/',views.logout,name="logout"),
    path('comments/',views.comments,name="comments"),

]