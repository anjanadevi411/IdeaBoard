from django import forms
from django.forms import BaseModelFormSet
from django.core.exceptions import ValidationError
from .models import TopicModel,IdeaModel


class TopicForm(forms.ModelForm):
    '''topicname = forms.CharField(label='Topicname', max_length=100)
    author_created = forms.CharField(label='Author',max_length=50,required=False)'''

    class Meta:
        model = TopicModel
        fields = ['topicname']

    def clean(self):
        super(TopicForm, self).clean()
        try:
            topicname = self.cleaned_data.get('topicname')
            TopicModel.objects.get(topicname__icontains=topicname)
            raise forms.ValidationError('Topic Already exists!')
        except TopicModel.DoesNotExist:
            return self.cleaned_data

class IdeaForm(forms.ModelForm):
    class Meta:
        model = IdeaModel
        fields = ['topicname_idea','idea']

    def clean(self):
        super(IdeaForm, self).clean()
        try:
            idea = self.cleaned_data.get('idea')
            IdeaModel.objects.get(idea__icontains=idea)
            raise forms.ValidationError('Idea already given')
        except IdeaModel.DoesNotExist:
            return self.cleaned_data

class BaseIdeaFormset(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.queryset = IdeaModel.objects.none()

    def clean(self):
        super(BaseIdeaFormset, self).clean()
        if any(self.errors):
            return
        ideas = []
        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):
                continue
            idea = form.cleaned_data.get('idea')
            if idea in ideas:
                raise ValidationError("Idea already given.")
            ideas.append(idea)




