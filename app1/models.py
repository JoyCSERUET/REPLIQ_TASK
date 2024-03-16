from django.db import models


# List of companies
class companies(models.Model):
    c_name = models.CharField(max_length = 50, primary_key = True)


# Employee Table
class employee(models.Model):
    u_id = models.EmailField(primary_key = True)
    company = models.ForeignKey(companies, on_delete = models.CASCADE)
    designation = models.CharField(max_length = 50)




# Device is table for details of devices
class device(models.Model):
    d_id = models.IntegerField(primary_key = True)
    name = models.CharField(max_length = 25)         # PC1, PC2, Laptop1 & so on...
    company = models.ForeignKey(companies, on_delete = models.PROTECT)
    availability = models.BooleanField(default = True)
    in_use_of = models.CharField(max_length = 50)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ['name', 'company'], name = 'company_wise_device'
            )
        ]



# Device Log
class device_log(models.Model):
    device_id = models.ForeignKey(device, on_delete = models.CASCADE)
    used_by = models.ForeignKey(employee, on_delete = models.CASCADE)
    out_time = models.DateTimeField(auto_now_add = True)
    out_condition = models.CharField(max_length = 50, default = "Good")
    return_time = models.DateTimeField(auto_now = True)
    return_condition = models.CharField(max_length = 50, default = "NA")
