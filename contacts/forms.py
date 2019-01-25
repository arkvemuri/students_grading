from django import forms

class ContactForm(forms.Form):
    contact_email = forms.EmailField(required=True, label='Email')
    contact_name = forms.CharField(required=True, label='Name')
    subject = forms.CharField(required=True, label='Subject')
    message = forms.CharField(widget=forms.Textarea(attrs={'rows':4, 'cols':10}), required=True, label='Message')

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['contact_email'].widget.attrs['style'] = "width:15rem"
        self.fields['contact_name'].widget.attrs['style'] = "width:15rem"
        self.fields['subject'].widget.attrs['style'] = "width:15rem"
        self.fields['message'].widget.attrs['style'] = "width:15rem"
