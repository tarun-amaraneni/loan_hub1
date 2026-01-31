from django import forms
from .models import User
from .models import Loan
from .models import InterestRate

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'Mobile', 'Address','code' #'IFSCcode', 'AccountNo1', 'AccountNo2',
                  #'IFSCcode2', 'Age', 'Email', 'BankAccountName', 
                  #'BranchName', 'BankAccountName2', 'BranchName2'
                  ]
        widgets = {
            'Age': forms.NumberInput(attrs={'type': 'number'}),
            'AccountNo1': forms.NumberInput(attrs={'type': 'number'}),
            'AccountNo2': forms.NumberInput(attrs={'type': 'number'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        if not name:
            raise forms.ValidationError('Name is required.')
        return cleaned_data
    

class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['gen_no', 'name', 'amount', 'cash', 'online', 'bank1','bank2','adj','type_of_loan']
    gen_no = forms.CharField(
        label='Gen.no',
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'No', 'class': 'input-box3'})
    )
    amount = forms.DecimalField(
        label='Amount',
        max_digits=10,
        decimal_places=2,
        required=True,
        widget=forms.NumberInput(attrs={'placeholder': 'Amount', 'class': 'input-box3'})
    )
    cash = forms.DecimalField(
        label='Cash',
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'Cash', 'class': 'input-box3'})
    )
    online = forms.CharField(
        label='Online',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Online', 'class': 'input-box3'})
    )
    bank1 = forms.CharField(
        label='Bank1',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Bank1', 'class': 'input-box3'})
    )
    bank2 = forms.CharField(
        label='Bank2',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Bank2', 'class': 'input-box3'})
    )
    adj = forms.CharField(
        label='Adj',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Adj', 'class': 'input-box3'})
    )
    # type_of_loan = forms.ChoiceField(
    #     label='Loan Type',
    #     # choices=[('type1', 'Type 1'), ('type2', 'Type 2')],  # replace with actual choices
    #     required=True,
    #     widget=forms.Select(attrs={'class': 'input-box3'})
    # )
 
class IntrestForm(forms.ModelForm):
    class Meta:
        model = InterestRate
        fields = ['Type_of_Receipt', 'interest']


from django import forms
import datetime

class DateSelectionForm(forms.Form):
    MONTH_CHOICES = [(str(i), datetime.date(2000, i, 1).strftime('%B')) for i in range(1, 13)]
    YEAR_CHOICES = [(str(year), str(year)) for year in range(2000, datetime.datetime.now().year + 1)]

    month = forms.ChoiceField(choices=MONTH_CHOICES)
    year = forms.ChoiceField(choices=YEAR_CHOICES)
