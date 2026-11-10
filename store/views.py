from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import ensure_csrf_cookie
import os
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET, require_POST
from .models import Product


@ensure_csrf_cookie
def home(request):
    return render(request, "store/index.html")


@require_POST
def style_ai_chat(request):
    """Answer fashion questions using the live SANBAD product catalogue."""
    import json

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return JsonResponse({
            "reply": "SANBAD STYLE AI is almost ready! The store owner needs to add the secure AI API key on the website server first."
        }, status=503)

    try:
        payload = json.loads(request.body or "{}")
        message = str(payload.get("message", "")).strip()
    except (json.JSONDecodeError, AttributeError):
        return JsonResponse({"error": "Please send a valid message."}, status=400)

    if not message:
        return JsonResponse({"error": "Please type a message."}, status=400)
    if len(message) > 1000:
        return JsonResponse({"error": "Please keep your message under 1,000 characters."}, status=400)

    from openai import OpenAI
    from openai import APIError, APITimeoutError, RateLimitError

    products = Product.objects.filter(is_active=True, stock__gt=0).order_by("category", "name")[:60]
    catalogue = [{
        "name": p.name,
        "category": p.category,
        "price_inr": str(p.price),
        "tag": p.tag,
        "description": p.description[:500],
        "stock": p.stock,
    } for p in products]

    history = request.session.get("sanbad_ai_history", [])
    history = history[-8:]
    input_messages = history + [{"role": "user", "content": message}]
    instructions = (
        "You are SANBAD STYLE AI, a warm, helpful fashion shopping assistant for SANBAD, "
        "an Indian clothing boutique for Women, Men and Kids. Brand tagline: Style for Every Generation. "
        "Speak only English. Keep replies friendly, concise and easy to understand. "
        "Use Indian rupees (₹). Recommend only items that appear in the supplied live catalogue. "
        "Never invent product names, prices, stock, discounts, shipping terms or policies. "
        "If no suitable product exists or the catalogue is empty, say so honestly and ask what they need. "
        "When recommending an item, give its exact name, category and listed price. "
        "You may ask one useful question about category, occasion, size preference or budget. "
        "Do not claim you added an item to the cart; explain that the customer can use Add to Bag on the product card. "
        "If asked about payment, delivery, returns or contact details not present in the catalogue, "
        "say the store team can confirm those details.\n\n"
        f"Current available SANBAD products (JSON): {json.dumps(catalogue, ensure_ascii=False)}"
    )

    try:
        client = OpenAI(api_key=api_key, timeout=25.0, max_retries=1)
        response = client.responses.create(
            model=os.environ.get("OPENAI_MODEL", "gpt-5.5"),
            instructions=instructions,
            input=input_messages,
            max_output_tokens=350,
        )
        reply = (response.output_text or "I'm sorry, I couldn't prepare a reply. Please try again.").strip()
        history = (input_messages + [{"role": "assistant", "content": reply}])[-10:]
        request.session["sanbad_ai_history"] = history
        return JsonResponse({"reply": reply})
    except RateLimitError:
        return JsonResponse({"error": "The style assistant is receiving too many requests. Please try again shortly."}, status=429)
    except (APITimeoutError, APIError):
        return JsonResponse({"error": "The style assistant is temporarily unavailable. Please try again in a moment."}, status=502)
    except Exception:
        return JsonResponse({"error": "Something went wrong with the style assistant. Please try again."}, status=500)


@require_GET
def product_list(request):
    products = Product.objects.filter(is_active=True)
    category = request.GET.get("category")
    if category in {"Women", "Men", "Kids"}:
        products = products.filter(category=category)
    data = [{
        "id": p.id,
        "name": p.name,
        "category": p.category,
        "price": float(p.price),
        "tag": p.tag,
        "image": p.image_url or "https://placehold.co/700x900?text=SANBAD",
        "description": p.description,
        "stock": p.stock,
    } for p in products]
    return JsonResponse(data, safe=False)


class StoreLoginView(LoginView):
    template_name = "registration/login.html"


def register(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Your SANBAD account has been created.")
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "store/register.html", {"form": form})


@require_POST
def store_logout(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect("home")
