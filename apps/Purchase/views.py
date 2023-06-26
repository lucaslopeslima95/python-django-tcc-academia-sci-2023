from django.shortcuts import render,redirect
from django.urls import reverse
from .forms import searchProductToPurchaseForm
from django.contrib import messages
from Product.models import Product
from User.forms import authForm
from django.contrib.auth import authenticate
from .DTO.PurchaseItemDTO import PurchaseItemDTO
from Collaborator.models import Collaborator
from Purchase.models import Purchase,PurchaseItem
from User.models import User


listPurchaseItemsDTO:PurchaseItemDTO = []

def initial_page_purchase(request,listPurchaseItemsDTO = [],login_failed=False):
    try:
        form_code_bar = searchProductToPurchaseForm()
        puchase_list_total_value = 0
        for i in listPurchaseItemsDTO:
            puchase_list_total_value += i.total_cost
    except Exception as e:
        print(f"Exceção ao salvar um colaborador {e}")
        messages.warning(request, "Ocorreu um erro ao registrar o Produto")
    return render(request, 'purchase/initial_purchase.html',
                  {'form_code_bar':form_code_bar,"purchaseItems":listPurchaseItemsDTO,"total":puchase_list_total_value,"authForm":authForm,"login_failed":login_failed })

def finish_purchase(request):
    if len(listPurchaseItemsDTO) == 0:
        messages.warning(request, "Não é possivel Finalizar Sem Adicionar Produtos")
        return initial_page_purchase(request)
    else:
        if request.method == "POST":
                form = authForm(request.POST)
                if form.is_valid():
                    username = form.cleaned_data['username']
                    password = form.cleaned_data['password']
                    user = authenticate(request, username=username, password=password)
                    
                    if user is not None:
                        if save_purchase(user,listPurchaseItemsDTO):
                            messages.success(request, "Salvo com Sucesso.")
                            return initial_page_purchase(request)
                            
                            #implementar Logica para mostrar o consumo da referencia atual
                    else:
                        login_failed = True
                        messages.warning(request, "Usuario ou Senha Errados.")
                        return initial_page_purchase(request,login_failed=login_failed,listPurchaseItemsDTO=listPurchaseItemsDTO)
                else:
                    messages.warning(request, "Credenciais inválidas.")
    return initial_page_purchase(request)
    

def find_product(request):
    product = None
    try:
        form = searchProductToPurchaseForm(request.POST)
        if request.method == "POST":
            if form.is_valid():
                code_bar = form.cleaned_data['code_bar']
                              
                if code_bar != None:
                    product = Product.objects.get(code_bar=code_bar)    
                    purchaseItem = PurchaseItemDTO()  
                    purchaseItem.product = product
                    purchaseItem.price = product.price
                    purchaseItem.total_cost = product.price
                    listPurchaseItemsDTO.append(purchaseItem)
                    
    except (Product.DoesNotExist,Exception) as e:
        print(f"Exceção ao procurar produto {e}")
        messages.warning(request, "Produto não encontrado")
        return initial_page_purchase(request, listPurchaseItemsDTO)
    
    request.method = "GET"   
    return initial_page_purchase(request, listPurchaseItemsDTO)
     
def remove_product_purchase(request,id):
    for produto in listPurchaseItemsDTO:
        if id == produto.product.id:
            listPurchaseItemsDTO.remove(produto)
    return initial_page_purchase(request,listPurchaseItemsDTO)
    
    
def clean_all_products_purchase(request):
    listPurchaseItemsDTO.clear()
    return initial_page_purchase(request,listPurchaseItemsDTO)


def save_purchase(user,listPurchaseItemsDTO):
    try:
      
        collaborator = Collaborator.objects.get(user=user.id)
        purchase_obj = Purchase()
        purchase_obj.collaborator = collaborator
        purchase_obj.save()
        for itemPurchaseDTO in listPurchaseItemsDTO:
            purchaseItem = PurchaseItem()
            Product.objects.filter(id = itemPurchaseDTO.product.id )\
            .update(stock_quantity=(Product.objects.get(id = itemPurchaseDTO.product.id)\
                                    .stock_quantity-1))
            purchaseItem.product = itemPurchaseDTO.product
            purchaseItem.price = itemPurchaseDTO.price
            purchaseItem.purchase = purchase_obj
            purchaseItem.save()

            
    except Exception as e:
        print(f" Exceção ao salva os itens da compra - {e}")
    return True  

