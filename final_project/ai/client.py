from django.conf import settings
from openai import OpenAI


OPENAI_AVAILABLE = bool(settings.OPENAI_API_KEY)


def is_openai_available():
    return OPENAI_AVAILABLE


def get_openai_client():
    if not OPENAI_AVAILABLE:
        return None

    return OpenAI(api_key=settings.OPENAI_API_KEY)