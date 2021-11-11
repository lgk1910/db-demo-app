from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.db.models.fields import CharField, NullBooleanField
from django.db.models.fields.related import ForeignKey
from datetime import date
from django.contrib.auth.models import User

from main.forms import Quantity

# Create your models here.
class Book(models.Model):
    isbn = models.CharField(max_length=13, primary_key=True)
    url = models.URLField()
    book_name = models.CharField(max_length=255)
    buy_price = models.IntegerField()
    rent_price = models.IntegerField()

    def __str__(self):
        return f"{self.book_name} ({self.isbn})"

class DigitalVersion(models.Model):
    isbn = models.ForeignKey(Book, on_delete=models.CASCADE, unique=True)
    digital_warehouse = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return f"Book {self.isbn} stored in {self.digital_warehouse}"

class HardCopy(models.Model):
    isbn = models.ForeignKey(Book, on_delete=models.CASCADE, unique=True)

    def __str__(self):
        return f"Book {self.isbn}"

class Warehouse(models.Model):
    warehouse_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.warehouse_name}"

class StoreInfo(models.Model):
    quantity = models.IntegerField()
    isbn = models.ForeignKey(HardCopy, on_delete=models.CASCADE)
    warehouse_id = models.ForeignKey(Warehouse, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.quantity} units of {self.isbn} stored in warehouse {self.warehouse_id}"

class Author(models.Model):
    author_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.author_name}"

class PublicationInfo(models.Model):
    isbn = models.ForeignKey(Book, on_delete=models.CASCADE)
    author_name = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return f"Book {self.isbn} is written by {self.author_name}"

class Keyword(models.Model):
    isbn = models.ForeignKey(Book, on_delete=models.CASCADE)
    keyword_name = models.CharField(max_length=32)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['isbn', 'keyword_name'], name='isbn-keyword composite key')
        ]

    def __str__(self):
        return f"{self.isbn} - {self.keyword_name}"
    
class Genre(models.Model):
    isbn = models.ForeignKey(Book, on_delete=models.CASCADE)
    genre_name = models.CharField(max_length=32)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['isbn', 'genre_name'], name='isbn-genre_name composite key')
        ]
    def __str__(self):
        return f"Book {self.isbn} is {self.genre_name}"

class Customer(models.Model):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.username}"

class Card(models.Model):
    card_code = models.IntegerField(unique=True)
    owner_name = models.CharField(max_length=255)
    expired_date = models.DateField()
    branch_name = models.CharField(max_length=255) 
    bank = models.CharField(max_length=255)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    cvv = models.IntegerField()
    balance = models.IntegerField(default=200000)

    def __str__(self):
        return f"Card of {self.customer}"

class TransactionInfo(models.Model):
    bookstore_account = models.IntegerField(default=666666, null=False)
    total_price = models.IntegerField()
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    trans_date = models.DateField(default=date.today)

    def __str__(self):
        return f"{self.customer} {self.id}"

class TransactionDetail(models.Model):
    trans_id = models.ForeignKey(TransactionInfo, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    service = models.BooleanField(null=False)
    price = models.IntegerField()
    trans_date = models.DateField(default=date.today)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"Book {self.book} - { self.service} - {self.price}$"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    quantity = models.IntegerField(default=0)
    total_price = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user}'s cart"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    service = models.BooleanField()
    total_price = models.IntegerField()

    def __str__(self):
        return f"{self.quantity} {self.book}"


