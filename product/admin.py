from django.contrib import admin
from .models import Category, Image, Product

admin.site.register(Category)
admin.site.register(Image)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ["title", "_owner", "create_at", "scheduled_date"]
	exclude = ["owner",]

	def _owner(self, instance):
		return f"{instance.owner.get_full_name()}"

	def get_queryset(self, request):
		query = super(ProductAdmin, self).get_queryset(request)
		return query.filter(owner=request.user)

	def save_model(self, request, obj, form, change):
		obj.owner = request.user
		super().save_model(request, obj, form, change)
