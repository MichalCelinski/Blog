from django import forms


class EmailArticleForm(forms.Form):
    sender = forms.CharField(max_length=20,
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Twoje Imię'}))
    email_sender = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control',
                                                                   'placeholder': 'Twój adres e-mail'}))
    email_receiver = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control',
                                                                     'placeholder': 'Adres e-mail Twojego Znajomego'}))
    message = forms.CharField(max_length=200,
                              required=False,
                              widget=forms.Textarea(attrs={'class': 'form-control',
                                                           'placeholder': 'Jeśli chcesz wpisz tutaj treść wiadomości'}))
