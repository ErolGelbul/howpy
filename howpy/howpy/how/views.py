from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from .forms import PostSearchForm
from .models import Post


class HomeView(ListView):
    model = Post
    context_object_name = "posts"
    paginate_by = 10

    def get_template_names(self):
        if self.request.htmx:
            return "how/components/post-list-elements.html"
        return "how/index.html"


def post_single(request, post):
    post = get_object_or_404(Post, slug=post, status="published")
    related = Post.objects.filter(author=post.author)[:5]
    return render(request, "how/single.html", {"post": post, "related": related})


class TagListView(ListView):
    model = Post
    paginate_by = 10
    context_object_name = "posts"

    def get_queryset(self):

        x = Post.objects.filter(tags__slug__in=[self.kwargs["tag"]])
        return x

    def get_template_names(self):
        if self.request.htmx:
            return "how/components/post-list-elements-tags.html"
        return "how/tags.html"

    def get_context_data(self, **kwargs):
        context = super(TagListView, self).get_context_data(**kwargs)
        context["tag"] = self.kwargs["tag"]
        return context


class PostSearchView(ListView):
    model = Post
    paginate_by = 10
    context_object_name = "posts"
    form_class = PostSearchForm

    def get_queryset(self):
        form = self.form_class(self.request.GET)
        if form.is_valid():
            return Post.objects.filter(title__icontains=form.cleaned_data["q"])
        return []

    def get_template_names(self):
        if self.request.htmx:
            return "how/components/post-list-elements-search.html"
        return "how/search.html"
