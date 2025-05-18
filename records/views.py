from django.shortcuts import render,redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from .models import RecordsName,FieldNames,FieldValues,Field2Names
from decimal import Decimal, InvalidOperation
from django.http import HttpResponseNotAllowed

def error404(request,exception):
    return render(request,"errors/error404.html",status=404)

def privacy_policy(request):
    return render(request,"records/privacy-policy.html")
@never_cache
def main(request,id=None):
    if request.user.is_authenticated:
        record_name_instance=RecordsName.objects.filter(owner=request.user)
        #Checking if user just created an account.
        if record_name_instance:
            #Checking if user just logged in or clicked on the records name.
            if id:
                record_name_instance=RecordsName.objects.get(id=id,owner=request.user)
                field_values=FieldValues.objects.filter(records_name=record_name_instance,owner=request.user).order_by("id")
                #field_name cannot be processed directly in the DTL as it is not a list(its a query set representation), so we need to use for in DTL.
                field_names=FieldNames.objects.filter(records_name=record_name_instance,owner=request.user)
                records_name=RecordsName.objects.filter(owner=request.user)
                context={'records_name':records_name,'field_values':field_values,'field_names':field_names,'record_name_instance':record_name_instance}
                return render(request,'records/records.html',context)
            else :
                record_name_instance_first=RecordsName.objects.filter(owner=request.user).first()
                field_values=FieldValues.objects.filter(records_name=record_name_instance_first,owner=request.user).order_by("id")
                field_names=FieldNames.objects.filter(records_name=record_name_instance_first,owner=request.user)
                records_name=RecordsName.objects.filter(owner=request.user)
                context={'records_name':records_name,'field_values':field_values,'field_names':field_names}
                return render(request,'records/records.html',context)
        #If user just created an account , rendering the usual page.
        else:
            return render(request,'records/records.html')
    return render(request, 'main.html')

class AddTableView(LoginRequiredMixin,View):
    login_url=reverse_lazy("login")
    redirect_field_name = "next"
    def get_context(self,request):
        records_name=RecordsName.objects.filter(owner=request.user)
        return {
            'user_entry':request.POST,
            'records_name':records_name
        }
    def get(self,request):
        context=self.get_context(request)
        return render(request, 'records/add-table.html',context)
    def post(self,request):
        #context for storing users entry
        context=self.get_context(request)
        #storing user submitted data.
        table_name=request.POST['table_name']
        field1_name=request.POST['field1_name']
        field2_name=request.POST['field2_name']
        field3_name=request.POST['field3_name']
        add_first_data=request.POST.get('add_first_data')
        #Checking if user has selected for first data to be inserted during table formation.
        if add_first_data:
            #Setting Limit for the field 1
            field1_limit=999999
            field1_value=request.POST['field1_value']
            field2_value=request.POST['field2_value']
            field3_value=request.POST['field3_value']
            description=request.POST['description']
            #Checking for all the relevant details to be inserted in the database.
            if not field1_value or not field2_value or not field3_value or not description or not table_name or not field1_name or not field2_name or not field3_name:
                messages.error(request, "Please fill all the fields")
                return render(request,"records/add-table.html",context)
            #Check for field1_value is a number or not.
            if not field1_value.isdigit():
                messages.error(request, "Please enter a number for Field-1")
                return render(request,"records/add-table.html",context)
            #Checking for Field 1 limit.
            if int(field1_value)>field1_limit:
                messages.error(request,"Limit Exceeding!")
                return render(request,"records/add-table.html",context)
        #Checking in case of no new data has to be inserted.
        if not table_name or not field1_name or not field2_name or not field3_name:
            messages.error(request, "Please fill all fields")
            return render(request,"records/add-table.html",context)
        #Creating records-name instance and call onto it as it is required for new data to inserted in database.
        records_name_instance, _ = RecordsName.objects.get_or_create(name=table_name,owner=request.user)
        #Creating table.
        FieldNames.objects.create(field_1=field1_name,field_2=field2_name,field_3=field3_name,records_name=records_name_instance,owner=request.user)
        #Checking for first_data.
        if add_first_data:
            #Creating field2_name instance and call onto it as it is required for new data to inserted in database.
            field2_name_instance, _ = Field2Names.objects.get_or_create(name=field2_value,records_name=records_name_instance,owner=request.user)
            #Creating new data in the database of a table.
            FieldValues.objects.create(owner=request.user,field_1=field1_value,field_2=field2_name_instance,field_3=field3_value,description=description,records_name=records_name_instance)
        #Checking for the submit button request -  for save or adding new data.
        action=request.POST.get('action')
        #Returning same page with success message when another data button is added.
        messages.success(request, "Table added successfully.")
        return redirect("add-table" if action == 'another' else "records")

@method_decorator(never_cache, name='dispatch')
class AddTableDataView(LoginRequiredMixin,View):
    login_url=reverse_lazy("login")
    redirect_field_name = "next"
    def get_context(self,request,id):
        #Getting record names for sidebar
        records_name=RecordsName.objects.filter(owner=request.user)
        #Getting single record name for field2 names
        single_record_name=RecordsName.objects.get(id=id,owner=request.user)
        #Filtering field2 names
        field2_names=Field2Names.objects.filter(records_name=single_record_name,owner=request.user)
        field_names=FieldNames.objects.get(records_name=single_record_name,owner=request.user)
        return {
            'user_entry':request.POST,
            'Field2Names':field2_names,
            'records_name':records_name,
            'single_record_name':single_record_name,
            'field_names':field_names
        }
    def get(self,request,id):
        context=self.get_context(request,id)
        return render(request, 'records/add-table-data.html',context)
    def post(self,request,id):
        #Setting Limit for the field 1
        field1_limit=999999
        #call context method to get the context
        context=self.get_context(request,id)
        #Storing the values of the fields from the form.
        field1_value=request.POST['field1_value']
        field2_value=request.POST['field2_value']
        field3_value=request.POST['date']
        description=request.POST['description']
        owner=request.user
        #Checking if Others option is been selected.
        if field2_value=='Other':
            field2_value=request.POST['otherField2_value']
        #Checking for any empty field.
        if not field1_value or not field2_value or not field3_value or not description:
            messages.error(request, "Please fill all fields")
            return render(request, 'records/add-table-data.html',context)
        #Checking whether field 1 is a number or not.
        try:
            field1_decimal = Decimal(field1_value)
        except (InvalidOperation, TypeError):
            messages.error(request, "Please enter a valid number for Field-1")
            return render(request, 'records/add-table-data.html', context)
        #Checking for Field 1 limit.
        if field1_decimal>field1_limit:
            messages.error(request,"Limit Exceeding!")
            return render(request, 'records/add-table-data.html',context)
        #Creating instances.
        #You used Foreign key in the model for the below two fields that is why 
        #you need a model instance to save the data as it is different from raw data.
        #E.g. Model Instance = <Field2Names: S3> and raw data = 'S3' or 1 (string or integer).
        records_name_instance = RecordsName.objects.get(id=id)
        #Creating field2_name if not already present.
        field2_name_instance, _ = Field2Names.objects.get_or_create(name=field2_value,records_name=records_name_instance,owner=request.user)
        #Creating the object in the required field.
        FieldValues.objects.create(owner=owner,field_1=field1_decimal,field_2=field2_name_instance,description=description,field_3=field3_value,records_name=records_name_instance)
        action = request.POST.get('action')
        messages.success(request, "Data added successfully in "+str(records_name_instance)+".")
        #Will redirect to the same page or to the data of current record.
        return redirect("add-table-data", id=id) if action == 'another' else redirect("records",id=id)

@method_decorator(never_cache, name='dispatch')
class EditTableDataView(LoginRequiredMixin,View):
    login_url=reverse_lazy("login")
    redirect_field_name = "next"
    def get_context(self,request,id):
        #Getting record names for sidebar
        records_name=RecordsName.objects.filter(owner=request.user)
        #Getting single record name for field2 names
        single_record_name=FieldValues.objects.get(id=id,owner=request.user).records_name
        #Filtering field2 names
        field2_names=Field2Names.objects.filter(records_name=single_record_name,owner=request.user)
        field_names=FieldNames.objects.get(records_name=single_record_name,owner=request.user)
        #Getting the field values for user requested id.
        field_value_id=FieldValues.objects.get(id=id,owner=request.user)
        return {
            'user_entry':request.POST,
            'Field2Names':field2_names,
            'records_name':records_name,
            'single_record_name':single_record_name,
            'field_names':field_names,
            'field_value_id':field_value_id
        }
    def get(self,request,id):
        context=self.get_context(request,id)
        return render(request, 'records/edit-table-data.html',context)
    def post(self,request,id):
        #Setting Limit for the field 1
        field1_limit=999999
        #call context method to get the context
        context=self.get_context(request,id)
        #Getting the field values for user requested id.
        field_value_id = context['field_value_id']
        field1_value=request.POST['field1_value']
        field2_value=request.POST['field2_value']
        field3_value=request.POST['date']
        description=request.POST['description']
        owner=request.user
        #Checking if Others option is been selected.
        if field2_value=='Other':
            field2_value=request.POST['otherField2_value']
        #Checking for any empty field.
        if not field1_value or not field2_value or not field3_value or not description:
            messages.error(request, "Please fill all fields")
            return render(request, 'records/edit-table-data.html',context)
        #Checking whether field 1 is a number or not.
        try:
            #Converting it to decimal.
            field1_decimal = Decimal(field1_value)
        except (InvalidOperation, TypeError):
            messages.error(request, "Please enter a valid number for Field-1")
            return render(request, 'records/edit-table-data.html', context)
        #Checking for Field 1 limit.
        if field1_decimal>field1_limit:
            messages.error(request,"Limit Exceeding!")
            return render(request, 'records/edit-table-data.html',context)
        records_name_instance = field_value_id.records_name
        #Creating field2_name if not already present.
        field2_name_instance, _ = Field2Names.objects.get_or_create(name=field2_value,records_name=records_name_instance,owner=request.user)
        #field_value_id is a model instance and not a dictionary hence field_value_id['key'] is not a valid syntax.
        #Replacing the previous data with the new one.
        field_value_id.owner = owner
        field_value_id.field_1 = field1_decimal
        field_value_id.field_2 = field2_name_instance
        field_value_id.description = description
        field_value_id.field_3 = field3_value
        field_value_id.records_name = records_name_instance
        #Saving the changes.
        field_value_id.save()
        #Returning the message.
        messages.success(request, "Data updated successfully in "+str(records_name_instance)+".")
        #Will redirect to the data of current record.
        return redirect("records",id=records_name_instance.id)

@never_cache
def DeleteTableDataView(request,id):
    if request.method == "POST":
        #Fetching the field_value data
        field_value_id=FieldValues.objects.get(id=id,owner=request.user)
        #Fetching the record_name_instance
        records_name_instance = field_value_id.records_name
        #Deleting the Field_value data
        field_value_id.delete()
        messages.success(request, "Data has been deleted from "+str(records_name_instance)+".")
        return redirect('records',id=records_name_instance.id)
    else:
        #Returning error message if another other Method apart from POST is used.
        messages.error(request,"Invalid Operation.")
        return redirect('records')


#Edit Record Name
#Delete complete record
#Delete Field2 Value from select options only
#Export Pdf and Excel