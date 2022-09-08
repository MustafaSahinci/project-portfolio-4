from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
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
from .models import Post, Category, Profile, User
from .forms import CommentForm, PostForm, ProfileForm
from django.contrib import messages
from django.urls import reverse_lazy


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
    if request.method == "POST":
        post.delete()
        messages.success(request, "Post successfully deleted!")
        return redirect('blog')
    return render(request, "post_delete.html", context)


def categories(request, cats):

    post_category = Post.objects.filter(
        status=1, category=cats).order_by("-created_on")
    paginator = Paginator(post_category, 6)
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, "categories.html", {"post_category": post_category,
                  "cats": cats, 'page': page, 'post_list': post_list})


class ProfileDetails(DetailView):
    model = Profile
    template_name = "profile_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_posts = Post.objects.filter(
            status=1, author=self.kwargs["pk"]).order_by("-created_on")
        logged_user = get_object_or_404(Profile, id=self.kwargs["pk"])
        context["logged_user"] = logged_user
        context['user_posts'] = user_posts
        return context


class ProfileCreate(CreateView):
    model = Profile
    template_name = "profile_create.html"
    form_class = ProfileForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ProfileEdit(UpdateView):
    model = Profile
    template_name = "profile_edit.html"
    form_class = ProfileForm
    success_url = reverse_lazy("home")


class PostList(ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "blog.html"
    paginate_by = 6


class Home(TemplateView):
    template_name = "index.html"

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all
        context = super(Home, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        return context


class PostDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("created_on")
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
        comments = post.comments.filter(approved=True).order_by("created_on")
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
