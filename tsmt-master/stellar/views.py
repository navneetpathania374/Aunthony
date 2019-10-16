from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect,HttpResponseBadRequest
import requests,sys,qrcode,os
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from stellar_base.builder import Builder
from stellar_base.horizon import Horizon
from stellar_base.keypair import Keypair
from stellar_base.asset import Asset
from .forms import ContactForm,FeedbacksForm,AccountForm
from .models import *
import qrcode
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import redirect

network_data = ['https://horizon-testnet.stellar.org','https://horizon.stellar.org']
SITE_ADDR = 'GAFNKWN2GX7FCCSYLS36OUN2NIWJAU4UVZC44MVTQQX6HDAUZ2UUQL6I'
SITE_SEED = 'SCC2V25EPMDLWUXNOJNLTBFXMWDHLLNJOY4DN5LWIEKFMYADNPW2OFXX'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@login_required()
def index(request):
    return render(request, 'base.html')


@login_required
def send(request):
    if request.method == "POST":
        account = request.POST['to_addr']
        user = request.POST['to_user']
        currency = request.POST['currency']
        amount = request.POST['amount']
        from_address = Accounts.objects.filter(user_name=request.user)
        sender = from_address[0].seed
        return send_payment(request,amount,currency,sender,account)
    return render(request, 'stellar/send.html')
@login_required
def send_contact(request,id,):
    if request.method == "POST":
        account = request.POST['to_addr']
        user = request.POST['to_user']
        currency = request.POST['currency']
        amount = request.POST['amount']
        from_address = Accounts.objects.filter(user_name=request.user)
        sender = from_address[0].seed
        return send_payment(request, amount, currency, sender, account)
    send_detailes = Contact.objects.get(id=id)
    return render(request, 'stellar/send.html', {'send_detailes': send_detailes})
def send_payment(request,amount,currency,sender,account):
    builder = Builder(secret=sender)
    builder.append_payment_op(account,amount,currency)
    builder.sign()
    s = builder.submit()
    print(s['_links'])
    return HttpResponseRedirect("/stellar/accountdetails")

@login_required
def get_contacts(request):
    if request.method =='GET':
        r = Contact.objects.filter(user_name=request.user)
        return render(request, 'stellar/get_contacts.html', {'r': r})

@login_required
def contact_create(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if(form.is_valid()):
            post = form.save(commit=False)
            post.user_name = request.user
            post.save()
            message = _("thank you for your contact")
        else:
            message = _("sorry something went wrong")
        context = {'success': message}
        return render(request, 'stellar/create_contact.html', context)
    if request.method =='GET':
        form = ContactForm()
        return render(request, 'stellar/create_contact.html', {'form': form})

@login_required
def contact_delete(request):
    contact = request.GET.get('contact')
    if contact:
        r = get_object_or_404(Contact,user_name=request.user,contact=contact)
        if r:
            print("delete")
            print(r)
            r.delete()
        else:
            message = _("sorry something went wrong")
            context = {'success': message}
    else:
        print("TEST")
    x = Contact.objects.filter(user_name=request.user)
    return redirect ('get_contacts')
from django.contrib.auth.models import User

@login_required
def request(request):
    if request.method == "POST":
        email = request.POST['email']
        amount = request.POST['amount']
        username = User.objects.get(username=request.user)
        sender = username.email
        print('eamil is ', email)
        subject = "Help"
        message = f'you have payment request of amount {amount} from {sender} click the link {"http://127.0.0.1:8000/stellar/send/"} for pay now'
        send_from = sender
        recipient_list = [email]
        send_mail(subject, message, send_from, recipient_list)
        print("email is send")
        return HttpResponse('Request is send successfully')
    user = Accounts.objects.filter(user_name=request.user)
    account = user[0].address
    carx = Accounts.objects.filter(user_name=request.user)
    for mycar in carx:
        MyCar = mycar.qrcode_file.url
    r = { 'account': account,}
    return render(request, 'stellar/request.html', {'carx': MyCar, 'r': r })

@login_required
def keys(request):
    user = Accounts.objects.filter(user_name=request.user)
    address = user[0].address
    secret_key = user[0].seed
    r = {'address':address,'secret_key':secret_key}
    print(r)
    return render(request, 'stellar/keys.html',{'r':r})

@login_required
def qrcode_gen(request):
    qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,)
    user = Accounts.objects.filter(user_name=request.user)
    address = user[0].address
    qr.add_data(address)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    file = os.path.join(BASE_DIR, 'media') + "/qr/" + str(address) + ".png"
    img.save(file)
    p = Accounts(qrcode_file=file, address=address)
    p.save()
    return HttpResponse('Generate successfull Qrcode')

@login_required
def transactions(request):
    a = Accounts.objects.filter(user_name=request.user)
    address = a[0].address
    hz = Horizon()
    r = hz.account_payments(address)
    x = r['_embedded']['records']
    r = {'r': x,'address': address}
    print(r)
    return render(request, 'stellar/transactions.html', r)

@login_required
def accounts(request):
    try:
        user = Accounts.objects.filter(user_name=request.user)
        username = []
        address = []
        seed = []
        name = []
        for x in user:
            username.append(x.user_name)
            address.append(x.address)
            seed.append(x.seed)
            name.append(x.name)
        r = {'username':username, 'address':address, 'seed':seed, 'name':name}
        return render(request, 'stellar/accounts.html',{'username':username, 'address':address,'name':name,'seed':seed})
    except:
        return render(request, 'stellar/accounts.html')
@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

@login_required
def contact(request):
    if request.method == 'GET':
        form = FeedbacksForm()
    else:
        form = FeedbacksForm(request.POST)
        if form.is_valid():
            Name = form.cleaned_data['Name']
            Email = form.cleaned_data['Email']
            Message = form.cleaned_data['Message']
            Subject = form.cleaned_data['Subject']
            form.save()
            try:
                name = Name
                subject = Subject
                message = f'{Message} from {Email}'
                email_from = Email
                print(email_from)
                recipient_list = ['admin email address add demo@demo.com', ]
                send_mail(subject, message, email_from, recipient_list , name,)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return HttpResponse('Successfully send your Feedback')
    return render(request, "stellar/contact.html", {'form': form})
@login_required
def results(request, account_id):
    response = "You're looking at the results of account_id %s."
    return HttpResponse(response % account_id)
@login_required
def detail(request, str_addr):
    hz = Horizon()
    r = hz.account(str_addr)['balances']
    x = {'r': r}
    return render(request, 'stellar/accountdetails.html', x)
@login_required
def accountdr(request, account_addr):
    hz = Horizon()
    if account_addr is None:
        address_addr = 'GDVRS4JT7QUXBYOZWDAJEQUBJC5L74Q5ASDYK5HROOGJHNBUVKB6CNGW'
    r = hz.account(address_addr)['balances']
    print(r)
    x = {'r': r}
    return render(request, 'stellar/accountdetails.html', x)

@login_required
def accountdetails(request):
    try:
        user = Accounts.objects.filter(user_name=request.user)
        address = user[0].address
        url = 'https://horizon-testnet.stellar.org/accounts/' + address
        r = requests.get(url)
        r= str(r.text).replace('true','True').replace('false','False')
        r = eval(r)
        r = r['balances']

        return render(request, 'stellar/accountdetails.html', {'r':r})
    except:
        return render(request, 'stellar/accountdetails.html')

@login_required
def create_fund(request):
    user = Accounts.objects.filter(user_name=request.user)
    address = user[0].address
    r = requests.get('https://horizon-testnet.stellar.org/friendbot?addr=' + address)
    return HttpResponseRedirect('/stellar/accountdetails/')

def offers(request):
    return render(request, 'index.html')
@login_required
def results(request, account_id):
    response = "You're looking at the results of account_id %s."
    return HttpResponse(response % account_id)

@login_required
def create_account(request):
    if request.method == 'POST':
        username = request.POST['username']
        name = request.POST['name']
        account_id = request.POST['account_id']
        seed = request.POST['seed']
        print("Get data..")
        if username:
            message = _("You account is successfully created")
        else:
            message = _("sorry something went wrong")
        context = {'success': message}
        return render(request, 'stellar/accountcreate.html', context)
    user = Accounts.objects.filter(user_name=request.user)
    address = user[0].address
    seed = user[0].seed
    name = user[0].name
    r = {'account_id':address, 'seed':seed, 'name':name }
    return render(request, 'stellar/accountcreate.html', {'r':r})

@login_required
def get_keys(request):
    user = Accounts.objects.filter(user_name=request.user)
    public_key = user[0].address
    secret_key = user[0].seed
    keys = {'public_key':public_key,'secret_key':secret_key}
    print(keys)
    return render(request,'stellar/keys.html',{'keys':keys})

@login_required
def importaccount(request):
    if request.method == "POST":
        username = request.POST['username']
        address = request.POST['address']
        print('address',address)
        return add_account(request,address)
    user = Accounts.objects.filter(user_name=request.user)
    context = {
        'username':user[0].user_name,
        'seed':user[0].seed
    }
    return render(request,'stellar/import_account.html',context)
@login_required
def add_account(request,private_key):
    if request.method == 'POST':
        user = Accounts.objects.filter(user_name=request.user)
        username = user[0].user_name
        kp = Keypair.random()
        account_id = kp.address().decode()
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4, )
        qr.add_data(account_id)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        file = os.path.join(BASE_DIR, 'media') + "/qr/" + str(account_id) + ".png"
        img.save(file)
        seed = private_key
        p = Accounts(user_name=username, name=user[0].name, address=account_id, seed=seed ,qrcode_file=file)
        p.save()
        return HttpResponseRedirect('/stellar/accounts')


@login_required
def admin_page(request):
    if request.method == 'GET':
        users = LoginHistory.objects.filter(user_name=request.user)
        user = []
        for user_data in users:
            user_data = str(user_data).split(' - ')
            user_data = user_data[0] + "  :- " +  user_data[1] + " :- " + user_data[2] + " :- " +  user_data[3]
            user.append(user_data)
    return render(request, 'stellar/loginhistory.html',{'username':user})


def mobile_number(request):
    if request.method == "POST":
        amount = request.POST['amount']
        currency = request.POST['currency']
        mobile = request.POST['mobile']
        memo = request.POST['memo']
        from_address = Accounts.objects.filter(user_name=request.user)
        print(from_address)
        sender = from_address[0].seed
        to_address = Accounts.objects.get(mobile_number=mobile)
        receiver = to_address.address
        link = "/stellar/verify?amount={}&currency={}&sender={}&reciever={}&memo={}".format(amount, currency, sender,receiver, memo)
        return HttpResponseRedirect(link)
    return render(request, 'stellar/sendmobile.html')

def verify(request):
    if request.method == "POST":
        from_address = Accounts.objects.get(user_name=request.user)
        sender = from_address.seed
        reciever_id = request.POST['reciever']
        currency = request.POST['currency']
        amount = request.POST['amount']
        builder = Builder(secret=sender)
        builder.append_payment_op(reciever_id, amount, currency)
        builder.sign()
        s = builder.submit()
        return HttpResponseRedirect('/stellar/accountdetails')
    else:
        amount = request.GET.get('amount')
        currency = request.GET.get('currency')
        memo = request.GET.get('memo')
        reciever = request.GET.get('reciever')
        context = {'amount':amount,'currency':currency,'reciever':reciever,'memo':memo}
        return render(request, 'stellar/payment_confirmation.html', context)

def Email_address(request):
    if request.method == "POST":
        amount = request.POST['amount']
        currency = request.POST['currency']
        email_id = request.POST['email']
        memo = request.POST['memo']
        from_address = Accounts.objects.get(user_name=request.user)
        data = Accounts.objects.get(email=email_id)
        sender = from_address.seed
        reciever = data.address
        print("sender :",sender)
        print("reciever :",reciever)
        link = "/stellar/verify?amount={}&currency={}&sender={}&reciever={}&memo={}".format(amount,currency,sender,reciever,memo)
        return HttpResponseRedirect(link)
    return render(request, 'stellar/sendemail.html')

def Enter_recipient(request):
    return render(request, 'stellar/enterrecipient.html',)




