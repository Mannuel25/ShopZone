import requests
from django_filters import rest_framework as filters
from .models import *
from decouple import config


class CategoryFilter(filters.FilterSet):
    class Meta:
        model = Category
        fields = ['name']


class StoreFilter(filters.FilterSet):
    class Meta:
        model = Store
        fields = ['owner', 'name']



class ProductFilter(filters.FilterSet):
    price = filters.NumberFilter(method='filter_by_price')

    class Meta:
        model = Product
        fields = '__all__'

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        currency = self.request.query_params.get('currency', 'NGN')
        if currency and currency != 'NGN':
            for obj in queryset:
                obj.converted_price = self.convert_price_to_currency(obj.price, currency)
        return queryset

    def filter_by_price(self, queryset, name, value):
        currency = self.request.query_params.get('currency', 'NGN')
        if currency and currency != 'NGN':
            conversion_result = self.get_conversion_rate(currency, value)
            print('conversion_result:', conversion_result)
            if conversion_result:
                converted_value = conversion_result['conversion_result']
                return queryset.filter(price__lte=converted_value)
        else:
            return queryset.filter(price__lte=value)

    def convert_price_to_currency(self, price, target_currency):
        """Convert price from NGN to the specified currency."""
        conversion_result = self.get_conversion_rate(target_currency, price)
        if conversion_result:
            return conversion_result['conversion_result']
        return price

    def get_conversion_rate(self, currency_code, amount):
        """Fetch the conversion rate from NGN to the target currency."""
        try:
            # generate your API_KEY here..
            API_KEY = config("API_KEY")
            url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/pair/NGN/{currency_code}/{amount}'
            response = requests.get(url)
            response_data = response.json()
            if response.status_code == 200 and response_data['result'] == 'success':
                return response_data
            return None
        except Exception as e:
            print(f"Error fetching conversion rate: {e}")
            return None

