from django import forms


class ImageCreateForm(forms.Form):
    title = forms.CharField(max_length=200)
    url = forms.URLField(max_length=2000, widget=forms.HiddenInput)
    description = forms.CharField()

    def clean_url(self) -> str or forms.ValidationError:
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg', 'png']
        extension = url.rsplit('.', 1)[1].lower()

        if extension not in valid_extensions:
            raise forms.ValidationError('The given URL does not match valid image extensions.')

        return url
