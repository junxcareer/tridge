from django import forms
from .models import Comment, Choice


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'body')


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ('choice_text',)


class SearchForm(forms.Form):
    categories = (
        (['Question', 'Choice'], 'All'),
        (['Question'], 'Question'),
        (['Choice'], 'Choice')
    )
    category = forms.ChoiceField(choices=categories)
    keyword = forms.CharField(max_length=30)
