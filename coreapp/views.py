from django.shortcuts import render
from django.core.paginator import Paginator
from authUser.models import WishList
from creators.models import Style
from django.views.decorators.cache import cache_page

"""
This view function handles the main page of the application.
It retrieves the published styles from the database, paginates them,
and prepares the context for rendering the index template.

If the user is authenticated, it retrieves the wishlist of the user
and includes the styles in the wishlist in the context.

The function is decorated with @cache_page to cache the response for 3 minutes.
"""
@cache_page(60 * 3)
def index(request):
    """
    Main page view function.

    Args:
        request (HttpRequest): The incoming request object.

    Returns:
        HttpResponse: The rendered index template with the context.
    """
    st = Style.published.all().order_by("-created_at") # Retrieve published styles, order by creation date (newest first)
    page_number = request.GET.get('page', 1) # Get the page number from the request query parameters, default to 1
    st_paginator = Paginator(st, 6) # Create a Paginator object for the styles, with 6 styles per page
    styles = st_paginator.get_page(page_number) # Get the current page of styles

    # If the user is authenticated, retrieve their wishlist and include the styles in the wishlist in the context
    if request.user.is_authenticated:
        wishl = WishList.objects.filter(user=request.user).first()
        sty = wishl.members.all() if wishl else None
    else:
        sty = None

    context = {"styles": styles, "sty": sty} # Prepare the context for rendering the index template
    return render(request, 'core/index.html', context) # Render the index template with the context and return the response
