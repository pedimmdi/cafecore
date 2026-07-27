from django import forms


class ReviewForm(forms.Form):

    rating = forms.IntegerField(
        min_value=1,
        max_value=5,
    )

    comment = forms.CharField()

    def clean_rating(self):

        rating = self.cleaned_data["rating"]

        if rating not in range(1, 6):

            raise forms.ValidationError(
                "Rating must be between 1 and 5."
            )

        return rating
