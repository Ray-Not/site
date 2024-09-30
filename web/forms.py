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


class ReviewForm(forms.ModelForm):
    order_number = forms.CharField(
        max_length=255,
        label="Номер заказа",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Номер заказа'}
            )
        )

    def clean_order_number(self):
        order_number = self.cleaned_data.get('order_number')
        if not Order.objects.filter(order_number=order_number).exists():
            raise forms.ValidationError("Заказ с таким номером не существует.")
        return order_number

    class Meta:
        model = Review
        fields = ['name', 'message', 'rating', 'order_number']
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Ваше имя'}
            ),
            'message': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'Ваш отзыв'
                }
            ),
            'rating': forms.RadioSelect(attrs={'class': 'form-check-input'})
        }
