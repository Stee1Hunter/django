from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.views import View
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Game, Category, Product, User, Basket, Order, OrderItem, Review
from .forms import GameForm, ProductForm, CategoryForm, UserForm, OrderForm, ReviewForm, LoginForm, RegistrationForm
from django.core.paginator import Paginator
from urllib.parse import urlencode
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.decorators import method_decorator
import logging
logger = logging.getLogger(__name__)

class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'main/order_detail.html'
    context_object_name = 'Order'

    def get_queryset(self):
        # Пользователь может видеть только свои заказы
        return Order.objects.filter(user=self.request.user)

class UserOrdersView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'main/myorders.html'
    context_object_name = 'orders'
    paginate_by = 10  # Пагинация по 10 заказов на странице

    def get_queryset(self):
        # Возвращаем только заказы текущего пользователя, отсортированные по дате (новые сначала)
        return Order.objects.filter(user=self.request.user)

def login_user(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if request.GET.get('next'):
                return redirect(request.GET.get('next'))
            return redirect('/')
    else:
        form = AuthenticationForm()
    context = {
        'form': form
    }
    return render(request, 'main/login.html', context)


def registration_user(request):
    if request.method == "POST":
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()  # ← создаём нового пользователя
            login(request, user)  # ← и сразу логиним его
            next_url = request.GET.get('next')
            return redirect(next_url or '/')
    else:
        form = RegistrationForm()

    context = {
        'form': form
    }
    return render(request, 'main/register.html', context)


def logout_user(request):
    logout(request)
    return redirect('/')

@login_required
def profile_view(request):
    return render(request, 'main/profile.html')
@method_decorator(staff_member_required, name='dispatch')
class ProductCreateView(CreateView):
    form_class = ProductForm
    template_name = 'main/product_form.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавить товар'
        return context

@method_decorator(staff_member_required, name='dispatch')
class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'main/product_form.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Редактировать: {self.object.name}'
        return context

@method_decorator(staff_member_required, name='dispatch')
class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'main/product_confirm_delete.html'
    success_url = reverse_lazy('index')

# Игры
@method_decorator(staff_member_required, name='dispatch')
class GameCreateView(CreateView):
    model = Game
    form_class = GameForm
    template_name = 'main/game_form.html'
    success_url = reverse_lazy('index')

@method_decorator(staff_member_required, name='dispatch')
class GameUpdateView(UpdateView):
    model = Game
    form_class = GameForm
    template_name = 'main/game_form.html'
    success_url = reverse_lazy('index')

@method_decorator(staff_member_required, name='dispatch')
class GameDeleteView(DeleteView):
    model = Game
    template_name = 'main/game_confirm_delete.html'
    success_url = reverse_lazy('index')

# Категории
@method_decorator(staff_member_required, name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'main/category_form.html'
    success_url = reverse_lazy('index')
@method_decorator(staff_member_required, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'main/category_form.html'
    success_url = reverse_lazy('index')
@method_decorator(staff_member_required, name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'main/category_confirm_delete.html'
    success_url = reverse_lazy('index')

# Пользователи
@method_decorator(staff_member_required, name='dispatch')
class UserCreateView(CreateView):
    model = User
    form_class = UserForm
    template_name = 'main/user_form.html'
    success_url = reverse_lazy('index')
@method_decorator(staff_member_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    form_class = UserForm
    template_name = 'main/user_form.html'
    success_url = reverse_lazy('index')
@method_decorator(staff_member_required, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    template_name = 'main/user_confirm_delete.html'
    success_url = reverse_lazy('index')

# Заказы
@method_decorator(staff_member_required, name='dispatch')
class OrderListView(ListView):
    model = Order
    template_name = 'main/order_list.html'
    context_object_name = 'orders'
@method_decorator(staff_member_required, name='dispatch')
class OrderDetailView(DetailView):
    model = Order
    template_name = 'main/order_detail.html'
@method_decorator(staff_member_required, name='dispatch')
class OrderUpdateView(UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'main/order_form.html'
    success_url = reverse_lazy('order_list')

# Отзывы

class ReviewListView(ListView):
    model = Review
    template_name = 'main/review_list.html'
    context_object_name = 'reviews'
@method_decorator(staff_member_required, name='dispatch')
class ReviewUpdateView(UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'main/review_form.html'
    success_url = reverse_lazy('review_list')
@method_decorator(staff_member_required, name='dispatch')
class ReviewDeleteView(DeleteView):
    model = Review
    template_name = 'main/review_confirm_delete.html'
    success_url = reverse_lazy('review_list')



class IndexView(View):
    def get(self, request):
        # Получаем игры с товарами, у которых есть скидка
        games = Game.objects.all()
        games_with_discounts = []

        for game in games:
            discounted_products = game.product_set.filter(discount__isnull=False)[:4]
            if discounted_products:
                games_with_discounts.append({
                    'game': game,
                    'products': discounted_products
                })

        context = {
            'games': games,
            'games_with_discounts': games_with_discounts,
            'basket_items_count': self._get_basket_count(request)
        }
        return render(request, 'main/index.html', context)

    def _get_basket_count(self, request):
        if hasattr(request, 'User') and request.user.is_authenticated:
            return Basket.objects.filter(user=request.user).count()
        return 0


class ProductView(View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        reviews = Review.objects.filter(product=product)
        similar_products = Product.objects.filter(
            category=product.category
        ).exclude(id=product.id)[:4]

        context = {
            'product': product,
            'reviews': reviews,
            'similar_products': similar_products,
            'basket_items_count': self._get_basket_count(request)
        }
        return render(request, 'main/prodinfo.html', context)

    def _get_basket_count(self, request):
        if hasattr(request, 'User') and request.user.is_authenticated:
            return Basket.objects.filter(user=request.user).count()
        return 0


class AboutView(View):
    def get(self, request):
        context = {
            'basket_items_count': self._get_basket_count(request)
        }
        return render(request, 'main/about.html', context)

    def _get_basket_count(self, request):
        if hasattr(request, 'User') and request.user.is_authenticated:
            return Basket.objects.filter(user=request.user).count()
        return 0


class BasketView(LoginRequiredMixin, View):
    def get(self, request):
        basket_items = Basket.objects.filter(user=request.user)

        subtotal = sum(item.product.price * item.quantity for item in basket_items)
        discount = sum(
            (item.product.old_price - item.product.price) * item.quantity
            for item in basket_items
            if item.product.discount and item.product.old_price
        )
        total = subtotal - discount if discount else subtotal

        context = {
            'basket_items': basket_items,
            'subtotal': subtotal,
            'discount': discount,
            'total': total,
            'basket_items_count': basket_items.count()
        }
        return render(request, 'main/basket.html', context)


class AddToBasketView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)

        # Проверяем, есть ли уже такой товар в корзине
        basket_item, created = Basket.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': 1}
        )

        if not created:
            basket_item.quantity += 1
            basket_item.save()

        return JsonResponse({
            'success': True,
            'basket_items_count': Basket.objects.filter(user=request.user).count()
        })


class RemoveFromBasketView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        basket_item = get_object_or_404(
            Basket,
            id=item_id,
            user=request.user
        )
        basket_item.delete()

        return JsonResponse({
            'success': True,
            'basket_items_count': Basket.objects.filter(user=request.user).count()
        })


class UpdateBasketView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        try:
            quantity = int(request.POST.get('quantity', 1))
            if quantity < 1:
                raise ValueError
        except (ValueError, TypeError):
            return JsonResponse({'success': False, 'message': 'Invalid quantity'})

        basket_item = get_object_or_404(
            Basket,
            id=item_id,
            user=request.user
        )
        basket_item.quantity = quantity
        basket_item.save()

        return JsonResponse({'success': True})


class CreateOrderView(LoginRequiredMixin, View):
    def post(self, request):
        basket_items = Basket.objects.filter(user=request.user)

        if not basket_items.exists():
            return JsonResponse({'success': False, 'message': 'корзина пустая'})

        # Создаем заказ
        total_price = sum(item.product.price * item.quantity for item in basket_items)
        order = Order.objects.create(
            user=request.user,
            total_price=total_price,
            status='pending'
        )

        # Создаем элементы заказа
        order_items = [
            OrderItem(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
            for item in basket_items
        ]
        OrderItem.objects.bulk_create(order_items)

        # Очищаем корзину
        basket_items.delete()

        return JsonResponse({
            'success': True,
            'order_id': order.id
        })


class AddReviewView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)

        try:
            rating = int(request.POST.get('rating', 0))
            if rating < 1 or rating > 5:
                raise ValueError
        except (ValueError, TypeError):
            return JsonResponse({'success': False, 'message': 'Invalid rating'})

        comment = request.POST.get('comment', '').strip()
        if not comment:
            return JsonResponse({'success': False, 'message': 'Comment cannot be empty'})

        # Проверяем, не оставлял ли пользователь уже отзыв
        if Review.objects.filter(product=product, user=request.user).exists():
            return JsonResponse({'success': False, 'message': 'You have already reviewed this product'})

        Review.objects.create(
            product=product,
            user=request.user,
            rating=rating,
            comment=comment
        )

        return JsonResponse({'success': True})


def catalog_view(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    categories = Category.objects.filter(game=game)
    products = Product.objects.filter(game=game)

    # Получаем параметры из запроса
    params = request.GET.copy()
    selected_categories = params.getlist('category', [])
    min_price = params.get('min_price', '')
    max_price = params.get('max_price', '')
    sort = params.get('sort', 'default')  # default — без сортировки

    # Применяем фильтры
    if selected_categories:
        products = products.filter(category_id__in=selected_categories)

    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
        except ValueError:
            pass

    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            pass

    # Применяем сортировку
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    # По умолчанию — без сортировки

    # Пагинация
    paginator = Paginator(products, 12)  # 12 товаров на странице
    page_number = request.GET.get('page', 1)
    products_page = paginator.get_page(page_number)

    # Функция для генерации URL с текущими параметрами
    def build_url(**kwargs):
        new_params = params.copy()
        for key, value in kwargs.items():
            if value is not None and value != '':
                new_params[key] = value
            else:
                new_params.pop(key, None)
        return f"?{new_params.urlencode()}" if new_params else ""

    context = {
        'game': game,
        'categories': categories,
        'products': products_page,
        'selected_categories': [int(c) for c in selected_categories],
        'min_price': min_price,
        'max_price': max_price,
        'current_sort': sort,
        'build_url': build_url,
    }

    print("Количество товаров после фильтрации:", products.count())

    return render(request, 'main/catalog.html', context)
