from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render

# Create your views here.
from django.views.generic import ListView
from blog.forms import CommentForm, EmailPostForm

from blog.models import Post


class PostListView(ListView):
    """
    Alternative post list view
    """

    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/post/list.html"


def post_list(request):
    posts = Post.published.all()
    paginator = Paginator(posts, 3)
    page_number = request.GET.get("page", 1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:  # i think it would be better to raise 404 here instead of returning last page or even raising a custom error can be useful
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)  # should this be nammed a page not posts ?
    return render(request, "blog/post/list.html", {"posts": posts})


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
    return render(request, "blog/post/detail.html", {"post": post, "comments": comments, "form": form})


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
    return render(request, "blog/post/comment.html", ctx) # whyy ? this doesn't seem to be clean design for me. i think we could have made it in the same post details view
