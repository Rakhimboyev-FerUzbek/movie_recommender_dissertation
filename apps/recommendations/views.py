from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render

from apps.interactions.models import Rating
from apps.recommendations.forms import RecommendationLabForm
from apps.recommendations.services import RecommendationService


User = get_user_model()


@login_required
def auto_recommendation_view(request):
    service = RecommendationService()
    result = service.recommend_for_user(
        user=request.user,
        model_key="auto",
        top_k=12,
        scenario="normal",
    )

    recent_ratings = (
        Rating.objects.filter(user=request.user)
        .select_related("movie")
        .order_by("-updated_at")[:5]
    )

    context = {
        "result": result,
        "recent_ratings": recent_ratings,
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