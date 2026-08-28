from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


@login_required
def home(request):
    """Keep the legacy URL pointed at the live administrative dashboard."""
    return redirect("admin_page_one")
