from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.db.models import Count
from django.shortcuts import render
from django.urls import reverse

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

    context = {
        "result": result,
        "total_recommendations": len(all_recommendations),
        "recommendations": all_recommendations,
        "favorite_movie_ids": favorite_movie_ids,
    }
    return render(request, "recommendations/for_you.html", context)


@login_required
def recommendation_lab_view(request):
    if not request.user.is_staff:
        raise PermissionDenied("Bu sahifa faqat staff/demo foydalanuvchilar uchun ochiq.")

    annotated_users = list(
        User.objects.select_related("profile")
        .annotate(
            ratings_count=Count("ratings", distinct=True),
            favorites_count=Count("favorites", distinct=True),
            watch_history_count=Count("watch_history", distinct=True),
        )
        .order_by("username")
    )

    form = RecommendationLabForm(request.GET or None, current_user=request.user)

    default_user_id = int(form.initial.get("user_id") or request.user.id)
    default_model = form.initial.get("model") or form.fields["model"].initial or "hybrid"
    default_scenario = form.initial.get("scenario") or form.fields["scenario"].initial or "normal"
    default_top_k = form.initial.get("top_k") or form.fields["top_k"].initial or 10

    if form.is_valid():
        target_user_id = form.cleaned_data.get("user_id") or request.user.id
        model_key = form.cleaned_data.get("model") or default_model
        scenario = form.cleaned_data.get("scenario") or default_scenario
        top_k = form.cleaned_data.get("top_k") or default_top_k
    else:
        target_user_id = default_user_id
        model_key = default_model
        scenario = default_scenario
        top_k = default_top_k

    selected_user = next((user for user in annotated_users if user.id == target_user_id), None) or request.user

    service = RecommendationService()
    result = service.recommend_for_user(
        user=selected_user,
        model_key=model_key,
        top_k=top_k,
        scenario=scenario,
    )

    favorite_movie_ids = set(
        Favorite.objects.filter(user=request.user, movie__is_active=True)
        .values_list("movie_id", flat=True)
    )

    lab_user_summaries = {}
    for user in annotated_users:
        try:
            profile = user.profile
        except ObjectDoesNotExist:
            profile = None

        display_name = user.get_full_name().strip() or user.username
        preferred_genres = list((profile.preferred_genres if profile else []) or [])
        photo_url = profile.profile_photo.url if profile and profile.profile_photo else ""

        can_open_interactions = request.user.is_superuser or user.id == request.user.id

        lab_user_summaries[str(user.id)] = {
            "id": user.id,
            "username": user.username,
            "display_name": display_name,
            "photo_url": photo_url,
            "initial": (display_name[:1] or user.username[:1] or "U").upper(),
            "gender": profile.get_gender_display() if profile and profile.gender else "Kiritilmagan",
            "birth_date": profile.birth_date.strftime("%Y-%m-%d") if profile and profile.birth_date else "Kiritilmagan",
            "phone_number": profile.phone_number if profile and profile.phone_number else "Kiritilmagan",
            "preferred_genres": preferred_genres,
            "ratings_count": getattr(user, "ratings_count", 0),
            "favorites_count": getattr(user, "favorites_count", 0),
            "watch_history_count": getattr(user, "watch_history_count", 0),
            "ratings_url": f"{reverse('ratings_list')}?user_id={user.id}" if can_open_interactions else "",
            "favorites_url": f"{reverse('favorites_list')}?user_id={user.id}" if can_open_interactions else "",
            "watch_history_url": f"{reverse('watch_history_list')}?user_id={user.id}" if can_open_interactions else "",
        }

    selected_user_summary = lab_user_summaries.get(str(selected_user.id), {})

    context = {
        "form": form,
        "selected_user": selected_user,
        "selected_user_summary": selected_user_summary,
        "result": result,
        "lab_user_summaries": lab_user_summaries,
        "favorite_movie_ids": favorite_movie_ids,
    }
    return render(request, "recommendations/lab.html", context)
