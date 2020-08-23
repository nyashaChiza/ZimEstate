from django import forms
from django.forms import ModelForm, TextInput, Textarea, ClearableFileInput
from .models import Seller, Property, Contact, Buyer
from django.core.exceptions import NON_FIELD_ERRORS


class PropertyForm(ModelForm):
    class Meta:
        model = Property
        property_choices = (
            (None, 'Type Of Property'), ('Apartment', 'Apartment'), ('House', 'House'), ('Cabin', 'Cabin'),
            ('Stand', 'Stand'))
        contract_choices = (
        (None, 'Type Of Contract'), ('On Lease', 'On Lease'), ('Rent', 'Rent'), ('For Sell', 'For Sell'))
        exclude = ['is_valid', 'date', 'vacant', 'views', 'interested', 'popularity']
        widgets = {'city': TextInput(attrs={'class': 'form-control', 'placeholder': 'Location (City)'}),
                   'suburb': TextInput(attrs={'class': 'form-control', 'placeholder': 'Location (Suburb)' }),
                   'size': TextInput(attrs={'class': 'form-control', 'type': 'number', 'placeholder': 'Size ', }),
                   'seller': TextInput(attrs={'type': 'number', 'hidden': 'hidden', 'value': 1}),
                   'price': TextInput(attrs={'class': 'form-control', 'type': 'number', 'placeholder': 'Price', }),
                   'image1': ClearableFileInput(
                       attrs={'class': 'form-control', 'type': 'file', 'required': 'required'}),
                   'image2': ClearableFileInput(
                       attrs={'class': 'form-control', 'type': 'file', 'required': 'required'}),
                   'image3': ClearableFileInput(
                       attrs={'class': 'form-control', 'type': 'file', 'required': 'required'}),
                   'bedroom_num': TextInput(
                       attrs={'class': 'form-control', 'type': 'number', 'placeholder': 'Number Of Bedrooms', }),
                   'bathroom_num': TextInput(
                       attrs={'class': 'form-control', 'type': 'number', 'placeholder': 'Number Of Bathrooms', }),
                   'property_type': forms.Select(choices=property_choices,
                                                 attrs={'choices': property_choices, 'class': 'form-control col-md-8',
                                                        'placeholder': 'Property Type ', }),
                   'contract_type': forms.Select(choices=contract_choices,
                                                 attrs={'choices': contract_choices, 'class': 'form-control col-md-8',
                                                        'placeholder': 'Contract Type    ', }),
                   'description': Textarea(
                       attrs={'max_length': 500, 'cols': 25, 'rows': 6, 'class': 'form-control  w-100',
                              'placeholder': 'Enter Description'}),
                   }


class SearchForm(forms.Form):
    property_type = forms.ChoiceField(widget=TextInput(attrs={'class': 'wide'}), label='property_type',
                                      choices=(('apartment', 'apartment'), ('house', 'House'),
                                               ('cottage', 'Cottage'), ('cabin', 'Cabin')))
    location = forms.ChoiceField(label='location', widget=TextInput(attrs={'class': 'wide'}),
                                 choices=(('a', 'aye'), ('b', 'bee'), ('c', 'see')))
    price = forms.IntegerField(label='price', widget=TextInput(attrs={'class': 'wide'}))
    bedroom_num = forms.ChoiceField(label='bedroom_num',
                                    choices=((1, '01'), (2, '02'), (3, '03'), (4, '04'), (5, '05'), (6, '06')))
    bathroom_num = forms.ChoiceField(label='bathroom_num', widget=TextInput(attrs={'class': 'wide'}),
                                     choices=((1, '01'), (2, '02'), (3, '03'), (4, '04'), (5, '05'), (6, '06')))


class SigninForm(forms.Form):
    email = forms.EmailField(label='email', max_length=80,
                             widget=forms.TextInput(
                                 attrs={'type': 'email', 'class': 'form-control', 'placeholder': 'you@example.com', }))
    password = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                            'placeholder': 'Password',
                                                                            'type': 'password'}))

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if not Seller.objects.filter(email=email, password=password):
            raise forms.ValidationError('Invalid Log In Details')
        return [email, password]


class SignupForm(ModelForm):
    class Meta:
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "%(model_name)s's %(field_labels)s are not unique.",
            }
        }
        model = Seller
        fields = ('name', 'surname', 'phone_number', 'email', 'password')
        widgets = {'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name', }),
                   'surname': TextInput(attrs={'class': 'form-control', 'placeholder': 'Surname', }),
                   'phone_number': TextInput(
                       attrs={'class': 'form-control', 'type': 'tel', 'placeholder': 'Phone Number'}),
                   'email': TextInput(
                       attrs={'type': 'email', 'class': 'form-control', 'placeholder': 'you@example.com', }),
                   'password': TextInput(
                       attrs={'class': 'form-control', 'placeholder': 'Password', 'type': 'password'}),

                   # 're_password': TextInput(
                   #    attrs={'class': 'form-control', 'placeholder': 'Re-enter Password', 'type': 'password'}),

                   }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Seller.objects.filter(email=email):
            raise forms.ValidationError('Email Already In Use')
        return self.cleaned_data['email']



class ContactForm(ModelForm):
    class Meta:
        fields = '__all__'
        model = Contact
        widgets = {'name': TextInput(attrs={'class': 'form-control valid', 'placeholder': 'Name', }),
                   'message': Textarea(
                       attrs={'cols': 30, 'rows': 9, 'class': 'form-control  w-100', 'placeholder': 'Enter Message'}),
                   'email': TextInput(attrs={'class': 'form-control  valid', 'placeholder': 'Email', 'type': 'email'}),
                   'subject': TextInput(attrs={'class': 'form-control  valid', 'placeholder': 'Subject'}),
                   }


class BuyerForm(ModelForm):
    class Meta:
        model = Buyer
        fields = '__all__'

        widgets = {'name': TextInput(attrs={'placeholder': 'Your Name', }),
                   'message': Textarea(attrs={'cols': 30, 'rows': 10, 'placeholder': 'Enter Message'}),
                   'email': TextInput(attrs={'placeholder': 'Email', 'type': 'email'}),
                   'phone_number': TextInput(attrs={'placeholder': 'Phone Number', 'type': 'tel'}),
                   'property': TextInput(attrs={'value': 16, 'hidden': 'hidden', 'type': 'number'}),
                   }


'''    def clean_password(self):
        cleaned_data = super(SignupForm, self).clean()
        print('password: %s' % self.cleaned_data.get('password'))
        print('Re-password: %s' % self.cleaned_data.get('re_password'))
        # print('Re-password: %s' % self.cleaned_data.get('re_password'))
        if self.cleaned_data.get('password') != self.cleaned_data.get('re_password'):
            raise forms.ValidationError('Passwords Do Not Match')
        return self.cleaned_data['password']
'''
