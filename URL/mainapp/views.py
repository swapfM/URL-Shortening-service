from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import shorty
import random , string
# Create your views here.

@login_required(login_url = "/login/")
def dash(request):
    usr = request.user
    urls = shorty.objects.filter(user = usr)
    return render(request, 'dashboard.html', {'urls':urls})


def randomgen():
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(6))



@login_required(login_url = "/login/")
def generate(request):
    if request.method == "POST":

        pass
        if request.POST['original'] and request.POST['short']:

            usr = request.user
            original = request.POST['original']
            short = request.POST['short']
            check = shorty.objects.filter(short_url = short)
            if not check:
                newurl = shorty(
                    user = usr,
                    long_url = original,
                    short_url = short,
                    
                )
                newurl.save()
                return redirect(dash)
            else:
                messages.error(request, "Already Exists")
                return redirect(dash)
     
        elif request.POST['original']:
            usr = request.user
            original = request.POST['original']
            generated = False
            while not generated:
                short = randomgen()
                check = shorty.objects.filter(short_url = short)
                if not check:
                    newurl = shorty(
                        user = usr,
                        long_url = original,
                        short_url = short,
                        
                    )
                    newurl.save()
                    return redirect(dash)
                else:
                    continue

            
        
        else:
            messages.error(request, "Empty Fields")
            return redirect(dash)
    else:
        return redirect('/dashboard/')
        

def home(request, query= None):
    if not query or query is None:
        return render(request, 'home.html')
    else:
        try:
            check = shorty.objects.get(short_url = query)
            check.visits+=1
            check.save()
            url_to_redirect = check.long_url
            return redirect(url_to_redirect)
        except shorty.DoesNotExist:
            return render(request, 'home.html', {'error' : 'URL does not Exists'})

