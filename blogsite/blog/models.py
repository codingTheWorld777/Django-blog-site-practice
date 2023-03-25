from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone

# Create your models here.

class Post(models.Model):
    author = models.ForeignKey("auth.User", verbose_name=_(""), on_delete=models.CASCADE)
    title = models.CharField(_(""), max_length=200)
    text = models.TextField(_(""))
    created_date = models.DateTimeField(_(""), default=timezone.now(), auto_now=False, auto_now_add=False)
    published_date = models.DateTimeField(_(""), blank=True, null=True)


    def publish(self):
        self.published_date = timezone.now()
        self.save()
    
    def approve_comments(self):
        return self.comments.filter(approved_comment=True)
    
    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})
    
    def __str__(self):
        return self.title
    


class Comment(model.Model):
    post = models.ForeignKey("blog.Post", related_name="comments")
    author = models.CharField(_(""), max_length=200)
    text = models.TextField(_(""))
    created_date = models.DateTimeField(_(""), default=timezone.now(), auto_now=False, auto_now_add=False)
    approved_comment = models.BooleanField(_(""), default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse("post_list", kwargs={"pk": self.pk})

    def __str__(self):
        return self.text
    