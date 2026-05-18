from django import forms
from django.contrib.auth.models import User
from .models import (
    Category,
    Supplier,
    InventoryItem,
    StockTransaction
)

class LoginForm(forms.Form):

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username',
                'class': 'form-control'
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password',
                'class': 'form-control'
            }
        )
    )

class RegisterForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password',
                'class': 'form-control'
            }
        )
    )

    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Confirm Password',
                'class': 'form-control'
            }
        )
    )

    class Meta:
        model = User

        fields = [
            'username',
            'email',
            'first_name',
            'last_name'
        ]

        widgets = {

            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Username'
                }
            ),

            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Email'
                }
            ),

            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'First Name'
                }
            ),

            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Last Name'
                }
            ),
        }
    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            raise forms.ValidationError(
                "Passwords do not match."
            )

        return cleaned_data


class CategoryForm(forms.ModelForm):

    class Meta:

        model = Category

        fields = [
            'name',
            'image',
            'description'
        ]

        widgets = {

            'name': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }

class SupplierForm(forms.ModelForm):

    class Meta:

        model = Supplier

        fields = [
            'name',
            'image',
            'contact_person',
            'phone',
            'email',
            'address'
        ]

        widgets = {

            'name': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),

            'contact_person': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'phone': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control'
            }),

            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }

class InventoryItemForm(forms.ModelForm):

    class Meta:

        model = InventoryItem

        fields = [
            'name',
            'image',
            'sku',
            'category',
            'supplier',
            'quantity',
            'unit',
            'reorder_level',
            'cost_price',
            'description'
        ]

        widgets = {

            'name': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),

            'sku': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'category': forms.Select(attrs={
                'class': 'form-select'
            }),

            'supplier': forms.Select(attrs={
                'class': 'form-select'
            }),

            'quantity': forms.NumberInput(attrs={
                'class': 'form-control'
            }),

            'unit': forms.Select(attrs={
                'class': 'form-select'
            }),

            'reorder_level': forms.NumberInput(attrs={
                'class': 'form-control'
            }),

            'cost_price': forms.NumberInput(attrs={
                'class': 'form-control'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }

class StockTransactionForm(forms.ModelForm):

    class Meta:

        model = StockTransaction

        fields = [
            'transaction_type',
            'quantity',
            'notes'
        ]

        widgets = {

            'transaction_type': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'quantity': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'step': '0.01',
                    'min': '0.01'
                }
            ),

            'notes': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'Optional notes...'
                }
            ),
        }