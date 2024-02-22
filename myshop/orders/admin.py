from django.contrib import admin
from .models import Order, OrderItem
from django.utils.safestring import mark_safe
from django.http import HttpResponse
import csv
import datetime
from django.urls import reverse


def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    content_disposition = f'attachment; filename={opts.verbose_name_plural}.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition
    writer = csv.writer(response)
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]

    # writing a first row with header information
    writer.writerow([field.verbose_name for field in fields])
    # writing data in rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            try:
                if isinstance(value, datetime.datetime):
                    value = value.strftime('%d/%m/%Y')
                data_row.append(value)
            except Exception as e:
                data_row.append(str(e))  # Handle cases where conversion fails
        writer.writerow(data_row)

    return response

export_to_csv.short_description = 'Export to CSV'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    def order_detail(self, obj):
        url = reverse('orders:admin_order_detail', args=[obj.id])
        return mark_safe(f'<a href="{url}">View</a>')

    def order_payment(self, obj):
        order_items = obj.items.all()
        payment_links = []
        for item in order_items:
            url = item.get_stripe_url()
            if item.stripe_id:
                html = f'<a href="{url}" target="_blank">{item.stripe_id}</a>'
                payment_links.append(html)
        if payment_links:
            return mark_safe(', '.join(payment_links))
        return ''

    def order_pdf(self, obj):  # Define order_pdf within OrderAdmin class
        url = reverse('orders:admin_order_pdf', args=[obj.id])
        return mark_safe(f'<a href="{url}">PDF</a>')

    order_pdf.short_description = 'Invoice'  # Assign short description here

    list_display = ['id', 'first_name', 'last_name', 'email', 'address', 'postal_code', 'city', 'paid', 'created', 'updated', 'order_payment', 'order_detail', 'order_pdf']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    actions = [export_to_csv]
