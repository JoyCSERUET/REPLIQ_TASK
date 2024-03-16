from django.shortcuts import render
from .models import companies, employee, device, device_log


# This is for a new company 
# and It should be controled by our_side
def new_company(request):
    
    # Say we get "Add_Company" in our POST request
    # from the front-end with Company name in 'C_NAME'
    if "Add_Company" in request.POST:
        Company_Name = request.POST['C_NAME']

        try:
            # tries to create an object ->
            companies.objects.create(
                c_name = Company_Name,
            )
            messages.success(request,"Account Created successfully.Please wait until it is authorized by the Department.")
            return redirect('HOME')

        except:
            # if the object creation is failed then ->
            messages.error(request,"There was an problem. Try Again Later.")
            return redirect('HOME')




# API to login
def login_page(request):
    # Say we get "admin"/"employee" in our POST request
    # from the front-end with email in 'U_Email' and password in 'U_PASS'
    u_mail = request.POST['U_EMAIL']
    u_pass = request.POST['U_PASS']

    try:
        # Authenticates user
        auth_users = authenticate(username = u_mail, password = u_pass)
    except:
        auth_users = None

    if "admin" in request.POST and auth_users is not None:
        # login to admin page
        login(u_mail, u_pass)
        return redirect('company_admin')

    elif "employee" in request.POST and auth_users is not None:
        #login to employee page
        login(u_mail, u_pass)
        return redirect('company_employee')

    elif auth_users is None:
        messages.error(request,"Wrong Email or Password.")
        return redirect('HOME')
        


# this API loads the company admin home page, with a string containing company name
# def c_admin(request):


# This API adds employee or devices to a company
def add_employee_or_device(request):
    # Say we get "employee" in our POST request
    # from the front-end, with employee details
    if "employee" in request.POST:
        try:
            dup_users = User.object.get(email = u_mail)
        except:
            dup_users = None
        
        # if user is not already in the table
        if dup_users is None:
            try:
                myuser = User.objects.create_user(u_mail, u_mail, u_pass)
                myuser.is_active = True
                myuser.save()

                employee.objects.create(
                    u_id        = u_mail,
                    company     = u_email,
                    designation = companies(company_Name)
                )

            except:
                messages.error(request,"There was a problem. Try Again Later.")
                return redirect('add_page')

        # if user is already in the table
        else:
            messages.error(request,"Employee already exists.")
            return redirect('add_page')


    # Say we get "device" in our POST request
    # from the front-end, with device details
    elif "device" in request.POST:
        try:
            dup_device = device.objects.filter(company = company_name, name = device_name)
        
        except:
            dup_device = None

        if dup_device in None:
            try:
                device.objects.create(
                    d_id      = device_id,
                    name      = device_name,
                    company   = companies(company_name),
                    in_use_of = "None", 
                )
            except:
                messages.error(request,"There was a problem. Try Again Later.")
                return redirect('add_page')
        
        else:
            messages.error(request,"Device already exists.")
            return redirect('add_page')
    
    # Just render the template
    # else:
    # return render(request, 'template.html', company_name)



# this API shows 
def assign_or_show_device(request):
    # Say we get "assign" in our POST request
    # from the front-end, with device and employee details
    if "assign" in request.POST:
        try:
            device_object = device.objects.get(d_id = Device_id)
            device_object.availability = False
            device_object.in_use_of = employee(Employee_id)

            device_object.save()

            device_log.objects.create(
                device_id = device(Device_id),
                used_by = employee(Employee_id),
                out_condition = Out_Condition,
            )
        except:
            messages.error(request,"There was a problem. Try Again Later.")
            return redirect('company_admin')
    
    # Say we get "show" in our POST request
    # from the front-end, with device details
    elif "show" in request.POST:
        try:
            log_object = device_log.objects.all().filter(device_id = Device_id)
        except:
            messages.error(request,"There was a problem. Try Again Later.")
            return redirect('company_admin')
    

    # else render a template with all available devices
    else:
        try:
            dev_object = device.objects.all().filter(availability = True)
            return redirect('add_show_page')
        except:
            messages.error(request,"There was a problem. Try Again Later.")
            return redirect('company_admin')



# Shows the devices used by one employee and a option for returning the devices
def return_device(request):
    # Say we get "Return" in POST request and
    # Devices is a list of device that the employee wants to return
    # Conditions is the current condition of the devices
    if "Return" in request.POST:
        try:
            # Iterate through selected devices in the front-end
            for i in len(Devices):
                dev_obj = device.object.get(d_id = Devices[i])
                dev_obj.availability = True
                dev_obj.in_use_of = "None"

                dev_obj.save()

                dev_logs = device_log.objects.all().filter(device_id = Devices[i], return_condition = "NA")

                # Iterate through the log objects, though dev_logs should contain only one item
                for dev_log in dev_logs:
                    dev_log.return_condition = Conditions[i]
                    dev_log.save()

        except:
            messages.error(request,"There was a problem. Try Again Later.")
            return redirect('employee_page')
    
    else:
        try:
            Devices = device_log.objects.all().filter(used_by = employee.Employee_id, return_condition = "NA")
            return render(request, "employee_device_page.html", Devices)
        except:
            messages.error(request,"There was a problem. Try Again Later.")
            return redirect('employee_page')





