from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from sections import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('dashboard', views.dashboard, name='dashboard'),
    # AUTH
    path('register', views.SignUp.as_view(), name='register'),
    path('login', auth_views.LoginView.as_view(), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    # Section
    path('section/create', views.CreateSection.as_view(), name='create_section'),
    path('section/<int:pk>', views.DetailSection.as_view(), name='details_section'),
    path('section/<int:pk>/update', views.UpdateSection.as_view(), name='update_section'),
    path('section/<int:pk>/delete', views.DeleteSection.as_view(), name='delete_section'),
    # Video
    path('section/<int:pk>/addvideo', views.add_video, name='add_video'),
    path('video/search', views.video_search, name='video_search'),
    path('video/<int:pk>/delete', views.DeleteVideo.as_view(), name='delete_video'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
