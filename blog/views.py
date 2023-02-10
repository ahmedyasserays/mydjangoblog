from django.core.mail import send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from django.db.models import Exists, OuterRef, Count, Q
from taggit.models import Tag

from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from .forms import EmailPostForm, CommentForm, SearchForm
from blog.models import Post

# Create your views here.


class PostListView(ListView):
    """
    Alternative post list view
    """

    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/post/list.html"

    def get_queryset(self):
        qs = Post.objects.filter(status=Post.Status.PUBLISHED).annotate(
            has_tags=Exists(Tag.objects.filter(post__id=OuterRef("id")))
        )
        if self.kwargs.get("slug"):
            qs = qs.filter(tags__slug=self.kwargs.get("slug"))
        qs = qs.prefetch_related("tags")
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["tag"] = (
            Tag.objects.get(slug=self.kwargs.get("slug"))
            if self.kwargs.get("slug")
            else None
        )
        return ctx


def post_list(request, slug=None):
    posts = Post.published.all()
    tag = None
    if slug:
        tag = get_object_or_404(Tag, slug=slug)
        posts = posts.filter(tags__in=[tag])
    paginator = Paginator(posts, 3)
    page_number = request.GET.get("page", 1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:  # i think it would be better to raise 404 here instead of returning last page or even raising a custom error can be useful
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)  # should this be nammed a page not posts ?
    ctx = {
        "posts": posts,
        "tag": tag,
    }
    return render(request, "blog/post/list.html", ctx)


def post_detail(request, year, month, day, slug):
    post = get_object_or_404(
        Post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
        slug=slug,
        status=Post.Status.PUBLISHED,
    )
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    # Form for users to comment
    form = CommentForm()
    tags = post.tags.all().values_list("id", flat=True)
    related_posts = (
        Post.objects.filter(tags__in=tags)
        .exclude(id=post.id)
        .annotate(tags_count=Count("tags", filter=Q(id__in=tags)))
        .order_by("-tags_count", "-publish")[:4]
    )
    ctx = {
        "post": post,
        "comments": comments,
        "form": form,
        "related_posts": related_posts,
    }
    return render(
        request,
        "blog/post/detail.html",
        ctx,
    )


def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == "POST":
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            # ... send email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}'s comments: {cd['comments']}"
            )
            send_mail(subject, message, "your_account@gmail.com", [cd["to"]])
            sent = True
    else:
        form = EmailPostForm()
    ctx = {
        "post": post,
        "form": form,
        "sent": sent,
    }

    return render(request, "blog/post/share.html", ctx)


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    # A comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a Comment object without saving it to the database
        comment = form.save(commit=False)
        # Assign the post to the comment
        comment.post = post
        # Save the comment to the database
        comment.save()
    ctx = {
        "post": post,
        "form": form,
        "comment": comment,
    }
    return render(
        request, "blog/post/comment.html", ctx
    )  # whyy ? this doesn't seem to be clean design for me. i think we could have made it in the same post details view

def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if "query" in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            # search_vector = SearchVector('title', weight='A') + \
            #                 SearchVector('body', weight='B')
            # search_query = SearchQuery(query)
            # results = Post.published.annotate(
            #     search=search_vector,
            #     rank=SearchRank(search_vector, search_query)
            # ).filter(rank__gte=0.3).order_by('-rank')
            results = Post.published.annotate(
                similarity=TrigramSimilarity('title', query),
                ).filter(similarity__gt=0.1).order_by('-similarity')
    return render(
        request,
        "blog/post/search.html",
        {"form": form, "query": query, "results": results},
    )
