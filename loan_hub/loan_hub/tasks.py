# your_app_name/tasks.py

from celery import shared_task
from .models import Loan, InterestLoan, InterestRate
from decimal import Decimal

@shared_task
def calculate_daily_interest():
    loans = Loan.objects.filter(type_of_loan='MTL Collection', loan_status='Active')
    for loan in loans:
        interest_rate_obj = InterestRate.objects.filter(Type_of_Receipt=loan.type_of_loan).first()
        if interest_rate_obj:
            interest_rate = interest_rate_obj.interest
            daily_interest = round((loan.amount * interest_rate / 100) / 365, 2)

            # Update the existing interest amount
            interest_loan = InterestLoan.objects.filter(original_loan=loan).first()
            if interest_loan:
                interest_loan.amount += daily_interest
                interest_loan.save()
