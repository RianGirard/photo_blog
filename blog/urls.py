from django.urls import path
from django.views.generic.dates import ArchiveIndexView
from . import views 
from blog.models import Post
from blog.views import PostYearArchiveView
from blog.views import PostMonthArchiveView
from blog.views import PostArchiveIndexView

app_name = "blog"

urlpatterns = [
    path("", views.HomePage.as_view(), name="index"),

    path("<int:pk>/", views.PostDetailView.as_view(), name="detail"),
    path("edit/<int:pk>/", views.post_edit, name="edit"),
    path("photos/<int:pk>/", views.photos_upload, name="photos"),
    path("photos_clear/<int:pk>/", views.photos_clear, name="photos_clear"),
    path("confirm_delete/<int:pk>/", views.confirm_delete, name="confirm_delete"),
    path("delete/<int:pk>/", views.PostDeleteView.as_view(), name="delete"),
    path("new/", views.CreateNewPost.as_view(), name="new_post"),
    path("archive/", PostArchiveIndexView.as_view(model=Post, date_field="updated_at"), name="archive"),
    path("archive/<int:year>/", PostYearArchiveView.as_view(), name="archive_year"),
    path("archive/<int:year>/<int:month>/", PostMonthArchiveView.as_view(month_format='%m'), name="archive_month_numeric"),
    path('enter_comment', views.enter_comment),
    path('delete_comment', views.delete_comment),

]