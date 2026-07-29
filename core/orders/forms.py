from django import forms


class CheckoutForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=20)
    address = forms.CharField()
    description = forms.CharField(required=False)


class CouponApplyForm(forms.Form):
    code = forms.CharField(
        max_length=50,
    )
