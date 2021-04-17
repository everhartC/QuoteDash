from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from login.models import User
from .models import Quote

# Create your views here.
def quotes(request):
    if 'user_id' not in request.session:
        return redirect('/')
    
    all_users = User.objects.all()
    user = User.objects.get(id=request.session['user_id'])
    # quotes = Quote.objects.all()
    likes = Quote.objects.filter(users_who_liked__id=user.id)
    total_likes = likes.count()
    
    quotes = Quote.objects.all().order_by('-id').exclude(id__in=[l.id for l in likes])
    all_quotes = Quote.objects.all()
    context = {
        'all_users': all_users,
        'user': user,
        'quotes': quotes,
        'all_quotes': all_quotes,
        'likes': likes,
        'total_likes': total_likes,
    }
    return render(request, "quotes.html", context)

def addQuote(request):
    id = request.session['user_id']
    user = User.objects.get(id=id)
    errors = Quote.objects.validator(request.POST, id)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/quotes")
    else:
        new_quote = Quote.objects.create(
            content = request.POST['quote'],
            author = request.POST['author'],
            poster = user,
        )
        return redirect("/quotes")

def addLike(request, quote_id):
    if 'user_id' not in request.session:
        return redirect('/')

    current_user = User.objects.get(id=request.session['user_id'])
    likedQuotes = Quote.objects.get(id=quote_id)
    current_user.likes.add(likedQuotes)
    return redirect('/quotes')

def deleteQuote(request, quote_id):
    q2del = Quote.objects.get(id=quote_id)
    q2del.delete()
    return redirect('/quotes')



