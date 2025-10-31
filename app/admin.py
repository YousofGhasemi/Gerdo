from django.contrib import admin
from .models import UserProfile, Customer, Currency, Commodity, Box, Bank, Ledger

admin.site.register([UserProfile, Customer, Currency, Commodity, Box, Bank, Ledger])
