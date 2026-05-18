from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Count, Q
from .models import Category, Supplier, InventoryItem, StockTransaction
from .forms import (
    CategoryForm,
    SupplierForm,
    InventoryItemForm,
    StockTransactionForm,
    LoginForm,
    RegisterForm
)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = LoginForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )

        if user:
            login(request, user)
            return redirect('dashboard')

        messages.error(request, 'Invalid username or password.')

    return render(request, 'user/login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = RegisterForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()

        messages.success(request, 'Account created! Please log in.')
        return redirect('login')

    return render(request, 'user/register.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    items = InventoryItem.objects.select_related('category', 'supplier')

    total_items = items.count()
    all_items = list(items)

    low_stock = [i for i in all_items if i.status == 'low_stock']
    out_of_stock = [i for i in all_items if i.status == 'out_of_stock']

    total_value = sum(i.total_value for i in all_items)

    recent_transactions = StockTransaction.objects.select_related(
        'item',
        'created_by'
    ).order_by('-created_at')[:8]

    categories = Category.objects.annotate(item_count=Count('items'))

    return render(request, 'inventory/dashboard.html', {
        'total_items': total_items,
        'low_stock_count': len(low_stock),
        'out_of_stock_count': len(out_of_stock),
        'total_value': total_value,
        'low_stock_items': low_stock[:5],
        'recent_transactions': recent_transactions,
        'categories': categories,
    })


@login_required
def item_list(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    status_filter = request.GET.get('status', '')

    items = InventoryItem.objects.select_related('category', 'supplier')

    if query:
        items = items.filter(
            Q(name__icontains=query) |
            Q(sku__icontains=query)
        )

    if category_id:
        items = items.filter(category_id=category_id)

    all_items = list(items)

    if status_filter:
        all_items = [i for i in all_items if i.status == status_filter]

    return render(request, 'inventory/itemlist.html', {
        'items': all_items,
        'categories': Category.objects.all(),
        'query': query,
        'selected_category': category_id,
        'selected_status': status_filter,
    })


@login_required
def item_create(request):

    if request.method == 'POST':

        form = InventoryItemForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            item = form.save(commit=False)
            item.created_by = request.user
            item.save()

            messages.success(
                request,
                f'"{item.name}" added to inventory.'
            )

            return redirect('item_list')

    else:

        form = InventoryItemForm()

    return render(request, 'inventory/itemform.html', {
        'form': form,
        'title': 'Add Item'
    })

@login_required
def item_edit(request, pk):

    item = get_object_or_404(
        InventoryItem,
        pk=pk
    )

    if request.method == 'POST':

        form = InventoryItemForm(
            request.POST,
            request.FILES,
            instance=item
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                f'"{item.name}" updated.'
            )

            return redirect('item_list')

    else:

        form = InventoryItemForm(instance=item)

    return render(request, 'inventory/itemform.html', {
        'form': form,
        'title': 'Edit Item',
        'item': item
    })

@login_required
def item_delete(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)

    if request.method == 'POST':
        name = item.name
        item.delete()

        messages.success(request, f'"{name}" deleted.')
        return redirect('item_list')

    return render(request, 'inventory/confirm_delete.html', {
        'object': item,
        'type': 'item'
    })


@login_required
def item_detail(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)

    transactions = item.transactions.select_related(
        'created_by'
    ).order_by('-created_at')[:20]

    return render(request, 'inventory/item_detail.html', {
        'item': item,
        'transactions': transactions
    })


@login_required
def add_transaction(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)

    form = StockTransactionForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        txn = form.save(commit=False)
        txn.item = item
        txn.created_by = request.user

        if txn.transaction_type in ('restock', 'adjustment'):
            item.quantity += txn.quantity
        else:
            item.quantity = max(0, item.quantity - txn.quantity)

        item.save()
        txn.save()

        messages.success(request, 'Stock updated successfully.')

        return redirect('item_detail', pk=item.pk)

    return render(request, 'inventory/transaction_form.html', {
        'form': form,
        'item': item
    })


@login_required
def category_list(request):
    categories = Category.objects.annotate(
        item_count=Count('items')
    ).order_by('name')

    return render(request, 'inventory/category_list.html', {
        'categories': categories
    })


@login_required
def category_create(request):

    if request.method == 'POST':

        form = CategoryForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Category created.'
            )

            return redirect('category_list')

    else:

        form = CategoryForm()

    return render(request, 'inventory/category_form.html', {
        'form': form,
        'title': 'Add Category'
    })


@login_required
def category_edit(request, pk):

    cat = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':

        form = CategoryForm(
            request.POST,
            request.FILES,
            instance=cat
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Category updated.'
            )

            return redirect('category_list')

    else:

        form = CategoryForm(instance=cat)

    return render(request, 'inventory/category_form.html', {
        'form': form,
        'title': 'Edit Category'
    })


@login_required
def category_delete(request, pk):
    cat = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        cat.delete()

        messages.success(request, 'Category deleted.')
        return redirect('category_list')

    return render(request, 'inventory/confirm_delete.html', {
        'object': cat,
        'type': 'category'
    })


@login_required
def supplier_list(request):
    suppliers = Supplier.objects.annotate(
        item_count=Count('items')
    ).order_by('name')

    return render(request, 'inventory/supplier_list.html', {
        'suppliers': suppliers
    })
@login_required
def supplier_create(request):

    if request.method == 'POST':

        form = SupplierForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Supplier added.'
            )

            return redirect('supplier_list')

    else:

        form = SupplierForm()

    return render(request, 'inventory/supplier_form.html', {
        'form': form,
        'title': 'Add Supplier'
    })

@login_required
def supplier_edit(request, pk):

    sup = get_object_or_404(Supplier, pk=pk)

    if request.method == 'POST':

        form = SupplierForm(
            request.POST,
            request.FILES,
            instance=sup
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Supplier updated.'
            )

            return redirect('supplier_list')

    else:

        form = SupplierForm(instance=sup)

    return render(request, 'inventory/supplier_form.html', {
        'form': form,
        'title': 'Edit Supplier'
    })


@login_required
def supplier_delete(request, pk):
    sup = get_object_or_404(Supplier, pk=pk)

    if request.method == 'POST':
        sup.delete()

        messages.success(request, 'Supplier deleted.')
        return redirect('supplier_list')

    return render(request, 'inventory/confirm_delete.html', {
        'object': sup,
        'type': 'supplier'
    })
