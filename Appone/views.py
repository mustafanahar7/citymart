from django.shortcuts import render , redirect
from django.http import JsonResponse , HttpResponse
import os
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login , logout
from sqlalchemy import create_engine
from django.db.models import Count , Sum
from django.core.files.storage import FileSystemStorage
from .models import CustomUser , ContactUsForm , ProductInventory, WebsiteOrder , WebsiteOrderItems

# engine = create_engine('postgresql+psycopg2://postgres:mustafabohra@localhost:5432/citymart')
engine = create_engine('postgresql+psycopg2://mustafa:3KIzwhrFvXe8oy4XFRUfydq68a94T1Nj@dpg-cram02aj1k6c73ch26qg-a.oregon-postgres.render.com/citymart')

# Create your views here.
@csrf_exempt
def RegistrationPage(request):
    msg=None
    if request.method=='POST':
        full_name = request.POST.get('full_name')
        mobile_number = request.POST.get('mobile_number')
        address = request.POST.get('address')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            store_user = CustomUser.objects.create(
                            full_name=full_name,
                            mobile_number=mobile_number,
                            email=email,
                            address=address,
                            password=password
            )
            return redirect('loginpage')
        except Exception as e :
            msg='Mobile Number already Exists'
            return render(request,'registration.html',{'error_msg':msg})
    return render(request,'registration.html')

@csrf_exempt
def LoginPage(request):
    
    error_msg=None
    if request.method=='POST':
        mobile_number = request.POST.get('mobile_number')
        password = request.POST.get('password')
        
        user = authenticate(mobile_number=mobile_number,password=password)
        if user and user.is_superuser==True:
            login(request,user)
            return redirect('admindashboardpage')
        
        if user:
            login(request,user)
            return redirect('homepage')
        else:
            error_msg = "Invalid Credentials"
        
    
    return render(request,'loginpage.html',{'error_msg':error_msg})


def LogoutPage(request):
    logout(request)
    return redirect('homepage')


def SplashPage(request):
    return render(request,'splashpage.html')



def HomePage(request):
    # print('<<<<<<<<<<<<<<<<<')
    # print(request.user)
    
    ## Render the Category from folder
    dir = os.path.join(settings.BASE_DIR, 'static', 'images', 'category')
    folder_list = os.listdir(dir)
    img = []
    img_name =[]
    for files in folder_list:
        img.append(files)
        img_name.append(files.split('.')[0])
    files = zip(img,img_name)
    ####################
    # print(img)
    
    most_purchased_product = WebsiteOrderItems.objects.values('product_code_id').annotate(product_count=Count('product_code_id')).order_by('-product_count')[:10]
    # print('=================')
    # print(most_purchased_product)
    # print('=================')
    top_purchased_list =[]
    for product in most_purchased_product:
        top_purchased_list.append({
            'product_name':ProductInventory.objects.get(product_code=product['product_code_id']).product_name,
            'product_img':ProductInventory.objects.get(product_code=product['product_code_id']).product_image,
            'product_price':ProductInventory.objects.get(product_code=product['product_code_id']).selling_price,
            'product_category':ProductInventory.objects.get(product_code=product['product_code_id']).product_category,
            'product_unit':ProductInventory.objects.get(product_code=product['product_code_id']).product_unit
        })
        
    # print('=================')
    # print(top_purchased_list)
    # print('=================')
    
    get_product = ProductInventory.objects.filter(qty__gt=1)
    unique_product = get_product.values('product_name').distinct()
    
    product_data = []
    for product in unique_product:
        units = get_product.filter(product_name=product['product_name'],qty__gt=1).values_list('product_unit', flat=True).distinct()
        price = get_product.filter(product_name=product['product_name'],qty__gt=1).values_list('selling_price', flat=True).order_by('product_unit')
        mrp = get_product.filter(product_name=product['product_name'],qty__gt=1).values_list('mrp', flat=True).order_by('product_unit')
         
        product_unit_and_price = zip(units,price,mrp)    
        # print('<<<<<<<<<<<<<< >>>>>>>>>>>>>>>>>>>>>>.')
        # print(product_unit_and_price)
        product_data.append({
            'name': product['product_name'],
            'units': product_unit_and_price,  # This will be a list of distinct units
            'image': get_product.filter(product_name=product['product_name']).first().product_image  # Get the image URL
            
        })
    
    
    flour_product = ProductInventory.objects.filter(product_category="Flour (Atta)")
    unique_product_flour = flour_product.values('product_name').distinct()
    
    flour_product_data = []
    for product in unique_product_flour:
        units = flour_product.filter(product_name=product['product_name'],qty__gt=1).values_list('product_unit', flat=True).distinct()
        price = flour_product.filter(product_name=product['product_name'],qty__gt=1).values_list('selling_price', flat=True).order_by('product_unit')
        mrp = flour_product.filter(product_name=product['product_name'],qty__gt=1).values_list('mrp', flat=True).order_by('product_unit')
         
        product_unit_and_price = zip(units,price,mrp)    
        # print('<<<<<<<<<<<<<< >>>>>>>>>>>>>>>>>>>>>>.')
        # print(product_unit_and_price)
        flour_product_data.append({
            'name': product['product_name'],
            'units': product_unit_and_price,  # This will be a list of distinct units
            'image': flour_product.filter(product_name=product['product_name']).first().product_image  # Get the image URL
            
        })
    
    return render(request,'home.html',{'data':files,'most_purchase_product':top_purchased_list,'categ':product_data,'flour':flour_product_data})

def CategoryPage(request):
    dir = os.path.join(settings.BASE_DIR, 'static', 'images', 'category')
    folder_list = os.listdir(dir)
    img = []
    img_name =[]
    for files in folder_list:
        img.append(files)
        img_name.append(files.split('.')[0])
        
    # print('<<<<<<<<<< images <<<<<<<<<<<<<<<< ')
    # print(img)
    # print('<<<<<<<<<< images name <<<<<<<<<<<<<<<< ')      
    # print(img_name) 
    files = zip(img,img_name)
    return render(request,'category.html',{'data':files})


@csrf_exempt
def ContactPage(request):
    if request.method=="POST":
        name = request.POST.get('name')
        mobile = request.POST.get('mobile_number')
        subject = request.POST.get('subject')
        msg = request.POST.get('message')
        
        store_inq = ContactUsForm.objects.create(
                                    customer_name=name,
                                    mobile_number=mobile,
                                    subject=subject,
                                    message=msg,
                                    is_resolved=False)
        
        return redirect('contactpage')
    return render(request,'contactpage.html')




def CategoryWise(request,category):
    # print(category)
    get_product = ProductInventory.objects.filter(product_category=category,qty__gt=1)
    unique_product = get_product.values('product_name').distinct()
    
    product_data = []
    product_price_and_unit=[]
    
    for product in unique_product:
        units = get_product.filter(product_name=product['product_name'],qty__gt=1).values_list('product_unit', flat=True).distinct()
        price = get_product.filter(product_name=product['product_name'],qty__gt=1).values_list('selling_price', flat=True).order_by('product_unit')
        mrp = get_product.filter(product_name=product['product_name'],qty__gt=1).values_list('mrp', flat=True).order_by('product_unit')
        
        # print('<<<<<<<<<,')
        # print(units)
        product_unit_and_price = zip(units,price,mrp)    
        # print('<<<<<<<<<<<<<< >>>>>>>>>>>>>>>>>>>>>>.')
        # print(product_unit_and_price)
        product_data.append({
            'name': product['product_name'],
            'units': product_unit_and_price,  # This will be a list of distinct units
            'image': get_product.filter(product_name=product['product_name']).first().product_image  # Get the image URL
            
        })
    
    return render(request,'categorywiseproduct.html',{'categ':product_data,'selected_category':category})


@csrf_exempt
@login_required
def Add_to_cart(request):
    
    # print('$$$$$$$$$$$$$')
    # print(request.user)
    product_name = request.POST.get('product_name')
    product_unit = request.POST.get('product_unit')
    
    get_product = ProductInventory.objects.get(product_name=product_name,product_unit=product_unit)
    get_user_info = CustomUser.objects.get(mobile_number=request.user)
    
    if 'cart_list' not in request.session:
        request.session['cart_list']=[]
        
    cart_list = request.session['cart_list']
    if get_product.product_code not in [item['product_code'] for item in cart_list]:
        cart_list.append({'product_code': get_product.product_code,
                        'product_name': product_name,
                        'unit':product_unit,
                        'price':get_product.selling_price,
                        'mrp':get_product.mrp,
                        'discount':float(get_product.mrp - get_product.selling_price),
                        'user':get_user_info.mobile_number,
                        })
        
    request.session['cart_list']=cart_list
    message = f"Product {product_name} Added in Cart !!"
    
    return redirect('homepage')
    return render(request,'home.html',{'cart_msg':message})
    # return JsonResponse(cart_list,safe=False)
    # return JsonResponse({'product_code':get_product.product_code,'product':product_name,'unit':product_unit,'price':get_product.selling_price})


from django.template.loader import render_to_string
from django.core.mail import send_mail,EmailMessage
from django.conf import settings
def send_order_confirmation_email(order, order_items):
    subject = 'Order Confirmation'
    order_email_template = render_to_string('website_order_bill_template.html', {
        'customer_name': order.customer_name,
        'order_number': order.order_number,
        'order_items': order_items,
        'total_bill_amount': order.bill_net_amount,
        'address':order.customer_address,
    })
    # plain_message = strip_tags(order_email_template)
    to = order.user_name
    subject='Order Confirmation'
    send_mail(
                    subject,
                    '',
                    from_email=settings.DEFAULT_FROM_EMAIL,  # Sender's email (set in your settings)
                    recipient_list=[to],
                    html_message=order_email_template,
                    fail_silently=False,  # Set to True to suppress exceptions if sending fails
                )
    return HttpResponse(order_email_template)



import razorpay
@login_required
def Cart(request):
    user = request.user
    user_details = CustomUser.objects.get(mobile_number=user)
    
    order_items=[]
    
    if 'cart_list' not in request.session:
        request.session['cart_list']=[]
        
    cart_list = request.session['cart_list']
    # print( request.session['cart_list'])
    if request.method=="POST":
        if 'button_pressed' in request.POST:
            # print('BBBBBBBBBBBBB')
            # print(request.POST.get('button_pressed'))
            # print(request.POST)
            # print(request.session['cart_list'])
            # print('BBBBBBBBBBBBB')
            
            # Update quantities in cart_list based on form data
            updated_cart_list = []
            for item in cart_list:
                product_code = item['product_code']
                quantity_key = f'quantity_{product_code}'
                quantity = request.POST.get(quantity_key, '1')  # Default to 1 if not provided
                
                # Update quantity in cart_list
                updated_item = item.copy()  # Create a copy of the item
                updated_item['quantity'] = int(quantity)  # Convert quantity to integer
                updated_cart_list.append(updated_item)
                
            # Update session cart_list
            request.session['cart_list'] = updated_cart_list
            request.session.modified = True  # Ensure changes are saved
            
            grand_net_amount=0
            discount = 0
            grand_mrp_amount = 0 
            for item in updated_cart_list:
                grand_net_amount += item['quantity']*item['price']
                grand_mrp_amount += item['quantity']*item['mrp']
                discount +=item['discount']
                
                
                
            # print('Mrp Amount - ',grand_mrp_amount)
            # print('Discount - ',discount)
            # print('Grand Amount - ',grand_amount)
            # print('********************')
            # print(request.session['cart_list'])
            
            customer_name = request.POST.get('name')
            mobile_number = request.POST.get('mobile_number')
            address = request.POST.get('address')
            payment_method = request.POST.get('payment_method')
            payment_id = request.POST.get('razorpay_payment_id')
            order_id = request.POST.get('razorpay_order_id')
            signature_id = request.POST.get('razorpay_signature')
            
            client = razorpay.Client(auth=(settings.KEY,settings.SECRET))
            payment = client.order.create(data={'amount':float(grand_net_amount)*100 , 'currency':'INR','payment_capture':1})
            
            # print('********************')
            # print('Paymeny Amount - ',payment)
           
            payment_response = {'payment_id':payment_id,'order_id':order_id,'signature_id':signature_id}
            
            is_paid=False
            is_accepted=False
            if payment_id!='':
                is_paid=True
                
            
            store_order = WebsiteOrder.objects.create(
                                                    customer_name=customer_name,
                                                    customer_mobile_number=mobile_number,
                                                    customer_address=address,
                                                    payment_method=payment_method,
                                                    payment_id=payment_id,
                                                    is_paid=is_paid,
                                                    is_accepted=is_accepted,
                                                    bill_net_amount = grand_net_amount,
                                                    bill_mrp_amount = grand_mrp_amount,
                                                    discount=discount,
                                                    user_name=user_details.email
                                                    )
            
            for item in updated_cart_list:
                
                total_amount = item['price']*item['quantity']
                
                
                order_items.append({
                'order_number':store_order.order_number,
                'product_name': item['product_name'],
                'product_unit': item['unit'],
                'price': item['price'],
                'product_qty' :item['quantity'],
                'total_amount':total_amount,
                'mrp':item['mrp'],
                'discount':item['discount']
                # 'gross_amount':grand_amount,
                })
                
                store_orderitem = WebsiteOrderItems.objects.create(
                    order_number_id=store_order.order_number,
                    product_code_id = item['product_code'],
                    qty =item['quantity'],
                    product_price = item['price'],
                    product_mrp_price = item['mrp'],
                    total_amount =  total_amount  
                )
                
                # Update product Inventry
                update_productInventory = ProductInventory.objects.get(product_code=item['product_code'])
                update_productInventory.qty -= item['quantity']
                update_productInventory.save()
                
            # print('=========================== **************** ====================')
            # print(order_items)
            # print(payment_response)
            # print('=========================== **************** ====================')
            send_order_confirmation_email(store_order, order_items)
            request.session['cart_list'] = []
            
            
            
            return render(request,'payment_successful.html',payment_response)
            
            
        
    return render(request,'cart.html' , {'cart_list':cart_list,'user':user_details})


import json
@require_POST
def Remove_item_from_cart(request):
    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')
        if not item_id:
            return JsonResponse({'success': False, 'error': 'Item ID is required'})

        cart_list = request.session.get('cart_list', [])
        request.session['cart_list'] = [item for item in cart_list if item['product_code'] != item_id]
        # print( request.session['cart_list'])
        return JsonResponse({'success': True})
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON'})
    
    
# @login_required
# def Delivery_details(request):
#     return render(request,"delivery_details_form.html")

@login_required
def Admin_navbar(request):
    user = request.user
    user_name = CustomUser.objects.get(mobile_number=user)
    return render(request,"adminnavbar.html",{'user':user_name})


@login_required
def Admin_dashboard(request):
    try:
        user = CustomUser.objects.get(mobile_number=request.user , is_superuser=True)
        return render(request,"admindashboard.html")
    except Exception as e:
        print(e)
        return redirect('loginpage')   
    
import pandas as pd
import pangres

@login_required
@csrf_exempt
def Upload_product(request):
    if request.method == 'POST':
        # print('@@@@@@@@@@@@@@@@@@@@@')
        # print(request.POST)
        # print('@@@@@@@@@@@@@@@@@@@@@')
        button_pressed = request.POST.get('button_pressed')
        
        if button_pressed=="upload_product":
            get_file = request.FILES.get('productFile')
            if get_file.name.split('.')[-1]=='xlsx':
                df_file = pd.read_excel(get_file)
            if get_file.name.split('.')[-1]=='csv':
                df_file = pd.read_csv(get_file)
            # print(df_file)
            # print(df_file.columns)
            
            try:
                rename_col = {'Product Code':'product_code',
                            'Product Name':'product_name',
                            'Product Image Url':'product_image',
                            'Product Unit':'product_unit',
                            'Product Category':'product_category',
                            'Quantity':'qty',
                            'Product Cost':'cost',
                            'MRP':'mrp',
                            'Selling Price':'selling_price',
                            'First Purchase Date':'first_purchase',
                            'Last Purchase Date':'last_purchase'}
                
                df_file = df_file.rename(columns=rename_col)
                # print(df_file.columns)
                
                table_name='Appone_productinventory'
                df_file.set_index(['product_code'],inplace=True)
                pangres.upsert(engine,df_file,table_name,if_row_exists="update")
                
                return render(request,'upload_product.html',{'msg':'product uploaded successfully !!'})
            
            except Exception as e:
                print(e)
                return render(request,'upload_product.html',{'msg':'Uploaded File is not according to template'})
        
        
        if button_pressed=="add_category":
            category_name = request.POST.get('category_name')
            category_img = request.FILES.get('categoryFile')
            
            file , file_exten = os.path.splitext(category_img.name)
            
            full_file_name = f"{category_name}{file_exten}"
            
            # fs = FileSystemStorage(location='static/images/category')  # Specify the folder path
            fs = FileSystemStorage(location=os.path.join(settings.BASE_DIR, 'static','images','category')) 
            filename = fs.save(full_file_name, category_img)
            uploaded_file_url = fs.url(filename)
            # return HttpResponse(f"Photo uploaded successfully: <a href='{uploaded_file_url}'>View Photo</a>")
            return render(request,'upload_product.html',{'addcat':'New Category Added Successfully !!'})   
        
        
        if button_pressed=="add_productimg":
            product_img = request.FILES.getlist('productImage')
            fs = FileSystemStorage(location=os.path.join(settings.BASE_DIR,'media','products') ) # Specify the folder path
            for files in product_img:
                filename = fs.save(files.name, files)
                # print(product_img)
            return render(request,'upload_product.html',{'addproductimg':'Product Image Uploaded !!'})
                 
    return render(request,'upload_product.html')


def download_product_template(request):
    # Define the path to the template file
    template_path = os.path.join(settings.BASE_DIR, 'excelfiles', 'Product Inventory Template.xlsx')
    
    # Open the file in binary mode
    with open(template_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=Product Inventory Template.xlsx'
        return response
    
    
    
from datetime import date 

@login_required
def get_inventory_data(request):
    get_data = ProductInventory.objects.all()
    sale_cat = [label.product_category for label in get_data]
    
    get_cat = ProductInventory.objects.values('product_category').annotate(total_inventory =Sum('qty'))
    labels = [items['product_category'] for items in get_cat]
    inventory = [items['total_inventory'] for items in get_cat]
    # print(get_cat)
    # print(sale_cat)
    # print(labels)
    # print(inventory)
    
    current_date = date.today()
    month_start_date = date(current_date.year,current_date.month,1)
    # print(month_start_date)
    # get_sales_report = customers_order_from_website.objects.filter(created_at__gt=current_date)
    get_websales_report = WebsiteOrder.objects.filter(order_date__gte=month_start_date)
    last_three_day_sales_report = get_websales_report.values('order_date').annotate(total_orders=Count('order_number')).order_by('order_date')
    # print('************************************************')
    # print(last_three_day_sales_report)
    # print('************************************************')
    sales_list_label = [items['order_date'] for items in last_three_day_sales_report] 
    sales_list_count = [items['total_orders'] for items in last_three_day_sales_report]
    
    payment_mode_wise = get_websales_report.values('payment_method').annotate(total_payments=Count('order_number')).order_by('payment_method')
    # print('************************************************')
    # print(payment_mode_wise)
    # print('************************************************')
    payment_label_list = [items['payment_method'] for items in payment_mode_wise] 
    payment_list_count = [items['total_payments'] for items in payment_mode_wise] 
    
    # get_shopsales_report = salesCustomerData.objects.filter(sales_date__gte=month_start_date)
    # last_three_day_shop_sales_report = get_shopsales_report.values('sales_date').annotate(total_orders=Count('customer_id')).order_by('sales_date')
    # print('************************************************')
    # print(last_three_day_shop_sales_report)
    # print('************************************************')
    # shop_sales_list_label = [items['sales_date'] for items in last_three_day_shop_sales_report] 
    # shop_sales_list_count = [items['total_orders'] for items in last_three_day_shop_sales_report] 
    
    
    total_sales_amount_website = WebsiteOrder.objects.aggregate(Sum('bill_net_amount'))['bill_net_amount__sum'] or 0
    # total_sales_amount_shop = salesCustomerData.objects.aggregate(Sum('total_sale_amount'))['total_sale_amount__sum'] or 0
    
    today_sales_amount_website = WebsiteOrder.objects.filter(order_date=current_date).aggregate(Sum('bill_net_amount'))['bill_net_amount__sum'] or 0
    # today_sales_amount_shop = salesCustomerData.objects.filter(sales_date=current_date).aggregate(Sum('total_sale_amount'))['total_sale_amount__sum'] or 0
    
    total_sales_data_label = ['website sales']
    total_sales_data = [ total_sales_amount_website]
    
    today_sales_data_label = ['website sales']
    today_sales_data = [ today_sales_amount_website]
    # print('************************************************')
    # print(total_sales_data)
    # print('************************************************')
    
    return JsonResponse(data={
        'categories': labels,
        'inventories': inventory,
        'sales_date':sales_list_label,
        'sales_order_count':sales_list_count,
        # 'shop_sales_date':shop_sales_list_label,
        # 'shop_sales_order_count':shop_sales_list_count,
        'payment_label_list':payment_label_list,
        'payment_list_count':payment_list_count,
        'total_sales_label':total_sales_data_label,
        'total_sales_data':total_sales_data,
        'today_sales_label':today_sales_data_label,
        'today_sales_data':today_sales_data
        
    })
    
    
    
def Product_inventory(request):
    get_inventory_report = ProductInventory.objects.all().order_by('product_code')
    return render(request,'admininventory.html',{'inventory':get_inventory_report})


def Customers(request):
    customers = CustomUser.objects.all().order_by('date_joined')
    return render(request,'customers.html',{'customers':customers})


def Admin_orders(request):
    get_order_report = WebsiteOrder.objects.all().order_by('order_number')
    # print(request.GET)
    if 'accept_order_id' in request.GET:
        order_no = request.GET.get('accept_order_id')
        print(order_no)
        Order = WebsiteOrder.objects.get(order_number=order_no)
        Order.is_accepted=True
        Order.save()
    return render(request,'adminorders.html',{'orders':get_order_report})

def Admin_order_items(request,order_number):
    get_order_items_report = WebsiteOrderItems.objects.filter(order_number_id=order_number).select_related('product_code')
    data = []

    # Loop through the order items and extract the relevant details
    for item in get_order_items_report:
        data.append({
            'order_number': item.order_number.order_number,
            'product_code': item.product_code.product_code,
            'product_name': item.product_code.product_name,
            'product_category': item.product_code.product_category,
            'product_unit': item.product_code.product_unit,
            'qty': item.qty,
            'product_MRP_price': item.product_mrp_price,
            'product_price': item.product_price,
            'total_amount': item.total_amount
        })

    # Convert the list of dictionaries into a pandas DataFrame
    # df = pd.DataFrame(data)

    # # Display the DataFrame
    # print(df)
    
    return render(request,'adminorder_items.html',{'data':data,'order_number':order_number})