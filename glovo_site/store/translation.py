from .models import Product, Store
from modeltranslation.translator import TranslationOptions,register



@register(Store)
class ProductTranslationOptions(TranslationOptions):
    fields = ('description',)





