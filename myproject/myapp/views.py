import os
import joblib
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from .models import Sentence
from django.conf import settings

# --------- Load ML Model (joblib) -----------
# Load model and vectorizer from the specified path
MODEL_PATH = os.path.join(settings.BASE_DIR, 'myapp/sentiment_model.joblib')
VECTORIZER_PATH = os.path.join(settings.BASE_DIR, 'myapp/vectorizer.joblib')

# Load the saved model and vectorizer
model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

# ---------- Authentication ----------
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect("login")

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, "signup.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return render(request, "signup.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, "signup.html")

        User.objects.create_user(username=username, email=email, password=password1)
        messages.success(request, "Account created successfully. Please log in.")
        return redirect("login")

    return render(request, "signup.html")

# ---------- Sentiment Analyzer ----------
def analyze_sentiment(text):
    try:
        # Transform input text and predict sentiment
        X = vectorizer.transform([text])  # Use the vectorizer to convert text into features
        prediction = model.predict(X)    # Predict sentiment
        return prediction[0]             # returns 'positive', 'negative', or 'neutral'
    except Exception as e:
        raise RuntimeError(f"Error during sentiment prediction: {e}")

# ---------- Home ----------
@login_required
def home(request):
    sentences = Sentence.objects.all().order_by('-created_at')

    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        if text:
            try:
                sentiment = analyze_sentiment(text)
                Sentence.objects.create(user=request.user, text=text, sentiment=sentiment, created_at=now())
                messages.success(request, f"Sentiment analysis: {sentiment.capitalize()}")
            except Exception as e:
                messages.error(request, f"Error analyzing sentiment: {e}")
            return redirect('home')

    return render(request, 'home.html', {'sentences': sentences})