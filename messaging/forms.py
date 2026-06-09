from django import forms


class MessageForm(forms.Form):
    text = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Type a message...",
                "class": "form-control",
            }
        ),
        label="",
        max_length=1000,
    )
