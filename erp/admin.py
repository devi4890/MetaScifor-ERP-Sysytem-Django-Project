from django.contrib import admin
from .models import Employee, InventoryItem, Sale, Expense,Payroll,Attendance


admin.site.register(Employee)
admin.site.register(InventoryItem)
admin.site.register(Sale)
admin.site.register(Expense)
admin.site.register(Payroll)
admin.site.register(Attendance)


