from django import forms

from blog.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content", )


class SearchForm(forms.Form):
    phrase = forms.CharField(required=False)
    tags = forms.CharField(required=False)

    def clean_tags(self):
        cleaned_data = super(SearchForm, self).clean()
        tags = cleaned_data.get("tags")
        if not tags:
            return []
        return tags.split(",")

    def clean(self):
        cleaned_data = super(SearchForm, self).clean()
        if not cleaned_data.get("phrase") and not cleaned_data.get("tags"):
            raise forms.ValidationError("Specify phrase, tags or both!")
        return cleaned_data
