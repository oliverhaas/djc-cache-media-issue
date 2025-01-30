# Based on clear_cache from
# https://github.com/django-extensions/django-extensions
import logging

from django.conf import settings
from django.core.cache import DEFAULT_CACHE_ALIAS, caches
from django.core.cache.backends.base import InvalidCacheBackendError
from django.core.management.base import BaseCommand, CommandError

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """A simple management command which clears the site-wide cache."""

    help = "Fully clear site-wide cache."

    def add_arguments(self, parser):
        parser.add_argument("--cache", action="append", help="Name of cache to clear")
        parser.add_argument(
            "--all",
            "-a",
            action="store_true",
            default=False,
            dest="all_caches",
            help="Clear all configured caches",
        )

    def handle(self, cache, all_caches, *args, **kwargs):
        if not cache and not all_caches:
            cache = [DEFAULT_CACHE_ALIAS]
        elif cache and all_caches:
            raise CommandError("Using both --all and --cache is not supported")
        elif all_caches:
            cache = getattr(settings, "CACHES", {DEFAULT_CACHE_ALIAS: {}}).keys()

        for key in cache:
            try:
                caches[key].clear()
            except InvalidCacheBackendError:
                logger.error('Cache "%s" is invalid!\n' % key)
            else:
                logger.info('Cache "%s" has been cleared!\n' % key)
