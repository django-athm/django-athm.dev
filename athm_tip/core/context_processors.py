from django.urls import translate_url
from django.utils.translation import get_language


def language_context(request):
    """Provide language-related context to all templates."""
    current_language = get_language()

    # Generate the URL for the alternate language
    alternate_language = "es" if current_language == "en" else "en"
    alternate_url = translate_url(request.path, alternate_language)

    # Preserve query parameters when switching languages
    if request.GET:
        query_string = request.GET.urlencode()
        alternate_url = f"{alternate_url}?{query_string}"

    return {
        "current_language": current_language,
        "alternate_language": alternate_language,
        "alternate_language_name": "Español"
        if alternate_language == "es"
        else "English",
        "alternate_url": alternate_url,
    }
