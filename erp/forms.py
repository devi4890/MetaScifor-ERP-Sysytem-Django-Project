from django import forms
from.models import Employee,InventoryItem,Sale,Expense,Payroll
from django.contrib.auth.models import User

from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['user', 'position', 'salary']

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        self.fields['user'].widget.attrs.update({
            'class': 'form-control',
            'style': 'background-color: #f8f9fa; color: #343a40; margin-bottom: 15px;',
            'readonly': True  # Make it non-editable
        })
        self.fields['position'].widget.attrs.update({
            'class': 'form-control',
            'style': 'background-color: #e3f2fd; color: #0d47a1; margin-bottom: 15px;',
            'placeholder': 'Enter Position'
        })
        self.fields['salary'].widget.attrs.update({
            'class': 'form-control',
            'style': 'background-color: #f1f8e9; color: #1b5e20; margin-bottom: 15px;',
            'placeholder': 'Enter Salary'
        })


class InventoryForm(forms.ModelForm):
    class Meta:
        model=InventoryItem
        fields = ['name', 'quantity', 'price_per_unit']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter item name'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter quantity'}),
            'price_per_unit': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price per unit'}),
        }

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['customer_name', 'product', 'quantity']

    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get('quantity')
        product = cleaned_data.get('product')

        if quantity and product:
            # Calculate total price dynamically
            price_per_unit = product.price_per_unit
            cleaned_data['total_price'] = quantity * price_per_unit

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.total_price = instance.quantity * instance.product.price_per_unit
        if commit:
            instance.save()
        return instance
CATEGORY_CHOICES = [
        ('Food', 'Food'),
        ('Transportation', 'Transportation'),
        ('Entertainment', 'Entertainment'),
        ('Utilities', 'Utilities'),
        ('Other', 'Other')
    ]
    
class ExpenseForm(forms.ModelForm):
    

    category = forms.ChoiceField(choices=CATEGORY_CHOICES)
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))  # Adds a date picker

    class Meta:
        model = Expense
        fields = ['name', 'amount', 'date','category']  # ✅ Make sure 'date' is included
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message', 'rows': 4}))

class PayrollForm(forms.ModelForm):
    class Meta:
        model = Payroll
        fields = ['employee', 'month', 'year', 'basic_salary', 'bonus', 'deductions', 'net_salary', 'payment_date']