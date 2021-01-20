from django import forms
from django.forms import BaseModelFormSet
from .models import EvaluationQModel,ProsModel
from django.core.exceptions import ValidationError

class EvaluationQForm(forms.ModelForm):
    class Meta:
        model = EvaluationQModel
        fields = ['question']

    def clean(self):
        super(EvaluationQForm, self).clean()
        try:
            question = self.cleaned_data.get('question')
            EvaluationQModel.objects.get(question__icontains=question)
            raise forms.ValidationError('Question Already exists!')
        except EvaluationQModel.DoesNotExist:
            return self.cleaned_data

class BaseProsFormset(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.queryset = ProsModel.objects.none()

    def clean(self):
        super(BaseProsFormset, self).clean()
        if any(self.errors):
            return
        pross = []
        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):
                continue
            pros = form.cleaned_data.get('pros')
            if pros in pross:
                raise ValidationError("Pros already given.")
            pross.append(pros)

class BaseConsFormset(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.queryset = ConsModel.objects.none()

    def clean(self):
        super(BaseConsFormset, self).clean()
        if any(self.errors):
            return
        conss = []
        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):
                continue
            cons = form.cleaned_data.get('cons')
            if cons in conss:
                raise ValidationError("cons already given.")
            conss.append(cons)

