from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from .forms import PayrollForm
from django.conf import settings
from .models import Employee, InventoryItem, Sale, Expense,Contact,Payroll,Attendance
from django.contrib.auth.models import User
from.forms import EmployeeForm,InventoryForm,SaleForm,ExpenseForm,ContactForm,AttendanceForm


from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from erp.models import Employee  # Ensure Employee model is imported

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        role = request.POST.get("role", "Employee")  # Default to Employee if not provided

        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect("register")

        # Create User
        user = User.objects.create_user(username=username, email=email, password=password1)

        # Set staff permissions for Admin
        if role == "Admin":
            user.is_staff = True  # ✅ Admin users can access Django admin panel
            user.is_superuser = True  # ✅ Superuser privileges
        else:
            user.is_staff = False  # Employees cannot access admin panel

        user.save()

        # Create Employee instance
        salary = 50000  # Default salary, adjust as needed
        Employee.objects.create(user=user, position="Staff", salary=salary, role=role)

        messages.success(request, "Registration successful! Please log in.")
        login(request, user)
        return redirect("login")

    return render(request, "register.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            # Get employee role
            try:
                employee = Employee.objects.get(user=user)
                if employee.role == "Admin":
                    return redirect("dashboard")  # Redirect to admin dashboard
                elif employee.role == "Employee":
                    return redirect("employee_dashboard")  # Redirect to employee dashboard
            except Employee.DoesNotExist:
                messages.error(request, "No role assigned. Contact Admin.")
                return redirect("login")

        messages.error(request, "Invalid username or password.")
        return redirect("login")

    return render(request, "login.html")


# ✅ FIX: Rename logout function
def logout_view(request):
    storage = messages.get_messages(request)
    storage.used = True  # ✅ Clear old messages
    
    logout(request)  # Clears session
    messages.success(request, "Logged out successfully!")
    
    return redirect('login')  # Redirect to login page


# ✅ Apply `@login_required` to restrict access to these views
@login_required
@login_required
def dashboard(request):
    employees = Employee.objects.count()
    total_sales = Sale.objects.count()
    total_expenses = Expense.objects.count()
    return render(request, 'dashboard.html', {'employees': employees, 'sales': total_sales, 'expenses': total_expenses})
# views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Employee, Payroll, Attendance  # Assuming these models exist

@login_required
def employee_dashboard(request):
    # Get the employee instance of the logged-in user
    employee = Employee.objects.get(user=request.user)

    # You can add payroll and attendance data if you need
    payroll = Payroll.objects.filter(employee=employee)
    attendance = Attendance.objects.filter(employee=employee)

    context = {
        'employee': employee,
        'payroll': payroll,
        'attendance': attendance,
    }
    return render(request, 'employee_dashboard.html', context)

@login_required
def manage_employees(request):
    employees = Employee.objects.all()
    
    return render(request, 'employees.html', {'employees': employees})

@login_required
def create_employee(request):
    
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Employee created successfully!")
            return redirect("manage_employees")
    else:
        form = EmployeeForm()
    return render(request, "employee_form.html", {"form": form, "title": "Add New Employee"})

@login_required
def update_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    
    if request.method == "POST":
        # Copy POST data into a mutable dictionary
        data = request.POST.copy()
        # Inject the current employee's user ID into the data
        data['user'] = employee.user.pk
        
        form = EmployeeForm(data, instance=employee)
        if form.is_valid():
            updated_employee = form.save(commit=False)
            # Reassign the original user to be safe
            updated_employee.user = employee.user
            updated_employee.save()
            messages.success(request, "Employee updated successfully!")
            return redirect("manage_employees")
        else:
            # Log or display form errors for debugging
            messages.error(request, f"Form errors: {form.errors}")
    else:
        form = EmployeeForm(instance=employee)
        # Disable the user field so it's read-only on GET
        form.fields['user'].disabled = True

    return render(request, "update.html", {"form": form, "title": "Edit Employee"})



@login_required
def delete_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == "POST":
        employee.delete()
        messages.success(request, "Employee deleted successfully!")
        return redirect("manage_employees")
    return render(request, "employee_confirm_delete.html", {"employee": employee})


@login_required
def manage_inventory(request):
    items = InventoryItem.objects.all()
    return render(request, 'inventory.html', {'items': items})

@login_required
def add_inventory(request):
    if request.method == "POST":
        form = InventoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Item added successfully!")
            return redirect("manage_inventory")
    else:
        form = InventoryForm()

    return render(request, 'inventory_form.html', {'form': form, 'title': 'Add Inventory Item'})

@login_required
def update_inventory(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)
    if request.method == "POST":
        form = InventoryForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Item updated successfully!")
            return redirect("manage_inventory")
    else:
        form = InventoryForm(instance=item)

    return render(request, 'inventory_form.html', {'form': form, 'title': 'Edit Inventory Item'})

@login_required
def delete_inventory(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)
    if request.method == "POST":
        item.delete()
        messages.success(request, "Item deleted successfully!")
        return redirect("manage_inventory")

    return render(request, 'confirm_delete.html', {'object': item, 'title': 'Delete Inventory Item'})

@login_required
def manage_sales(request):
    sales = Sale.objects.all()
    return render(request, 'sales.html', {'sales': sales})
@login_required
def add_sale(request):
    if request.method == "POST":
        customer_name = request.POST.get("customer_name")
        product_id = request.POST.get("product")  # The product ID will be sent as part of the form
        quantity = request.POST.get("quantity")  # Get quantity as string

        # Check if quantity is provided and is a valid integer
        if quantity is None or quantity == "":
            messages.error(request, "Quantity is required.")
            return redirect('add_sale')  # Redirect back to the add sale page

        try:
            quantity = int(quantity)  # Convert quantity to an integer
        except ValueError:
            messages.error(request, "Quantity must be a valid number.")
            return redirect('add_sale')  # Redirect back to the add sale page

        # Get the product object from the product ID
        try:
            product = InventoryItem.objects.get(id=product_id)
        except InventoryItem.DoesNotExist:
            messages.error(request, "Selected product does not exist.")
            return redirect('add_sale')  # Redirect back to the add sale page

        # Calculate the total price
        total_price = product.price_per_unit * quantity

        # Create the sale object
        sale = Sale(
            customer_name=customer_name,
            product=product,
            quantity=quantity,
            total_price=total_price  # Save the calculated total_price
        )

        sale.save()
        messages.success(request, "Sale added successfully!")
        return redirect('manage_sales')  # Redirect to the sales management page

    # If it's a GET request, just display the form
    products = InventoryItem.objects.all()  # Get all available products
    return render(request, 'add_sale.html', {'products': products})
@login_required
def update_sale(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    
    if request.method == "POST":
        form = SaleForm(request.POST, instance=sale)
        if form.is_valid():
            form.save()  # This will save the updated sale, including recalculating the total price
            messages.success(request, "Sale updated successfully!")
            return redirect("manage_sales")
    else:
        form = SaleForm(instance=sale)

    return render(request, 'update_sale.html', {'form': form, 'title': "Edit Sale"})
@login_required
def delete_sale(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    
    if request.method == "POST":
        sale.delete()  # This deletes the sale from the database
        messages.success(request, "Sale deleted successfully!")
        return redirect("manage_sales")  # Redirect back to the sales list page
    
    return render(request, 'confirm_delete_sale.html', {'sale': sale})

@login_required
def manage_expenses(request):
    expenses = Expense.objects.all()
    return render(request, 'expenses.html', {'expenses': expenses})
@login_required
def add_expense(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Expense added successfully!")
            return redirect("manage_expenses")
    else:
        form = ExpenseForm()
    return render(request, "add_expense.html", {"form": form})


# Update Expense View
@login_required
def update_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, "Expense updated successfully!")
            return redirect("manage_expenses")
    else:
        form = ExpenseForm(instance=expense)
    return render(request, "update_expense.html", {"form": form, "title": "Edit Expense"})

# Delete Expense View
@login_required
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == "POST":
        expense.delete()
        messages.success(request, "Expense deleted successfully!")
        return redirect("manage_expenses")
    return render(request, "confirm_delete_expense.html", {"expense": expense})

def contact_us(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Show success message
            messages.success(request, "We will contact you soon! Thank you for your message.")
            return redirect("contact_us")  # To avoid form resubmission on refresh
    else:
        form = ContactForm()

    return render(request, "contact_us.html", {"form": form})

def manage_payroll(request):
    payrolls = Payroll.objects.all()  # Get all payroll records
    print(payrolls)  # Debugging step to check data

    return render(request, 'payroll.html', {'payrolls': payrolls})


def manage_attendance(request):
    attendances = Attendance.objects.all()
    return render(request, 'attendance.html', {'attendances': attendances})
# 
@login_required
def update_payroll(request, payroll_id):
    payroll = get_object_or_404(Payroll, id=payroll_id)
    
    # Check if the user is an admin (staff member)
    if not request.user.is_staff:  # Or is_superuser for full admin access
        return redirect('payroll')  # Redirect or handle error if not authorized
    
    if request.method == 'POST':
        form = PayrollForm(request.POST, instance=payroll)
        if form.is_valid():
            form.save()
            return redirect('manage_payroll')  # Redirect to payroll list after update
    else:
        form = PayrollForm(instance=payroll)

    return render(request, 'update_payroll.html', {'form': form})

@login_required
def delete_payroll(request, payroll_id):
    payroll = get_object_or_404(Payroll, id=payroll_id)
    
    # Check if the user is an admin (staff member)
    if not request.user.is_staff:  # Or is_superuser for full admin access
        return redirect('manage_payroll')  # Redirect or handle error if not authorized
    
    # Proceed to delete the payroll entry if the user is authorized
    payroll.delete()
    return redirect('manage_payroll')  # Redirect to the payroll list page after deletion

@login_required
def update_attendance(request, attendance_id):
    attendance = get_object_or_404(Attendance, id=attendance_id)  # Get the attendance instance

    if request.method == "POST":
        form = AttendanceForm(request.POST, instance=attendance)  # Bind the form with POST data and the attendance instance
        if form.is_valid():
            form.save()  # Save the updated attendance
            return redirect("manage_attendance")  # Redirect to the manage attendance page after updating
        else:
            print(form.errors)  # Print errors if the form is invalid
    else:
        form = AttendanceForm(instance=attendance)  # Prepopulate the form with existing data

    return render(request, "update_attendance.html", {"form": form})

def delete_attendance(request, attendance_id):
    attendance = get_object_or_404(Attendance, id=attendance_id)
    attendance.delete()
    return redirect('manage_attendance')