from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views.generic import (
    View,
    TemplateView,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.http import HttpResponseRedirect
from .models import Post
from .forms import CommentForm, PostForm
from django.contrib import messages


def post_create(request):

    post_form = PostForm(request.POST or None, request.FILES or None)
    context = {
        'post_form': post_form,
    }

    if request.method == "POST":
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post_form = post_form.save(commit=False)
            post_form.author = request.user
            post_form.status = 1
            post_form.save()
            return redirect('blog')
    else:
        post_form = PostForm()
    return render(request, 'post_create.html', context)


def post_edit(request, slug):

    post = get_object_or_404(Post, slug=slug)
    post_form = PostForm(request.POST or None, instance=post)
    context = {
        "post_form": post_form,
        "post": post
    }
    if request.method == "POST":
        post_form = PostForm(request.POST, request.FILES, instance=post)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog')
    else:
        post_form = PostForm(instance=post)
    return render(request, "post_edit.html", context)


def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)
    context = {
        "post": post
    }
    # post = Post.objects.get(Post, slug=slug)
    if request.method == "POST":
        post.delete()
        messages.success(request, "Post successfully deleted!")
        return redirect('blog')
    return render(request, "post_delete.html", context)


def categories(request, cats):
    post_category = Post.objects.filter(category=cats)
    return render(request, "categories.html", {"cats": cats, "post_category":post_category})


class PostList(ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "blog.html"
    paginate_by = 6


# class CreatePost(CreateView):
#     model = Post
#     form_class = PostForm
#     template_name = "post_create.html"

#     def new_post(request, self):
#         # submitted = False
#         if request.method == "POST":
#             form_class = PostForm(request.POST)
#             if form.is_valid():
#                 form.save()
#         context = {'form_class':form_class}
#         return render(request, 'post_create.html', context)
    #     return render(request, 'blog.html')
    # else:
    #     form_class = PostForm
    #     if submitted in request.Get:
    #         submitted = True
    #     return render(request, 'blog.html')

    # def form_valid(self, form):
    #     """Function to set signed in user as author of form to post"""
    #     form.instance.author = self.request.user
    #     return super().form_valid(form)


class Home(TemplateView):
    template_name = "index.html"


class PostDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": False,
                "liked": liked,
                "comment_form": CommentForm()
            },
        )

    def post(self, request, slug, *args, **kwargs):

        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
        else:
            comment_form = CommentForm()

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": True,
                "comment_form": comment_form,
                "liked": liked
            },
        )


class PostLike(View):

    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))
