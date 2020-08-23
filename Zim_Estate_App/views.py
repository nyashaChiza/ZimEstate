from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.views import generic
from .models import Property, Seller, Buyer
from .forms import SearchForm, SigninForm, SignupForm, ContactForm, PropertyForm, BuyerForm
from django.core.mail import send_mail
from paynow import Paynow

from Zim_Estate.settings import EMAIL_HOST_USER


# Create your views here.


def index(request):
    template = 'Zim_Estate_App/home.html'
    form = SearchForm()
    properties = Property.objects.order_by('-date')

    prop = []

    for p in properties:
        if p.is_valid and p.vacant:

            prop.append(p)

    result = set([item.city for item in properties])
    context = {'properties': prop[:6], 'form': form, 'result': list(result)}

    return render(request, template, context)


def my_properties(request):
    template = 'Zim_Estate_App/my_properties.html'
    item = Property.objects.all().filter(seller_id=request.session['user_id'])
    for p in item:
        p.popularity = (p.interested / p.views) * 100
        p.save()
    context = {'property': item}
    return render(request, template, context)


def properties(request):
    template = 'Zim_Estate_App/properties.html'
    prop = Property.objects.order_by('-date')
    property_list = []
    for p in prop:
        if p.is_valid and p.vacant:
            property_list.append(p)
    paginator = Paginator(property_list, 6)
    page = request.GET.get('page', 1)
    try:
        props = paginator.page(page)
    except PageNotAnInteger:
        props = paginator.page(1)
    except EmptyPage:
        props = paginator.page(paginator.num_pages)

    context = {'paginator': paginator, 'properties': props}
    return render(request, template, context)


def account(request):
    form = SigninForm()
    template = 'Zim_Estate_App/account.html'
    context = {'data': [], 'form': form}
    return render(request, template, context)


def my_account(request):
    template = 'Zim_Estate_App/manage.html'
    seller = get_object_or_404(Seller, pk=request.session['user_id'])
    return render(request, template, {'seller': seller, 'user_id': request.session['user_id']})


def offline(request):
    template = 'Zim_Estate_App/offline.html'
    return render(request, template)


def property_details(request, id):
    property_detail = get_object_or_404(Property, pk=id)
    property_detail.views = property_detail.views+1
    property_detail.save()
    seller = get_object_or_404(Seller, pk=property_detail.seller.pk)
    form = BuyerForm()
    context = {'property': property_detail, 'phone': seller.phone_number, 'email': seller.email, 'form': form}
    template = 'Zim_Estate_App/property_details.html'
    return render(request, template, context)


def property_enquiries(request):
    property_list = Property.objects.all().filter(seller_id=request.session['user_id'])
    buyers = Buyer.objects.all()
    buyers_dict = {x.property: x for x in buyers}
    buyers_list = [x for x in buyers_dict.values()]
    buyers_prop = [x for x in buyers_dict.keys()]
    prop = [x for x in property_list]
    y = list(set(prop).intersection(buyers_prop))

    my_buyers = [buyers_dict[p] for p in [pr for pr in y]]
    print(my_buyers)
    context = {'buyers': my_buyers}
    template = 'Zim_Estate_App/property_enquiries.html'
    return render(request, template, context)


def about(request):
    template = 'Zim_Estate_App/about.html'
    context = {'data': []}
    return render(request, template, context)


def edit_property(request, id):
    prop = get_object_or_404(Property, pk=id)
    template = 'Zim_Estate_App/edit_property.html'
    context = {'property': prop}
    return render(request, template, context)


def edit_process(request, id):
    prop = get_object_or_404(Property, pk=id)
    if request.method == 'POST':
        prop.city = request.POST['city']
        prop.suburb = request.POST['suburb']
        prop.size = request.POST['size']
        prop.price = request.POST['price']
        prop.description = request.POST['description']
        prop.property_type = request.POST['property_type']
        prop.contract_type = request.POST['contract_type']
        prop.bedroom_num = request.POST['bedroom_num']
        prop.bathroom_num = request.POST['bathroom_num']
        prop.save()

    template = 'Zim_Estate_App/manage.html'
    context = {'property': prop}
    return render(request, template, context)


def accounts(request, message):
    form = SigninForm()
    template = 'Zim_Estate_App/account.html'
    context = {'data': [], 'form': form, 'message': message}
    return render(request, template, context)


def signup(request):
    template = 'Zim_Estate_App/signup.html'
    form = SignupForm()
    context = {'data': [], 'form': form}
    return render(request, template, context)


def upload_property(request):
    template = 'Zim_Estate_App/upload_property.html'
    form = PropertyForm()
    context = {'form': form}
    return render(request, template, context)


def contact(request):
    template = 'Zim_Estate_App/contact.html'
    form = ContactForm()
    context = {'data': [], 'form': form}
    return render(request, template, context)


def contact_process(request):
    print("contact in")
    if request.method == 'POST':

        # create a form instance and populate it with data from the request:
        form = ContactForm(request.POST or None)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            message = True

            return index(request)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ContactForm()

    return render(request, 'Zim_Estate_App/contact.html', {'form': form})


def buyer_process(request, id):
    if request.method == 'POST':
        prop = get_object_or_404(Property, pk=id)
        rec = prop.seller.email
        print('prop Views: %s' % prop.views)
        print('prop Interested: %s' % prop.interested)
        prop.views = prop.views + 1
        prop.interested = prop.interested + 1
        prop.save()

        print('property: %s' % prop)

        # create a form instance and populate it with data from the request:
        form = BuyerForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            item = form.save(commit=False)
            item.property = prop
            message = "Good day, we would like to inform you we have a client interested in your property " + prop.city+","+prop.suburb + ". The following this the client information " \
                                                                                                                              "\nName: " + \
                      form.cleaned_data['name'] + "  \
                        \nEmail: " + form.cleaned_data['email'] + "  \
                        \nPhone Number: " + form.cleaned_data['phone_number'] + "  \
                        \nMessage : " + form.cleaned_data['message']

            subject = 'An Enquiry Has Been Made On Your Property'
            recipient = rec
            # print(message)
            send_mail(subject, message, EMAIL_HOST_USER, [recipient], fail_silently=True)

            form.save()
            return index(request)
        else:
            print(form.errors)
    # if a GET (or any other method) we'll create a blank form

    return render(request, 'Zim_Estate_App/home.html')


def signup_process(request):
    if request.method == 'POST':

        # create a form instance and populate it with data from the request:
        form = SignupForm(request.POST or None)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            message = True

            return accounts(request, message)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SignupForm()

    return render(request, 'Zim_Estate_App/signup.html', {'form': form})


def signout(request):
    request.session['user_id'] = None
    print('session data: %s ' % request.session['user_id'])
    form = SigninForm()
    return render(request, 'Zim_Estate_App/account.html', {'form': form})


def signin(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SigninForm(request.POST or None)
        # check whether it's valid:

        if form.is_valid():
            password = form.cleaned_data[1]
            email = form.cleaned_data[0]
            print('email: ' + str(email))
            print('pass: ' + str(password))
            if Seller.objects.filter(email=email, password=password):
                print('logged in: %s' % Seller.objects.filter(email=email, password=password))
                request.session['user_id'] = Seller.objects.get(email=email).id
                seller = Seller.objects.get(pk=request.session['user_id']).name
                return render(request, 'Zim_Estate_App/manage.html',
                              {'form': form, 'seller': seller, 'user_id': request.session['user_id']})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SigninForm()

    return render(request, 'Zim_Estate_App/account.html', {'form': form})


def upload_process(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        seller = Seller.objects.get(pk=request.session['user_id'])

        form = PropertyForm(request.POST, request.FILES)
        # check whether it's valid:

        if form.is_valid():
            print('form is valid')
            if request.FILES:
                item = form.save(commit=False)
                item.seller = seller

                print('seller ID: %s' % form.cleaned_data['seller'])
                form.save()
                message = 'Property was successfully uploaded '
                print(message)
                seller = Seller.objects.get(pk=seller.id).name

                return render(request, 'Zim_Estate_App/manage.html', {'message': message, 'seller': seller})
        else:
            print(form.errors)
    # if a GET (or any other method) we'll create a blank form
    else:
        print('failed to upload')
        form = PropertyForm()

    return render(request, 'Zim_Estate_App/upload_property.html', {'form': form})


def search(request):
    print('method: %s' % request.method)
    if request.method == 'POST':
        location = request.POST['location']
        property_type = request.POST['property_type']
        bathroom_num = request.POST['bathroom_num']
        bedroom_num = request.POST['bedroom_num']
        result = Property.objects.all().filter(city=location, property_type=property_type)
        results = [item for item in result]
        paginator = Paginator(result, 6)
        page = request.GET.get('page', 1)
        try:
            props = paginator.page(page)
        except PageNotAnInteger:
            props = paginator.page(1)
        except EmptyPage:
            props = paginator.page(paginator.num_pages)
        template = 'Zim_Estate_App/search.html'
        context = {'paginator': paginator, 'properties': props, 'length': len(results), 'location': location}

        return render(request, template, context)
