import random
from datetime import datetime 

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


from django.db import models
from django.utils import timezone



import re

def generate_unique_code(model_class, prefix, length=4):
    """
    Safe sequential code generator.
    Works with old LN codes + new prefixes.
    """

    last_code = (
        model_class.objects
        .filter(code__startswith=prefix)
        .order_by('-code')
        .values_list('code', flat=True)
        .first()
    )

    if last_code:
        match = re.search(r'(\d+)$', last_code)
        last_number = int(match.group()) if match else 0
        new_number = last_number + 1
    else:
        new_number = 1

    return f"{prefix}{new_number:0{length}d}"
# ---------------- Models ----------------

class Receipt(models.Model):
    type_of_receipt = models.CharField(max_length=255)
    ref = models.CharField(max_length=50)
    balance = models.IntegerField()
    cash = models.IntegerField()
    bank1 = models.CharField(max_length=255)
    bank2 = models.CharField(max_length=255)
    adj = models.CharField(max_length=255)
    actions = models.CharField(max_length=50)


class User(models.Model):
    name = models.CharField(max_length=100)
    Mobile = models.CharField(max_length=20)
    Address = models.CharField(max_length=255)
    IFSCcode = models.CharField(max_length=100, blank=True)
    AccountNo1 = models.IntegerField(max_length=50,
    null=True,
    blank=True)
    AccountNo2 = models.IntegerField(max_length=50,
    null=True,
    blank=True)
    IFSCcode2 = models.CharField(max_length=100, blank=True)
    Age = models.CharField(max_length=3, blank=True)
    Email = models.EmailField(max_length=50,
    null=True,
    blank=True)
    code = models.CharField(max_length=10, blank=True, null=True, unique=True)

    BankAccountName = models.CharField(max_length=100, null=True,
    blank=True)
    BranchName = models.CharField(max_length=100, null=True,
    blank=True)
    BankAccountName2 = models.CharField(max_length=100, null=True,
    blank=True)
    BranchName2 = models.CharField(max_length=100, null=True,
    blank=True)

    def __str__(self):
        return self.name

class Loan(models.Model):
    LOAN_TYPES = [
        ('MTL LOAN', 'MTL LOAN'),
        ('FDL LOAN', 'FDL LOAN'),
        ('KVP/NSC LOAN', 'KVP/NSC LOAN'),
        ('MTL INTEREST', 'MTL INTEREST'),
        ('FDL INTEREST', 'FDL INTEREST'),
        ('KVP/NSC INTEREST', 'KVP/NSC INTEREST'),
        ('FIXED DEPOSITS', 'FIXED DEPOSITS'),
        ('THRIFT FUNDS', 'THRIFT FUNDS'),
        ('WELFARE COLLECTIONS', 'WELFARE COLLECTIONS'),
        ('ADMISSION FEES', 'ADMISSION FEES'),
        ('OTHER RECEIPTS', 'OTHER RECEIPTS'),
        ('CASH WITHDRAWALS', 'CASH WITHDRAWALS'),
        ('SALARY PAID', 'SALARY PAID'),
        ('OFFICE EXPENSES', 'OFFICE EXPENSES'),
        ('OTHER PAYMENTS', 'OTHER PAYMENTS')

    ]

    SOURCE_CHOICES = [
        ('RECEIPT', 'Receipt'),
        ('PAYMENT', 'Payment'),
    ]

    gen_no = models.CharField(max_length=100)
    name = models.CharField(max_length=255, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    cash = models.CharField(max_length=10, blank=True, default=0)
    online = models.CharField(max_length=100, blank=True, default='-')
    bank1 = models.CharField(max_length=100, blank=True, default='-')
    bank2 = models.CharField(max_length=100, blank=True, default='-')
    adj = models.CharField(max_length=100, blank=True, default='-')

    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    code = models.CharField(max_length=10, blank=True, null=True, unique=True)

    type_of_loan = models.CharField(max_length=100, choices=LOAN_TYPES)
    source = models.CharField(max_length=100, blank=True, default='-')


    created_at = models.DateTimeField(default=datetime.now)

    loan_status = models.CharField(max_length=50, default='Active')

    def save(self, *args, **kwargs):
        if self.cash in ["", None]:
            self.cash = "0"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name



class InterestRate(models.Model):
    Type_of_Receipt = models.CharField(max_length=100)
    interest = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.Type_of_Receipt


class InterestLoan(models.Model):
    original_loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='interest_loans')
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type_of_loan = models.CharField(max_length=100, default='Other')
    created_at = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=10, blank=True, null=True, unique=True)

    loan_status = models.CharField(max_length=50, default='Active')

    def __str__(self):
        return f"Interest Loan for Loan ID {self.original_loan.id}"


class InterestTransactions(models.Model):
    interest_loan = models.ForeignKey(InterestLoan, on_delete=models.CASCADE, related_name='interest_transactions')
    cash = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bank1 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bank2 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    adj = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=10, blank=True, null=True, unique=True)


    def __str__(self):
        return f"Transaction for Interest Loan ID {self.interest_loan.id}"


class LoanTransactions(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    cash = models.IntegerField()
    bank1 = models.CharField(max_length=255)
    bank2 = models.CharField(max_length=255)
    code = models.CharField(max_length=10, blank=True, null=True, unique=True)

    adj = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


class LoanRepayment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    type_of_loan = models.CharField(max_length=100, blank=True, default='')  # ✅ New field
    total_payment = models.DecimalField(max_digits=10, decimal_places=2)
    paid_to_interest = models.DecimalField(max_digits=10, decimal_places=2)
    paid_to_principal = models.DecimalField(max_digits=10, decimal_places=2)
    payment_mode = models.CharField(max_length=50, blank=True)
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    cash = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bank1 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bank2 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    adj = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    code = models.CharField(max_length=10, blank=True, null=True, unique=True)


import random

def generate_unique_repayment_code():
    while True:
        code = f"LR{random.randint(1000,9999)}"
        if not LoanRepayment.objects.filter(code=code).exists():
            return code

from django.db import models
from django.utils import timezone

class AddCash(models.Model):
    TYPE_CHOICES = [
        ("Cash", "Cash"),
        ("Bank1", "Bank 1"),
        ("Bank2", "Bank 2"),
        ("Adjustment", "Adjustment"),
    ]

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type_of_cash = models.CharField(max_length=20, choices=TYPE_CHOICES)
    remarks = models.CharField(max_length=255, blank=True, null=True)
    datetime = models.DateTimeField(default=timezone.now, editable=False)  # ✅ auto date + time
    code = models.CharField(max_length=6, unique=True, blank=True)

    def __str__(self):
        return f"{self.code} - {self.type_of_cash} - {self.amount}"

# ---------------- Signals ----------------

@receiver(post_save, sender=User)
def set_user_code(sender, instance, created, **kwargs):
    if created and not instance.code:
        instance.code = generate_unique_code(User, 'CN')
        instance.save(update_fields=['code'])

LOAN_CODE_PREFIX = {
    'MTL LOAN': 'MTL',
    'FDL LOAN': 'FDL',
    'KVP/NSC LOAN': 'KVP',
    'MTL INTEREST': 'MTLI',
    'FDL INTEREST': 'FDLI',
    'KVP/NSC INTEREST': 'KVPI',
    'FIXED DEPOSITS': 'FD',
    'THRIFT FUNDS': 'TF',
    'WELFARE COLLECTIONS': 'WC',
    'CASH WITHDRAWALS': 'CW'
}




@receiver(post_save, sender=Loan)
def set_loan_code(sender, instance, created, **kwargs):
    if created and not instance.code:
        prefix = LOAN_CODE_PREFIX.get(instance.type_of_loan, 'LN')

        instance.code = generate_unique_code(
            Loan,
            prefix,
            length=4
        )

        # Avoid recursive save
        Loan.objects.filter(pk=instance.pk).update(code=instance.code)
        
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=LoanRepayment)
def set_loanrepayment_code(sender, instance, created, **kwargs):
    if created and not instance.code:
        # Generate a unique code
        from .models import generate_unique_code  # or ensure it's imported
        instance.code = generate_unique_code(LoanRepayment, 'LT')
        # Update directly in DB to avoid recursive save
        LoanRepayment.objects.filter(pk=instance.pk).update(code=instance.code)


@receiver(post_save, sender=InterestLoan)
def set_interestloan_code(sender, instance, created, **kwargs):
    if created and not instance.code:
        instance.code = generate_unique_code(InterestLoan, 'IL')
        instance.save(update_fields=['code'])

@receiver(post_save, sender=LoanTransactions)
def set_loantransaction_code(sender, instance, created, **kwargs):
    if created and not instance.code:
        instance.code = generate_unique_code(LoanTransactions, 'TX')
        instance.save(update_fields=['code'])

@receiver(post_save, sender=InterestTransactions)
def set_interesttransaction_code(sender, instance, created, **kwargs):
    if created and not instance.code:
        instance.code = generate_unique_code(InterestTransactions, 'IT')
        instance.save(update_fields=['code'])

@receiver(post_save, sender=AddCash)
def set_addcash_code(sender, instance, created, **kwargs):
    if created and not instance.code:
        instance.code = generate_unique_code(AddCash, "AC", 4)
        instance.save(update_fields=['code'])





from django.db import models
from django.utils import timezone

class CashEntry(models.Model):
    TYPE_CHOICES = [
        ("Cash", "Cash"),
        ("Bank1", "Bank 1"),
        ("Bank2", "Bank 2"),
        ("Adjustment", "Adjustment"),
    ]

    # Existing fields
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type_of_cash = models.CharField(max_length=20, choices=TYPE_CHOICES)
    remarks = models.CharField(max_length=255, blank=True, null=True)
    datetime = models.DateTimeField(default=timezone.now, editable=False)
    code = models.CharField(max_length=6, unique=True, blank=True)

    # NEW FIELD
    type_of_loan = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.code} - {self.type_of_cash} - {self.amount} - {self.type_of_loan}"


from django.db import models
from decimal import Decimal


class OtherCashTransaction(models.Model):

    TRANSACTION_TYPE_CHOICES = [
        ('RECEIPT', 'Receipt'),
        ('PAYMENT', 'Payment'),
    ]

    transaction_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_TYPE_CHOICES
    )

    # Gen No (links receipt/payment to user)
    gen_no = models.CharField(max_length=50)

    # Receipt / Payment type
    type_of_loan = models.CharField(max_length=100)

    cash = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    bank1 = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    bank2 = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # ✅ NEW STORED TOTAL
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    code = models.CharField(max_length=20, unique=True, blank=True)

    # created_at = models.DateTimeField(auto_now_add=True),
    created_at = models.DateTimeField(default=datetime.now)
    def save(self, *args, **kwargs):
        """
        Always keep amount = cash + bank1 + bank2
        """
        self.amount = (
            (self.cash or Decimal('0')) +
            (self.bank1 or Decimal('0')) +
            (self.bank2 or Decimal('0'))
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.gen_no} | {self.transaction_type} | {self.amount}"


OTHER_CASH_PREFIX = {
    'RECEIPT': 'RC',
    'PAYMENT': 'PM',
}

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=OtherCashTransaction)
def set_othercash_code(sender, instance, created, **kwargs):
    if created and not instance.code:
        prefix = OTHER_CASH_PREFIX.get(instance.transaction_type, 'OC')

        instance.code = generate_unique_code(
            OtherCashTransaction,
            prefix,
            length=4
        )

        OtherCashTransaction.objects.filter(pk=instance.pk).update(
            code=instance.code
        )

