from django import forms
from .models import Question, Choice

class QuestionForm(forms.ModelForm):
    choice1 = forms.CharField(max_length=80, required=False, label="Choix 1")
    choice2 = forms.CharField(max_length=80, required=False, label="Choix 2")
    choice3 = forms.CharField(max_length=80, required=False, label="Choix 3")
    choice4 = forms.CharField(max_length=80, required=False, label="Choix 4")
    choice5 = forms.CharField(max_length=80, required=False, label="Choix 5")

    class Meta:
        model = Question
        fields = ['question_text']

    def save(self, commit=True):
        question = super().save(commit=False)
        if commit:
            question.save()

            choices = [self.cleaned_data[f"choice{i}"] for i in range(1, 6) if self.cleaned_data[f"choice{i}"]]
            for choice_text in choices:
                Choice.objects.create(question=question, text=choice_text)

        return question