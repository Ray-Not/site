from django import forms

from .models import CustomOrder, Order, Review, GetDiscount


class GetDiscountForm(forms.ModelForm):
    class Meta:
        model = GetDiscount
        fields = ['phone',]
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }


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


class CustomOrderForm(forms.ModelForm):
    class Meta:
        model = CustomOrder
        fields = '__all__'
        widgets = {
            'type_contruction': forms.Select(attrs={'class': 'form-control'}),
            'double_glazing': forms.Select(attrs={'class': 'form-control'}),
            'out_cover': forms.Select(attrs={'class': 'form-control'}),
            'in_cover': forms.Select(attrs={'class': 'form-control'}),
            'platbans': forms.Select(attrs={'class': 'form-control'}),
            'top_castle': forms.Select(attrs={'class': 'form-control'}),
            'bot_castle': forms.Select(attrs={'class': 'form-control'}),
            'cylinder': forms.Select(attrs={'class': 'form-control'}),
            'hinge': forms.Select(attrs={'class': 'form-control'}),
            'blockers': forms.Select(attrs={'class': 'form-control'}),
            'insulation': forms.Select(attrs={'class': 'form-control'}),
            'dismantling': forms.Select(attrs={'class': 'form-control'}),
            'night_lock': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
            'peephole': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
            'door_closer_100kg': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
            'door_closer_120kg': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
            'handle_scarf': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
        }
