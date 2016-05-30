from django import forms
from myblog.models import Comment

class EmailPostForm(forms.Form):
    '''
    A form inheriting forms.Form
    '''
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required = False, widget = forms.Textarea)

class CommentForm(forms.ModelForm):
    '''
    A form inheriting ModelForms
    '''
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')