from django import forms
from django.conf import settings

from blog.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = (
            "parent",
            "article",
            "content",
        )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        return super(CommentForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(CommentForm, self).clean()

        # Check depth for comment.
        parent = cleaned_data["parent"]
        if parent and parent.get_depth() >= settings.MAX_DEPTH_FOR_COMMENT:
            raise (forms.ValidationError(
                   "Comments can't go deeper than {} levels."
                   .format(settings.MAX_DEPTH_FOR_COMMENT)))

        # Check for duplicate comment.
        if Comment.objects.filter(article=cleaned_data["article"], author=self.user, content=cleaned_data["content"]).exists():
            raise forms.ValidationError("Such comment is duplicate!")

        return cleaned_data


class SearchForm(forms.Form):
    phrase = forms.CharField(required=False)
    tags = forms.CharField(required=False)

    def clean_tags(self):
        cleaned_data = super(SearchForm, self).clean()
        tags = cleaned_data.get("tags")
        if not tags:
            return []
        tags = tags.split(",")
        tags = [tag.strip() for tag in tags]
        return tags

    def clean(self):
        cleaned_data = super(SearchForm, self).clean()
        if not cleaned_data.get("phrase") and not cleaned_data.get("tags"):
            raise forms.ValidationError("Specify phrase, tags or both!")
        return cleaned_data
