from django.urls import path
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth import views as auth_views


from . import views  

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"), 
    # path('password-reset/', PasswordResetView.as_view(template_name="reset_password.html"), name="password_reset"),
    path('password-reset/', PasswordResetView.as_view(
    template_name="reset_password.html",
    success_url='/password-reset-done/'), name="password_reset"),

    path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"), name="password_reset_confirm"),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"), name="password_reset_complete"),
    path('password-reset-done/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"), name="password_reset_done"),

    path("logout/", views.logout_view, name="logout"),  
    path("dashboard/", views.dashboard, name="dashboard"),
    path("employees/", views.manage_employees, name="manage_employees"),
    path('employees/add/', views.create_employee, name='create_employee'),
    path('employees/edit/<int:pk>/', views.update_employee, name='update_employee'),
    path('employees/delete/<int:pk>/', views.delete_employee, name='delete_employee'),
    path("inventory/", views.manage_inventory, name="manage_inventory"),
    path('inventory/add/', views.add_inventory, name="add_inventory"),
    path('inventory/update/<int:pk>/', views.update_inventory, name="update_inventory"),
    path('inventory/delete/<int:pk>/', views.delete_inventory, name="delete_inventory"),
    path("sale/", views.manage_sales, name="manage_sales"), 
    path('sale/add/', views.add_sale, name='add_sale'),
    path('sale/update/<int:pk>/', views.update_sale, name='update_sale'),
    path('sale/delete/<int:pk>/', views.delete_sale, name='delete_sale'),
    path("expenses/", views.manage_expenses, name="manage_expenses"),
    path('expense/add/', views.add_expense, name='add_expense'),
    path('expense/edit/<int:pk>/', views.update_expense, name='update_expense'),
    path('expense/delete/<int:pk>/', views.delete_expense, name='delete_expense'),
    path('contact-us/', views.contact_us, name='contact_us'),
    path('payroll/', views.manage_payroll, name='manage_payroll'),
    path('attendance/', views.manage_attendance, name='manage_attendance'),
    path('employee_dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('payroll/update/<int:payroll_id>/', views.update_payroll, name='update_payroll'),
    path('payroll/delete/<int:payroll_id>/', views.delete_payroll, name='delete_payroll'),
]
