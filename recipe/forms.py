from django import forms
from django.core.exceptions import ValidationError

from .models import Recipe, Ingredient


class RecipeForm(forms.ModelForm):
    time = forms.IntegerField(
        min_value=1,
        required=True,
    )

    class Meta:
        model = Recipe
        fields = (
            'title',
            'time',
            'text',
            'image',
            'tags',
        )

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('tags'):
            raise ValidationError(
                'Убедитесь, что установили ТЭГ!'
            )

        ing_added, quantity = False, True
        print(self.data.values())

        for key in self.data.keys():
            if key.startswith('nameIngredient_'):
                print(self.data[key])
                ing_added = True

            if key.startswith('valueIngredient_'):
                print(self.data[key])
                if int(self.data[key]) < 1:
                    quantity = False

        if not ing_added:
            raise ValidationError(
                'Добавьте хотя бы один ингредиент!'
            )

        if not quantity:
            raise ValidationError(
                'Убедитесь, что это значение ингредиента больше либо равно 1 !'
            )
