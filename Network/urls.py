from django.urls import path

from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('saved/', views.saved, name='saved'),
    path('profile/<str:username>', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path('search/', views.search, name='search'),
    path('follow_unfollow/<str:pk>', views.follow_unfollow, name='follow_unfollow'),
    path('post/<int:post_id>/like', views.like_post, name="likepost"),
    path("post/<int:post_id>/unlike", views.unlike_post, name="unlikepost"),
    path("post/<int:post_id>/save", views.save_post, name="savepost"),
    path("post/<int:post_id>/unsave", views.unsave_post, name="unsavepost"),
    path("createpost", views.create_post, name="createpost"),
    path('comments/<int:post_id>', views.get_comments, name="comments"),
    path('delete_comment/', views.delete_comment, name='deletecomment'),
    path('add_comment/', views.add_comment, name='addcomment'),
    path('chats/', views.chats, name='chats'),
    path('messages/<int:chat_id>', views.get_messages, name='get_messages'),
    path('add_message/', views.add_message, name='add_message'),
    path('edit_post/', views.edit_post, name='edit_post'),
    path('delete_post/', views.delete_post, name='delete_post'),
]
