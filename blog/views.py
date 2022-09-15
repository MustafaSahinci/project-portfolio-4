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
from .models import Post, Category, Profile, User, Comment
from .forms import CommentForm, PostForm, ProfileForm
from django.contrib import messages
from django.urls import reverse_lazy


class PostCreate(CreateView):
    """Create the view for Creating a post"""
    model = Post
    template_name = "post_create.html"
    form_class = PostForm

    def form_valid(self, form):
        """Function to set signed in user as author of form to post"""
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostEdit(UpdateView):
    """create the view for Updating the post"""
    model = Post
    template_name = "post_edit.html"
    form_class = PostForm

    def form_valid(self, form):
        """Function to set signed in user as author of form to post"""
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDelete(DeleteView):
    """Create the view for deleting the post"""
    model = Post
    template_name = "post_delete.html"
    success_url = reverse_lazy("blog")


def categories(request, cats):
    """create the view for the categories"""
    post_category = Post.objects.filter(
        category=cats).order_by("-created_on")

    """Paginate by 6 for function view"""
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
    """Create the view for profile details"""
    model = Profile
    template_name = "profile_detail.html"

    def get_context_data(self, **kwargs):
        """Get user posts and user id"""
        context = super().get_context_data(**kwargs)
        user_posts = Post.objects.filter(
            author=self.kwargs["pk"]).order_by("-created_on")
        logged_user = get_object_or_404(Profile, id=self.kwargs["pk"])
        context["logged_user"] = logged_user
        context['user_posts'] = user_posts
        return context


class ProfileCreate(CreateView):
    """"Create the view for creating a profile"""
    model = Profile
    template_name = "profile_create.html"
    form_class = ProfileForm

    def form_valid(self, form):
        """Function to set signed in user as user of form to profile"""
        form.instance.user = self.request.user
        return super().form_valid(form)


class ProfileEdit(UpdateView):
    """Create the view for editing profile"""
    model = Profile
    template_name = "profile_edit.html"
    form_class = ProfileForm


class PostList(ListView):
    """Create the view for all posts paginated by 6"""
    model = Post
    queryset = Post.objects.order_by("-created_on")
    template_name = "blog.html"
    paginate_by = 6


class Home(TemplateView):
    """Create the view for home page"""
    template_name = "index.html"

    def get_context_data(self, *args, **kwargs):
        """Get the categories for the dropdown in the nav bar"""
        cat_menu = Category.objects.all
        context = super(Home, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        return context


class PostDetail(View):
    """"create the view for the post details"""
    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.order_by("created_on")
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
        queryset = Post.objects
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.order_by("created_on")
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
    """Create the view for clicking like on the post details"""
    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))


class CommentDelete(DeleteView):
    """Create the view for deleting comments"""
    model = Comment
    template_name = "comment_delete.html"

    def test_func(self):
        comment = self.get_object()
        return comment.name == self.request.user.username

    def get_success_url(self):
        """reverse to post_detail after deleting"""
        post = self.object.post
        return reverse_lazy('post_detail', kwargs={'slug': post.slug})


class CommentEdit(UpdateView):
    model = Comment
    template_name = "comment_edit.html"
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        """reverse to post_detail after Updating"""
        post = self.object.post
        return reverse_lazy('post_detail', kwargs={'slug': post.slug})
