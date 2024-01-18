from django.shortcuts import render
from django.views import generic

# Create your views here.
class HomePageView(generic.View):
    """
    Basic homepage view.

    """

    def get(self, request):
        """
        Basic Get view for the homepage.

        """
     

        return render(
            request,
            "home.html",
        )

