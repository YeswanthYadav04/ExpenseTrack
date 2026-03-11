from django.shortcuts import render, redirect
from .models import Expense
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models.functions import TruncMonth
from django.db.models import Sum


@login_required
def dashboard(request):

    transactions = Expense.objects.filter(user=request.user).order_by("date")

    sections = []
    current_section = None
    balance = 0

    # section for expenses before first deposit
    pre_expenses = {
        "deposit": None,
        "expenses": []
    }

    for t in transactions:

        if t.type == "income":

            balance += t.amount

            current_section = {
                "deposit": t,
                "expenses": [],
                "balance_after": balance
            }

            sections.append(current_section)

        else:

            balance -= t.amount

            if current_section:
                current_section["expenses"].append(t)
            else:
                pre_expenses["expenses"].append(t)

        # running balance
        t.running_balance = balance


    # add early expenses section if needed
    if pre_expenses["expenses"]:
        sections.insert(0, pre_expenses)


    # CATEGORY ANALYTICS
    category_totals = {}

    for t in transactions:
        if t.type == "expense":
            category_totals[t.category] = category_totals.get(t.category, 0) + t.amount


    # MONTHLY SPENDING ANALYTICS
    monthly_data = Expense.objects.filter(
        user=request.user,
        type="expense"
    ).annotate(
        month=TruncMonth("date")
    ).values("month").annotate(
        total=Sum("amount")
    ).order_by("month")


    return render(request, "dashboard.html", {
        "sections": sections,
        "balance": balance,
        "transactions": transactions,
        "category_data": category_totals,
        "monthly_data": list(monthly_data)
    })


@login_required
def add_expense(request):

    if request.method == "POST":

        title = request.POST["title"]
        amount = float(request.POST["amount"])
        category = request.POST["category"]
        type = request.POST["type"]

        Expense.objects.create(
            user=request.user,
            title=title,
            amount=amount,
            category=category,
            type=type
        )

        return redirect("dashboard")

    return render(request, "add_expense.html")


@login_required
def delete_expense(request, id):

    expense = Expense.objects.get(id=id, user=request.user)
    expense.delete()

    return redirect("dashboard")


@login_required
def edit_expense(request, id):

    expense = Expense.objects.get(id=id, user=request.user)

    if request.method == "POST":

        expense.title = request.POST["title"]
        expense.amount = request.POST["amount"]
        expense.category = request.POST["category"]
        expense.type = request.POST["type"]

        expense.save()

        return redirect("dashboard")

    return render(request, "edit_expense.html", {"expense": expense})


def register(request):

    if request.method == "POST":

        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("/accounts/login/")

    else:
        form = UserCreationForm()

    return render(request, "register.html", {"form": form})


def home(request):

    return render(request, "home.html")