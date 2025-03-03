from datetime import timezone
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Employee(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    position=models.CharField(max_length=100)
    salary=models.DecimalField(max_digits=10,decimal_places=2)
    role = models.CharField(max_length=20, choices=[('Admin', 'Admin'), ('Employee', 'Employee')], default='Employee')


    def __str__(self):
        return self.user.username
    
class InventoryItem(models.Model):
    name=models.CharField(max_length=200)
    quantity=models.IntegerField()
    price_per_unit=models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return self.name
    
class Sale(models.Model):
    customer_name=models.CharField(max_length=200)
    product=models.ForeignKey(InventoryItem,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    total_price=models.DecimalField(max_digits=10,decimal_places=2)
    date=models.DateTimeField(auto_now_add=True)
CATEGORY_CHOICES = [
    ('Food', 'Food'),
    ('Transportation', 'Transportation'),
    ('Entertainment', 'Entertainment'),
    ('Utilities', 'Utilities'),
    ('Other', 'Other')
]
class Expense(models.Model):
    name = models.CharField(max_length=255, default="Unknown")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)  # ✅ Allows manual editing
    category = models.CharField(max_length=255,choices=CATEGORY_CHOICES, default='Other')  # Make sure this field is present

    def formatted_date(self):
        return timezone.localtime(self.date).strftime("%b. %d, %Y, %I:%M %p")

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return f"Message from {self.name}"

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])

    def __str__(self):
        return f"{self.employee} - {self.date}"

class Payroll(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = models.CharField(max_length=20)
    year = models.PositiveIntegerField()
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Payroll for {self.employee.user.username} - {self.payment_date}"

    def save(self, *args, **kwargs):
        # Calculate net salary as basic_salary + bonus - deductions
        self.net_salary = self.basic_salary + self.bonus - self.deductions
        super().save(*args, **kwargs)
