from django.shortcuts import render
from django.contrib.auth.models import User
from .models import HistoricalData, Result
from django.contrib.auth import authenticate
from django.contrib import messages, auth
from django.shortcuts import redirect
from .forms import UploadFileForm
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
        if User.objects.filter(username=username).exists():
            return render(request, 'src/signup.html', {'error': 'Username is already taken'})
        else:
            print('Creating user')
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
@login_required
def index(request):
    form = UploadFileForm()
    if request.method == 'POST' and request.FILES:
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['csv_file']
            upload = HistoricalData(user=request.user, csv_file=file)
            upload.save()
            file_path = upload.csv_file.path
            index = upload.pk
            try:
                result_image = app(file_path,index) + '.png'
                result = Result(user=request.user, historical_data=upload, result=result_image)
                result.save()
                return redirect('result', pk=result.pk)
            except(Exception ) as e:
                print(e)
                upload.delete()
                return render(request, 'src/index.html', {'error': 'Invalid file'})
                
        else:
            upload.delete()

        return redirect('index')
    return render(request, 'src/index.html', {'form': form})
@login_required
def results(request):
    results = Result.objects.filter(user=request.user)
    print(results,'results')
    return render(request, 'src/results.html', {'results': results})
@login_required
def result(request, pk):
    result = Result.objects.get(pk=pk)
    return render(request, 'src/result.html', {'result': result})