from django.http import Http404
from django.shortcuts import render


def custom_404_view(request, exception):
    return render(request, "errors/404.html", status=404)


def custom_500_view(request):
    return render(request, "errors/500.html", status=500)


# Local preview uchun
def preview_404(request):
    raise Http404("Preview 404")


def preview_500(request):
    raise Exception("Preview 500")