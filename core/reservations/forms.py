from django import forms


class ReservationForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=20)
    reservation_date = forms.DateField()
    reservation_time = forms.TimeField()
    number_of_guests = forms.IntegerField(min_value=1)
    description = forms.CharField(required=False)

    def clean_number_of_guests(self):
        number_of_guests = self.cleaned_data["number_of_guests"]
        if number_of_guests > 20:
            raise forms.ValidationError("حداکثر تعداد نفرات ۲۰ نفر است.")
        return number_of_guests
