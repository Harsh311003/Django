from django.contrib import admin
from django.urls import path
from blogApp.views import (
    home_view,
    login_view,
    logout_view,
    user_signup,
    profile_view,
    logout_view,
    category_view,
    createBlog_view,
    follow_user,
    update_blog,
    blog_view,
    delete_blog,
    show_drafts,
    publish_blog,
    like_blog,
    rateBlog    
)


urlpatterns = [
   path('', home_view, name = 'home'),
   path('login/',login_view, name = 'login'),
   path('logout/', logout_view, name = 'logout'),
   path('signup/', user_signup, name='signup'),
   path('profile/<int:req_user_id>/', profile_view, name = 'profile'),
   path('category/<int:category_id>/',category_view, name = 'category' ),
   path('createBlog/',createBlog_view, name = 'createBlog' ),
   path('follow/<int:req_user_id>/',follow_user, name = 'follow'),
   path('blog/<int:blog_id>/', blog_view, name = 'blog'),
   path('blog/<int:blog_id>/update/', update_blog, name='update_blog'),
   path('blog/<int:blog_id>/delete/', delete_blog, name='delete_blog'),
   path('blog/<int:blog_id>/publish/', publish_blog, name='publish_blog'),
    path('blog/<int:blog_id>/like/', like_blog, name='like_blog'),
   path('drafts', show_drafts, name='drafts'),
   path('blog/<int:blog_id>/rate/', rateBlog, name = 'blogRating')

]
