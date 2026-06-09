from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["image", "caption"]
        widgets = {
            "caption": forms.Textarea(attrs={"rows": 3, "placeholder": "Write a caption..."}),
        }

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if not image:
            raise forms.ValidationError("Image is required.")
        return image


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {
            "text": forms.TextInput(attrs={"placeholder": "Add a comment...", "class": "form-control"}),
        }
        labels = {"text": ""}
