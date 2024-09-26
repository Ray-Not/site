from django import forms

from .models import Order, Review


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'phone', 'call_time', 'address', 'message']
        widgets = {
            'call_time': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'}
            ),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(
                attrs={'class': 'form-control', 'rows': 3}
            ),
            'message': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3}
            ),
        }


class ReviewFirm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'name', 'message', 'rating']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(
                attrs={'class': 'form-control', 'rows': 3}
            ),
            'rating': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3}
            )
        }
