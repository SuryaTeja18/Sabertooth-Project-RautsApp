from django.db import models
from safedelete.models import SafeDeleteModel
from safedelete.models import HARD_DELETE_NOCASCADE

# Create your models here.

class User(models.Model):
    _safedelete_policy = HARD_DELETE_NOCASCADE
    username = models.CharField(max_length=128)
    email = models.EmailField(max_length= 128)
    phone = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    role_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank= True)
    #deleted_at = models.DateTimeField()

class Vehicle(models.Model):
    _safedelete_policy = HARD_DELETE_NOCASCADE
    vehicle_name = models.CharField(max_length=128)
    number_plate = models.CharField(max_length=128)
    rc_number = models.CharField(max_length=128)
    vehicle_insurance = models.CharField(max_length=128)
    manufacture_date = models.DateField()
    puc = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    #deleted_at = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete= models.CASCADE)

class VehicleDocument(models.Model):
    vehicle_id = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=128)
    path = models.CharField(max_length=128)

class User_Detail(models.Model):
    _safedelete_policy = HARD_DELETE_NOCASCADE
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    adhaar_card_number = models.CharField(max_length=16)
    license = models.CharField(max_length=20)
    name = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    #deleted_at = models.DateTimeField()
    #created_by = models.ForeignKey(User, on_delete=models.CASCADE)

class Distributor(models.Model):
    _safedelete_policy = HARD_DELETE_NOCASCADE
    organization_name = models.CharField(max_length=128)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    #deleted_at = models.DateTimeField()
    #created_by = models.ForeignKey(User, on_delete=models.CASCADE)

class DistributorInsurance(models.Model):
    _safedelete_policy = HARD_DELETE_NOCASCADE
    distributor_id = models.ForeignKey(Distributor, on_delete=models.CASCADE)
    insurance_master_id = models.CharField(max_length=128)
    expiry_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    #deleted_at = models.DateTimeField()
    #created_by = models.ForeignKey(User, on_delete=models.CASCADE)

class User_Leave(models.Model):
    _safedelete_policy = HARD_DELETE_NOCASCADE
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    leave_date = models.DateField()
    number_of_days = models.IntegerField()
    reason_type = models.CharField(max_length=128)
    description = models.CharField(max_length=128)
    is_approved = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    #deleted_at = models.DateTimeField()
    #created_by = models.ForeignKey(User, on_delete=models.CASCADE)

class User_Expense(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.CharField(max_length=128)

class Expense_Media(models.Model):
    expense_id = models.ForeignKey(User_Expense, on_delete=models.CASCADE)
    photo = models.ImageField()

class Banker_Detail(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ImageField()

class Delivery_Boy_Data(models.Model):
    _safedelete_policy = HARD_DELETE_NOCASCADE
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    is_vehicle_insured = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    #deleted_at = models.DateTimeField()
    #created_by = models.ForeignKey(User, on_delete=models.CASCADE)

class Delivery_Boy_Vehicle_Data(models.Model):
    _safedelete_policy = HARD_DELETE_NOCASCADE
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle_id = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    #deleted_at = models.DateTimeField()
    #created_by = models.ForeignKey(User, on_delete=models.CASCADE)


class Cylinder_Master(models.Model):
    name = models.CharField(max_length=128)
    sub_name = models.CharField(max_length=128)
    weight = models.IntegerField()
    amount = models.IntegerField()

class Insurance_Master(models.Model):
    name = models.CharField(max_length=128)
    is_explosive = models.BooleanField()
    is_hazardous = models.BooleanField()

class Business_Master_Type(models.Model):
    type = models.CharField(max_length=128)
    sub_name = models.CharField(max_length=128)

class Gas_Distributor_Material(models.Model):
    _safedelete_policy = HARD_DELETE_NOCASCADE
    distributor_id = models.ForeignKey(Distributor, on_delete=models.CASCADE)
    business_type = models.CharField(max_length=128) #choice to be added
    total_cylinders = models.IntegerField()
    total_filler_cylinders = models.IntegerField()
    total_empty_cylinders = models.IntegerField()
    total_godown_filled_cylinders = models.IntegerField()
    total_godown_empty_cylinders =models.IntegerField()
    total_vehicle_filled_cylinders = models.IntegerField()
    total_vehicle_empty_cylinders = models.IntegerField()
    cylinder_master_id = models.ForeignKey(Cylinder_Master, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    #deleted_at = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

#customer_id
class Sales_Gas_Data(models.Model):
    _safedelete_policy = HARD_DELETE_NOCASCADE
    delivery_boy = models.ForeignKey(Delivery_Boy_Data, on_delete=models.CASCADE)
    cylinder_master_id = models.ForeignKey(Cylinder_Master, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    amount = models.IntegerField()
    is_empty = models.BooleanField()
    is_delivered = models.BooleanField()
    customer_id = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_date = models.DateField()
    delivery_time = models.TimeField()
    business_type = models.CharField(max_length=128) #choice to be added
    delivery_type = models.IntegerField() #choice to be added (0,1,2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    #deleted_at = models.DateTimeField()

class New_or_Emergency_Connection(models.Model):
    _safedelete_policy = HARD_DELETE_NOCASCADE
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    gas_amount=models.IntegerField()
    gas_tank_amount = models.IntegerField()
    is_rental = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    #deleted_at = models.DateTimeField()
    #created_by = models.ForeignKey(User, on_delete=models.CASCADE)
