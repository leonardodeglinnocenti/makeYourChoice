from django import forms


class AnswerForm(forms.Form):
    def __init__(self, *args, **kwargs):
        choices = kwargs.pop("choices")
        # Choices must be a list of Choice objects separated by question
        super(AnswerForm, self).__init__(*args, **kwargs)
        for choice in choices:
            self.fields[choice.question.text] = forms.ModelChoiceField(queryset=choice.question.choice_set.all(),
                                                                       widget=forms.RadioSelect,
                                                                       empty_label=None)