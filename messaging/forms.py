from django import forms


class MessageForm(forms.Form):
    text = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Message...", "class": "form-control"}),
        label="",
        max_length=1000,
        required=False,
    )
    image = forms.ImageField(required=False)
    voice = forms.FileField(required=False)

    def clean(self):
        cleaned = super().clean()
        if not cleaned.get("text") and not cleaned.get("image") and not cleaned.get("voice"):
            raise forms.ValidationError("Message must contain text, image, or voice.")
        return cleaned
