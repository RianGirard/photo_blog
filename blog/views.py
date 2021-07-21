from typing import Text
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.dates import ArchiveIndexView     # See here for archive details: https://docs.djangoproject.com/en/3.2/ref/class-based-views/generic-date-based/
from django.views.generic.dates import YearArchiveView
from django.views.generic.dates import MonthArchiveView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage

from .models import Post, Photo, Comment, User


class HomePage(LoginRequiredMixin, TemplateView):
    http_method_names = ['get']
    template_name = "blog/homepage.html"
    model = Post
        
    def dispatch(self, request, *args, **kwargs):                   # this "Mixin" method here... 
        self.request = request
        return super().dispatch(request, *args, **kwargs)           # allows us to reference self.request.user ... 
    
    def get_context_data(self, *args, **kwargs):                    # This is a "Mixin" Method, or "ContextMixin" that allows the sending in of additional context variables
        context = super().get_context_data(*args, **kwargs)         # Note used in DetailView class below too
        posts = Post.objects.filter(published='yes').order_by('-updated_at')[0:30]      # See: https://docs.djangoproject.com/en/3.2/ref/class-based-views/mixins-simple/
        unpub_posts = Post.objects.filter(published='no').order_by('-updated_at')
        context['posts'] = posts
        context['unpub_posts'] = unpub_posts
        context['photos'] = Photo.objects.all()
        return context

class PostDetailView(DetailView):
    context_object_name = "post"
    model = Post
    http_method_names = ['get']
    template_name = "blog/detail.html"

    def get_context_data(self, **kwargs):                       # Mixins are like "extender" methods that are available for access by Class Based Views
        context = super().get_context_data(**kwargs)            # I couldn't figure how to filter the Photo.objects by pk, which DetailView does not let me pass from urls.py
        context['photos'] = Photo.objects.all()                 # So I send in "all" and filter on template -- not efficient! 
        return context


def post_edit(request, pk):
    if request.method == 'POST':
        post = Post.objects.get(id=pk)
        post.title=request.POST['title']
        post.desc=request.POST['desc']
        print(request.POST['published'])
        if request.POST['published'] == "yes":
            post.published='yes'
        else: 
            post.published='no'
        post.save()
        return redirect(f'/{pk}')
    else:
        context = {
            "post": Post.objects.get(id=pk),
        }
        return render(request, "blog/edit.html", context)

def photos_upload(request, pk):
    if request.method == 'POST':                                # Solution! https://www.geeksforgeeks.org/django-upload-files-with-filesystemstorage/
        request_file = request.FILES['media'] if 'media' in request.FILES else None
        if request_file:
            # fs = FileSystemStorage()                          # this section puts photo in /media for reference directly by link (fileurl)...
            # file = fs.save(request_file.name, request_file)   # but we don't need that as will create a Photo object instead in following lines! 
            # fileurl = fs.url(file)
            # print(fileurl)
            post = Post.objects.get(id=pk)
            Photo.objects.create(file=request_file, post=post)  # create Photo object! 
            print("It's alive!")
        return redirect(f'/{pk}')
    elif request.method == 'GET':
        context = {
            "photos": Photo.objects.filter(post=pk),
            "post": Post.objects.get(id=pk),
        }
        return render(request, "blog/photos.html", context)
    else:
        return redirect('/')

def photos_clear(request, pk):
    post = Post.objects.get(id=pk)
    photos = Photo.objects.filter(post=post)
    for photo in photos:
        photo.delete()
    return redirect(f'/{pk}')

def confirm_delete(request, pk):
    post = Post.objects.get(id=pk)
    context = {
        "post": post,
    }
    return render(request, "blog/confirm_delete.html", context)

class PostDeleteView(DeleteView):
    model = Post
    success_url ='/'
    
class CreateNewPost(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "blog/create.html"
    fields = ['title', 'desc', 'author', 'published']
    success_url = "/"

    def dispatch(self, request, *args, **kwargs):           # dispatch is required to give self.request a value, so that it can be assigned below as "author"
        self.request = request
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.save()
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        post = Post.objects.create(
            title=request.POST.get("title"),
            desc=request.POST.get("desc"),
            author=request.user,
            published=request.POST.get("published"),
        )
        return render(
            request,
            "includes/post.html",
            {
                "post": post,
                "show_detail_link": True,
            },
            content_type="application/html"
        )


class PostArchiveIndexView(LoginRequiredMixin, ArchiveIndexView):
    date_list_period = "month"                  # This is view that comes "batteries included" with Django:  
                                                # https://docs.djangoproject.com/en/3.2/ref/class-based-views/generic-date-based/
class PostYearArchiveView(LoginRequiredMixin, YearArchiveView):     # default context that is send into templates is: "date_list"
    queryset = Post.objects.filter(published='yes')
    date_field = "updated_at"
    make_object_list = True                     # View has default "object_list" in context for the defined queryset (Post)
    allow_future = True

class PostMonthArchiveView(LoginRequiredMixin, MonthArchiveView):
    queryset = Post.objects.filter(published='yes')
    date_field = "updated_at"
    allow_future = True

    def get_context_data(self, **kwargs):                       # Mixin method, as above
        context = super().get_context_data(**kwargs)            
        context['photos'] = Photo.objects.all()
        return context

def enter_comment(request):
    if request.method == "POST":
        author = User.objects.get(id=request.POST['user_id'])
        post = Post.objects.get(id=request.POST['post_id'])
        Comment.objects.create(
            comment=request.POST['comment'],
            author=author,
            post=post,
        )
    return HttpResponse("")          # sending HttpResponse just to send something; AJAX performs reload of screen;

def delete_comment(request):
    if request.method == "POST":
        comment = Comment.objects.get(id=request.POST['comment_id'])
        comment.delete()
    return HttpResponse("")