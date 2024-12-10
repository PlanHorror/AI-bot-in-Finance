from django.shortcuts import render
from django.contrib.auth.models import User
from .models import HistoricalData, Result
from django.contrib.auth import authenticate
from django.contrib import messages, auth
from django.shortcuts import redirect
from .forms import UploadFileForm, UploadTwoFilesForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from lstm_stock_predictor_closing import *
# Create your views here.
def home(request):
    return render(request, 'src/home.html')
def signup(request):
    if request.method == 'POST':
        print(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        password1 = request.POST['password1']
        if User.objects.filter(username=username).exists():
            return render(request, 'src/signup.html', {'error': 'Username is already taken'})
        else:
            if password != password1:
                return render(request, 'src/signup.html', {'error': 'Passwords do not match'})
            user = User.objects.create_user(username=username, password=password)
            user.save()
        return redirect('signin')
    return render(request, 'src/signup.html')
def signin(request):
    if request.method == 'POST':
        print(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is None:
            return render(request, 'src/signin.html', {'error': 'User not found'})
        else:
            auth.login(request, user)
            return redirect('index')
    return render(request, 'src/signin.html')
@login_required(login_url='signin')
def index(request):
    form = UploadTwoFilesForm()
    if request.method == 'POST' and request.FILES:
        form = UploadTwoFilesForm(request.POST, request.FILES)
        if form.is_valid():
            price_file = request.FILES['price_csv']
            fng_file = request.FILES['fng_csv']
            
            # Save price data
            price_upload = HistoricalData(user=request.user, csv_file=price_file)
            price_upload.save()
            
            # Save Fear and Greed data
            fng_upload = HistoricalData(user=request.user, csv_file=fng_file)
            fng_upload.save()
            
            try:
                # Pass both file paths to app function
                result_image = app(
                    price_upload.csv_file.path, 
                    fng_upload.csv_file.path, 
                    price_upload.pk
                ) + '.png'
                
                result = Result(
                    user=request.user, 
                    historical_data=price_upload, 
                    result=result_image
                )
                result.save()
                return redirect('result', pk=result.pk)
            
            except Exception as e:
                print(e)
                price_upload.delete()
                fng_upload.delete()
                return render(request, 'src/index.html', {'error': 'Invalid files'})
        
        return redirect('index')
    return render(request, 'src/index.html', {'form': form})
@login_required(login_url='signin')
def results(request):
    results = Result.objects.filter(user=request.user)
    return render(request, 'src/results.html', {'results': results})
@login_required(login_url='signin')
def result(request, pk):
    result = Result.objects.get(pk=pk)
    return render(request, 'src/result.html', {'result': result})
@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')