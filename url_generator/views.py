from django.shortcuts import render
import functionality
from url_generator.forms import user_form


def index(request):
    if request.method == "POST":
        domain_form = user_form()
        domain_url = request.POST.get("domain")
        data = functionality.get_urls(domain_url)
        return render(request, "index.html", {"form": domain_form, "urls": data})
    else:
        domain_form = user_form()
        return render(request, "index.html", {"form": domain_form})
