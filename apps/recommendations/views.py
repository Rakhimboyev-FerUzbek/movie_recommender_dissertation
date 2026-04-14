from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.shortcuts import render

from apps.interactions.models import Favorite
from apps.recommendations.forms import RecommendationLabForm
from apps.recommendations.services import RecommendationService


User = get_user_model()


@login_required
def auto_recommendation_view(request):
    service = RecommendationService()
    result = service.recommend_for_user(
        user=request.user,
        model_key="auto",
        top_k=None,
        scenario="normal",
    )

    all_recommendations = result["recommendations"]

    favorite_movie_ids = set(
        Favorite.objects.filter(user=request.user, movie__is_active=True)
        .values_list("movie_id", flat=True)
    )

    paginator = Paginator(all_recommendations, 24)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    favorite_movie_ids = set(
        Favorite.objects.filter(user=request.user, movie__is_active=True)
        .values_list("movie_id", flat=True)
    )

    context = {
        "result": result,
        "total_recommendations": len(all_recommendations),
        "page_obj": page_obj,
        "recommendations_page": page_obj.object_list,
        "favorite_movie_ids": favorite_movie_ids,
    }
    return render(request, "recommendations/for_you.html", context)


@login_required
def recommendation_lab_view(request):
    if not request.user.is_staff:
        raise PermissionDenied("Bu sahifa faqat staff/demo foydalanuvchilar uchun ochiq.")

    form = RecommendationLabForm(request.GET or None, current_user=request.user)
    selected_user = request.user
    result = None

    if form.is_valid():
        target_user_id = form.cleaned_data.get("user_id") or request.user.id
        selected_user = User.objects.get(pk=target_user_id)

        service = RecommendationService()
        result = service.recommend_for_user(
            user=selected_user,
            model_key=form.cleaned_data["model"],
            top_k=form.cleaned_data["top_k"],
            scenario=form.cleaned_data["scenario"],
        )

    context = {
        "form": form,
        "selected_user": selected_user,
        "result": result,
    }
    return render(request, "recommendations/lab.html", context)