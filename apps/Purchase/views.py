from django.dispatch import receiver
from django.shortcuts import render,redirect
from Purchase.PurchaseService.calculateExpends import calculates_and_returns_current_referral_spending, calculates_and_returns_last_reference_spend
from User.models import User
from .forms import searchProductToPurchaseForm
from django.contrib import messages
from Product.models import Product
from User.forms import authForm
from django.contrib.auth import authenticate
from .DTO.PurchaseItemDTO import PurchaseItemDTO
from Collaborator.models import Collaborator
from Purchase.models import Purchase,PurchaseItem
from django.db.models.signals import post_save
from User.emails.emails import confirm_purchase
from django.db.models import Sum



def initial_page_purchase(request):
    cart = PurchaseItemDTO()
    form_code_bar = searchProductToPurchaseForm()
    puchase_list_total_value = None
    
    if request.method == "GET":
        try:
            puchase_list_total_value = 0
            for i in cart.products:
                puchase_list_total_value += i.product.price
            
        except Exception as e:
            print(f"Exceção ao salvar um colaborador {e}")
            messages.warning(request, "Ocorreu um erro ao adicionar o Produto")
        
    return render(request, 'purchase/initial_purchase.html',
               {
                'form_code_bar':form_code_bar,
                'cart':cart,
                'total':puchase_list_total_value,
                'authForm':authForm
                })

def finish_purchase(request):
    cart = PurchaseItemDTO()
    try:
        if request.method == "POST":
                form = authForm(request.POST)
                if form.is_valid():
                    username = form.cleaned_data['username']
                    password = form.cleaned_data['password']
                    user = authenticate(request, username=username, password=password)
                    if user is not None:
                        collaborator = Collaborator.objects.get(user=user.id)
                        if collaborator.active and save_purchase(collaborator):
                            cart.products.clear()                                 
                            messages.success(request, "Salvo com Sucesso.")
                            request.session['total_spends_current'] = float(calculates_and_returns_current_referral_spending(collaborator).aggregate(total=Sum('purchaseitem__price'))['total'])
                            request.session['total_spends_last_referred'] = float(calculates_and_returns_last_reference_spend(collaborator).aggregate(total=Sum('purchaseitem__price'))['total'])
                        else:
                            cart.products.clear()
                            messages.warning(request, "Colaborador Inativo, por favor entre em contato com o RH")
                            return redirect('purchase:initial_purchase')
                            
                    else:
                        messages.warning(request, "Usuario ou Senha Errados.")
                        return redirect('purchase:initial_page_purchase')
                else:
                    messages.warning(request, "Credenciais inválidas.")
    except (Exception,Product.DoesNotExist) as e:
        print(f" Exceção ao finalizar a compra - {e}")
        
    return redirect('purchase:initial_page_purchase')

    
def find_product(request):
    in_cart = PurchaseItemDTO()
    if request.method == "POST":
        product = None
        try:
            form = searchProductToPurchaseForm(request.POST)
            if form.is_valid():
                code_bar = form.cleaned_data['code_bar']
                if code_bar != None:
                    product = Product.objects.get(code_bar=code_bar)
                    if product.stock_quantity < 1:
                        messages.warning(request, f"O {product.name} não possui unidades disponiveis no momento")
                    else:    
                        purchaseItem = PurchaseItem()  
                        purchaseItem.product = product
                        purchaseItem.price = product.price
                        in_cart.products.append(purchaseItem)
        except (Product.DoesNotExist,Exception) as e:
            print(f"Exceção ao procurar produto {e}")
            messages.warning(request, "Produto não encontrado")
        

    return redirect('purchase:initial_page_purchase')
     
def remove_product_purchase(request,id):
    in_cart = PurchaseItemDTO()
    in_cart.products.pop((id-1))
    return redirect('purchase:initial_page_purchase')
    
    
def clean_all_products_purchase(request):
    in_cart = PurchaseItemDTO()
    in_cart.products.clear()
    request.session['total_spends_current'] = 0.0
    request.session['total_spends_last_referred'] = 0.0
    
    return redirect('purchase:initial_page_purchase')


def save_purchase(collaborator:Collaborator) -> bool:
    try:
        listPuchaseItems = []   
        cart = PurchaseItemDTO()
        set_products = set()
        for item in cart.products:
            set_products.add(item.product)
        purchase = Purchase()
        purchase.collaborator = collaborator
        purchase.save()
        for item in set_products:
            count =  0
            for product in cart.products:
                if item.id == product.product.pk:
                    count += 1  
            update_quantity(item,count)
            purchaseItem = PurchaseItem.objects.create(
                                        product=item,
                                        price=item.price,
                                        purchase=purchase,
                                        quantity=count
                                        )
            listPuchaseItems.append(purchaseItem)
            purchaseItem.save()
            
        confirm_purchase(email=collaborator.user.email,nameUser=collaborator.name,purchaseItems=listPuchaseItems)
    except Exception as e:
        print(f" Exceção ao salvar a compra - {e}")
    return True  
   
    
def update_quantity(product,quantity) -> None:
    try:
        Product.objects.filter(id = product.id ).update(\
            stock_quantity=(product.stock_quantity-quantity))
    except Exception as e:
        print(f" Exceção ao atualizar a quantidade do produto - {e}")
        
        
def check_balance(request):
    if request.method == "POST":
        form = authForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                collaborator = Collaborator.objects.get(user=user.id)
                if collaborator.active:          
                    request.session['total_spends_current'] = float(calculates_and_returns_current_referral_spending(collaborator).aggregate(total=Sum('purchaseitem__price'))['total'])
                    request.session['total_spends_last_referred'] = float(calculates_and_returns_last_reference_spend(collaborator).aggregate(total=Sum('purchaseitem__price'))['total'])
                    request.session['only_consult'] = True
                else:
                    messages.warning(request,"Perfil de Colaborador Inativo, entre em contato com o RH")
            else:
                messages.warning(request,"Credenciais Inválidas")
    return redirect('purchase:initial_page_purchase')

def clean_consult(request):
    request.session['total_spends_current'] = 0.0
    request.session['total_spends_last_referred'] = 0.0
    request.session['only_consult'] = False
    return redirect('purchase:initial_page_purchase')
