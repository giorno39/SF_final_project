"""Self-contained settings for running the test suite.

Run with:

    python manage.py test tests --settings=final_project.test_settings

It reuses the normal project settings but swaps every external dependency
(PostgreSQL, the Redis channel layer, SMTP e-mail) for in-process equivalents,
so the tests run anywhere with no services to start.

A custom test runner also defaults test discovery to the project's
``*_test.py`` naming convention, so the ``--pattern`` flag is optional.
"""
from django.test.runner import DiscoverRunner

from final_project.settings import *  # noqa: F401,F403


class PatternTestRunner(DiscoverRunner):
    """DiscoverRunner that finds ``*_test.py`` files by default."""

    def __init__(self, *args, pattern=None, **kwargs):
        if not pattern or pattern == "test*.py":
            pattern = "*_test.py"
        super().__init__(*args, pattern=pattern, **kwargs)


TEST_RUNNER = "final_project.test_settings.PatternTestRunner"

# Fast, isolated, in-memory database - no PostgreSQL required.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# Channels without Redis.
CHANNEL_LAYERS = {
    "default": {"BACKEND": "channels.layers.InMemoryChannelLayer"},
}

# Capture e-mails in memory instead of sending them.
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# Speed up password hashing during tests.
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# Serve URLs under a supported language prefix.
LANGUAGE_CODE = "en"

# Write any uploaded media to a throwaway temp directory.
import tempfile  # noqa: E402

MEDIA_ROOT = tempfile.mkdtemp(prefix="test_media_")

#execute unit test command
#python manage.py test tests --settings=final_project.test_settings