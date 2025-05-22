import re
from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import render, redirect,get_object_or_404
from .models import Employee


def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employees/employee_list.html', {'employees': employees})


def is_valid_name(text):
    return bool(re.match(r'^[A-Za-z ]+$', text))

def is_valid_email(email):
    return bool(re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email))

def employee_create(request):
    if request.method == "POST":
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        department = request.POST.get('department', '').strip()
        position = request.POST.get('position', '').strip()
        salary = request.POST.get('salary', '').strip()

        
        if not is_valid_name(name):
            messages.error(request, "Name must contain only letters and spaces.")
        elif not is_valid_email(email):
            messages.error(request, "Enter a valid email address.")
        elif not is_valid_name(department):
            messages.error(request, "Department must contain only letters and spaces.")
        elif not is_valid_name(position):
            messages.error(request, "Position must contain only letters and spaces.")
        elif not salary.replace('.', '', 1).isdigit() or float(salary) <= 0:
            messages.error(request, "Salary must be a positive number.")
        else:
            try:
                Employee.objects.create(
                    name=name,
                    email=email,
                    department=department,
                    position=position,
                    salary=salary
                )
                return redirect('employee_list')
            except IntegrityError:
                messages.error(request, "Employee with this email already exists.")

    return render(request, 'employees/employee_form.html')



def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)

    if request.method == "POST":
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        department = request.POST.get('department', '').strip()
        position = request.POST.get('position', '').strip()
        salary = request.POST.get('salary', '').strip()

        if not is_valid_name(name):
            messages.error(request, "Name must contain only letters and spaces.")
        elif not is_valid_email(email):
            messages.error(request, "Enter a valid email address.")
        elif not is_valid_name(department):
            messages.error(request, "Department must contain only letters and spaces.")
        elif not is_valid_name(position):
            messages.error(request, "Position must contain only letters and spaces.")
        elif not salary.replace('.', '', 1).isdigit() or float(salary) <= 0:
            messages.error(request, "Salary must be a positive number.")
        else:
            employee.name = name
            employee.email = email
            employee.department = department
            employee.position = position
            employee.salary = salary
            try:
                employee.save()
                return redirect('employee_list')
            except IntegrityError:
                messages.error(request, "Employee with this email already exists.")

    return render(request, 'employees/employee_form.html', {'employee': employee})




def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    
    if request.method == "POST":
        employee.delete()
        return redirect('employee_list')
    
    return render(request, 'employees/employee_confirm_delete.html', {'employee': employee})
