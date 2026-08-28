"""Render the authenticated shelter selection screen."""

from urllib.parse import urlencode

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


@login_required
def mainscreen(request):
    shelter = request.GET.get("shelter", "")
    if shelter == "whiteflag":
        return redirect("whiteflag")
    if shelter in {"mens", "womens", "diversion"}:
        return redirect(f'/shelters/?{urlencode({"shelter": shelter})}')
    return render(request, "mainscreen/mainscreen.html")
