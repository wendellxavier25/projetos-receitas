from collections import defaultdict
from django import forms
from recipes.models import Recipe
from utils.django_forms import add_attr
from django.core.exceptions import ValidationError
from utils.strings import is_positive_number

class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._my_errors = defaultdict(list)
        self._my_errors

        add_attr(self.fields.get('preparation_steps'), 'class', 'span-2')
        add_attr(self.fields.get('cover'), 'class', 'span-2')

    class Meta:
        model = Recipe
        fields = 'title', 'description', 'preparation_time', \
              'preparation_time_unit', 'servings', 'servings_unit', \
              'preparation_steps',  'cover'
        widgets = {'cover': forms.FileInput(attrs={ 'class': 'span-2'}), 'servings_unit': forms.Select(
            choices=(
                    ('Poeções', 'Porções'),
                    ('Pedaços', 'Pedaços'),
                    ('Pessoa', 'Pessoa'),
                    ),
                ),
                'preparation_time_unit': forms.Select(
                choices=(
                    ('Minutos', 'Minutos'),
                    ('Horas', 'Horas'),
                    ('Dia', 'Dia'),
                    ),
                ),
            }
              
    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        cleanded_data = self.cleaned_data
        title = cleanded_data.get('title')
        description = cleanded_data.get('description')


        if len(title) < 4:
            self._my_errors['title'].append('Title must have at least 4 chars.')

        if len(description) < 4:
            self._my_errors['description'].append('description must have at least 5 chars.')
        


        if self._my_errors:
            raise ValidationError(self._my_errors)
        return super_clean
    
    def clean_preparation_time(self):
        field_name = 'preparation_time'
        field_value = self.cleaned_data.get(field_name)

        if not is_positive_number(field_value):
            self._my_errors[field_name].append('Must be a positive number')
        return field_value
    

    def clean_servings(self):
        field_name = 'servings'
        field_value = self.cleaned_data.get(field_name)

        if not is_positive_number(field_value):
            self._my_errors[field_name].append('Must be a positive number')
        return field_value