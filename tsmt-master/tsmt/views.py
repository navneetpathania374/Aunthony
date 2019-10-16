from django.shortcuts import redirect,render
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.http import HttpResponse, HttpResponseRedirect
from stellar_base.keypair import Keypair
from stellar.models import Accounts
import requests,sys,qrcode,os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



def index(request):
    return redirect('/stellar/')
def remittance(request):
    return render(request,'remittance.html')

def about(request):
    return render(request,'about.html')


def set_mycookie(request):
    from django.http import HttpResponse
    response = HttpResponse('<htm>blah</html>')
    from cryptography.fernet import Fernet
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    cipher_text = cipher_suite.encrypt(b"A really secret message. Not for prying eyes.")

    response.set_cookie('qw', cipher_text)
    #cookie = "TEST"
    #request.session['session_var_name'] = cookie
    return response


def get_mycookie(request):
    from django.http import HttpResponse
    response = HttpResponse('<htm>blah</html>')
    request.COOKIES.get('qw')
    from cryptography.fernet import Fernet
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    cipher_text = cipher_suite.encrypt(b"A really secret message. Not for prying eyes.")
    plain_text = cipher_suite.decrypt(cipher_text)
    response.set_cookie('qw', cipher_text)
    #cookie = "TEST"
    #request.session['session_var_name'] = cookie
    return response


def register_update(request):
    return render(request,'registration_update.html')


from django.contrib.auth import authenticate, login


def settings(request):
    return render(request,'settings.html')


def login_user(request):
    # from http://www.tangowithdjango.com/book17/chapters/login.html
    msg = []
    if request.method != 'POST':
        return render(request,'login.html')
    username = request.POST['username']
    password = request.POST['password']
    print(username, password)
    IP = request.META['REMOTE_ADDR']
    HOST = request.META['REMOTE_HOST']
    print(IP)
    #TO LOG IP
    user  = authenticate(username=username.lower(), password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            msg.append("login_user success")
            return redirect('/stellar/')
            return HttpResponseRedirect('/stellar/login/')
        else:
            return HttpResponse("Your Stellar account is disabled.")
    else:
        print("no login")
        return redirect('/register/')


def logout_user(request):
    logout(request)
    return redirect('/stellar/')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        jname = request.POST['zname']
        name = str(fname) + " " + str(lname)
        print(password, username, email)
        if password and username:
            try:
                user = User.objects.create_user(username=username, password=password,first_name=fname,last_name=lname)
                r = user.save()
                kp = Keypair.random()
                account_id = kp.address().decode()
                seed = kp.seed().decode()
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
                p = Accounts(user_name=username,name=name,address=account_id,seed=seed,qrcode_file=file,mobile_number=jname,email=email)
                p.save()
                if r is None:
                    return render(request,'registration_complete.html')
            except:  # IntegrityError:
                return render(request,'registration_form.html')
        else:
            print("create_user does not contain fields")
            return render(request,'registration_form.html')
       # request was empty

    return render(request,'registration_form.html')


