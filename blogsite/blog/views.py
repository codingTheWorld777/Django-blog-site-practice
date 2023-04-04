from django.shortcuts import render
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView, 
    ListView, 
    TemplateView,
    UpdateView,
)
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from blog.models import Comment, Post
from blog.forms import CommentForm, PostForm, AuthorWidget

# Create your views here.

class AboutView(TemplateView):
    template_name = 'about.html'


class PostListView(ListView):
    model = Post

    def get_queryset(self):
        # return super().get_queryset()
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

    
class PostDetailView(DetailView):
    model = Post


class CreatePostView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # Override to pass 'user' argument to the PostForm
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')  # wait until the post actually deleted then redirect


class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'

    def get_queryset(self):
        # return super().get_queryset()
        return Post.objects.filter(published_date__isnull=True).order_by('-created_date')
    

# Comment view
@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@method_decorator(login_required, name='dispatch')
class AddCommentToPostView(View):
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # Override to pass 'user' argument to the PostForm
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        form = CommentForm()
        context = {
            'post': post,
            'form': form,
        }
        return render(request, 'blog/comment_form.html', context)

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
        context = {
            'post': post,
            'form': form,
        }
        return render(request, 'blog/comment_form.html', context)

# functional view of AddCommentToPostView
# @login_required
# def add_comment_to_post(request, pk):
#     post = get_object_or_404(Post, pk=pk)

#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.post = post
#             comment.save()
            
#             return redirect('post_detail', pk=post.pk)
    
#     else:
#         form = CommentForm()
    
#     return render(request, 'blog/comment_form.html', { 'form': form })


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()

    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()

    return redirect('post_detail', pk=post_pk)
