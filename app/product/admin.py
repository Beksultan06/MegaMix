from django.contrib import admin
from app.product.models import Product, ProductImage, Category, Contact, Order, OrderItem
from django.contrib.admin import SimpleListFilter
from django.utils.timezone import now
from datetime import timedelta
from django.db.models import Sum, F

class DateRangeFilter(admin.SimpleListFilter):
    title = 'Период продаж'
    parameter_name = 'period'

    def lookups(self, request, model_admin):
        return [
            ('today', 'Сегодня'),
            ('week', 'Эта неделя'),
            ('month', 'Этот месяц'),
        ]

    def queryset(self, request, queryset):
        today = now().date()
        if self.value() == 'today':
            return queryset.filter(orderitem__order__created_at__date=today)
        if self.value() == 'week':
            week_start = today - timedelta(days=today.weekday())
            return queryset.filter(orderitem__order__created_at__date__gte=week_start)
        if self.value() == 'month':
            month_start = today.replace(day=1)
            return queryset.filter(orderitem__order__created_at__date__gte=month_start)
        return queryset

class RevenueFilter(SimpleListFilter):
    title = 'Выручка'
    parameter_name = 'revenue'

    def lookups(self, request, model_admin):
        return [
            ('0-1000', 'До 1000'),
            ('1000-5000', '1000-5000'),
            ('5000+', 'Более 5000'),
        ]

    def queryset(self, request, queryset):
        if self.value() == '0-1000':
            return [p for p in queryset if p.total_revenue() <= 1000]
        if self.value() == '1000-5000':
            return [p for p in queryset if 1000 < p.total_revenue() <= 5000]
        if self.value() == '5000+':
            return [p for p in queryset if p.total_revenue() > 5000]
        return queryset

class ImageProductInlin(admin.TabularInline):
    model = ProductImage
    extra = 1 
    verbose_name = "Фото Продукта"
    verbose_name_plural = "Фото Продукта"
    

class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'title', 
        'category', 
        'sold_today', 
        'sold_week', 
        'sold_month', 
        'total_sold', 
        'total_revenue'
    )
    list_filter = ('category', DateRangeFilter)
    search_fields = ('title', 'sku')
    ordering = ('title',)

    def sold_today(self, obj):
        today = now().date()
        return obj.orderitem_set.filter(order__created_at__date=today).aggregate(total=Sum('quantity'))['total'] or 0
    sold_today.short_description = 'Продано сегодня'
    sold_today.admin_order_field = 'orderitem__quantity'

    def sold_week(self, obj):
        today = now().date()
        week_start = today - timedelta(days=today.weekday())
        return obj.orderitem_set.filter(order__created_at__date__gte=week_start).aggregate(total=Sum('quantity'))['total'] or 0
    sold_week.short_description = 'Продано за неделю'

    def sold_month(self, obj):
        today = now().date()
        month_start = today.replace(day=1)
        return obj.orderitem_set.filter(order__created_at__date__gte=month_start).aggregate(total=Sum('quantity'))['total'] or 0
    sold_month.short_description = 'Продано за месяц'

    def total_sold(self, obj):
        return obj.orderitem_set.aggregate(total=Sum('quantity'))['total'] or 0
    total_sold.short_description = 'Всего продано'
    total_sold.admin_order_field = 'orderitem__quantity'

    def total_revenue(self, obj):
        try:
            price = float(obj.price.replace(',', '.'))
        except:
            price = 0
        total = sum(item.quantity * price for item in obj.orderitem_set.all())
        return total
    total_revenue.short_description = 'Выручка'
    total_revenue.admin_order_field = 'orderitem__quantity'

admin.site.register(Product, ProductAdmin)
    
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'created_at', 'total_order_value')
    inlines = [OrderItemInline]

    def total_order_value(self, obj):
        total = 0
        for item in obj.items.all():
            try:
                price = float(item.product.price.replace(',', '.'))
            except:
                price = 0
            total += price * item.quantity
        return total
    total_order_value.short_description = 'Сумма заказа'

admin.site.register(Order, OrderAdmin)

admin.site.register(Category)
admin.site.register(Contact)