from django.shortcuts import render, redirect
from reviews.forms import ReviewForm
from django.shortcuts import redirect, render
from .models import Store, Review
from .forms import StoreForm, CommentForm
from django.contrib import messages

from django.db.models import Avg

# Create your views here.
def index(request):
    stores = Store.objects.all()
    context = {
        "stores": stores,
    }
    return render(request, "reviews/index.html", context)


def store(request):
    if request.method == "POST":
        store_form = StoreForm(request.POST, request.FILES)
        if store_form.is_valid():
            store = store_form.save(commit=False)
            store.save()
            return redirect("reviews:index")
    else:
        store_form = StoreForm()

    context = {
        "store_form": store_form,
    }

    return render(request, "reviews/store.html", context)


def store_detail(request, store_pk):
    store = Store.objects.get(pk=store_pk)
    reviews = Review.objects.all()

    if request.POST.get('grade-5'):
      reviews = Review.objects.filter(grade=5)
      print('로직')
    elif request.POST.get('grade-4'):
      reviews = Review.objects.filter(grade=4)
    elif request.POST.get('grade-3'):
      reviews = Review.objects.filter(grade=3)
    elif request.POST.get('grade-2'):
      reviews = Review.objects.filter(grade=2)
    elif request.POST.get('grade-1'):
      reviews = Review.objects.filter(grade=1)
    elif request.POST.get('reset'):
      reviews = Review.objects.order_by("-pk")

    print(reviews[0])
    review_5 = Review.objects.filter(grade=5).count()
    review_4 = Review.objects.filter(grade=4).count()
    review_3 = Review.objects.filter(grade=3).count()
    review_2 = Review.objects.filter(grade=2).count()
    review_1 = Review.objects.filter(grade=1).count()

    ave = Review.objects.aggregate(Avg('grade'))

    # round(값, 표시하고 싶은 자리수)
    review_ave = round(ave['grade__avg'], 2)

    context = {
        "store": store,
        # "reviews":store.review_set.order_by("-pk"),
        "reviews": reviews,
        "review_5": review_5,
        "review_4": review_4,
        "review_3": review_3,
        "review_2": review_2,
        "review_1": review_1,
        "review_ave": review_ave,
    }
    return render(request, "reviews/store_detail.html", context)


def review_create(request, store_pk):
    store = Store.objects.get(pk=store_pk)
    if request.method == "POST":
        review_form = ReviewForm(request.POST, request.FILES)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.store = store
            review.user = request.user
            review.save()
            return redirect("reviews:store_detail", store.pk)
    else:
        review_form = ReviewForm()
    context = {
        "review_form": review_form,
    }
    return render(request, "reviews/review_form.html", context)


def review_detail(request, store_pk, review_pk):
    review = Review.objects.get(pk=review_pk)
    store = Store.objects.get(pk=store_pk)
    context = {
        "review": review,
        "store": store,
    }
    return render(request, "reviews/review_detail.html", context)


def review_delete(request, store_pk, review_pk):
    review = Review.objects.get(pk=review_pk)
    if request.user == review.user:
        if request.method == "POST":
            review.delete()
            return redirect("reviews:store_detail", store_pk)
    return redirect("reviews:store_detail", store_pk)


def review_update(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    if request.user == review.user:
        if request.method == "POST":
            review_form = ReviewForm(request.POST, request.FILES, instance=review)
            if review_form.is_valid():
                form = review_form.save(commit=False)
                form.user = request.user
                form.save()
                return redirect("reviews:review_detail", review_pk)
        else:
            review_form = ReviewForm(instance=review)
        context = {
            "review_form": review_form,
        }
        return render(request, "reviews/review_form.html", context)
    else:
        messages.warning(request, "작성자만 수정할 수 있습니다.")
        return redirect("articles:detail", review.pk)
