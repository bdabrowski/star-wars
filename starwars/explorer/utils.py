import concurrent.futures
import os

from django.apps import apps
from django.conf import settings


class EfficientPagination:
    """
    Provides pagination functionality in slicing manner in backends serving html.

    When loading more reaches the limit of MAX_ITEMS the next page's beginning
    will have subtracted one page. This prevents to exceed limit of maximum items per page.
    """
    PER_PAGE = 10
    MAX_ITEMS = 50

    def __init__(self, slice, count):
        self.slice = slice
        self.count = count
        self.start, self.end = self._get_current_range()

    def _get_current_range(self):
        if self.slice:
            start, end = self.slice.split(':')
            return int(start), int(end)
        else:
            return 0, self.PER_PAGE

    @staticmethod
    def _format_param(start, end):
        return ':'.join([str(start), str(end)])

    def has_next(self):
        """
        Return True next page exists.
        """
        return self.count >= self.end

    def get_next_range(self):
        """
        Get range value as string for the next page.
        """
        next_start = self.start
        if (self.end - self.start) >= self.MAX_ITEMS:
            next_start = self.start + self.PER_PAGE
        if self.count < self.end:
            return None
        next_end = self.end + self.PER_PAGE
        return self._format_param(next_start, next_end)

    def has_previous(self):
        """
        Return True if previous page exists.
        """
        return bool(self.start)

    def get_previous_range(self):
        """
        Get range value as string for the next page.
        """
        if not self.start:
            return None
        prev_start = self.start - self.PER_PAGE
        prev_end = self.end - self.PER_PAGE
        return self._format_param(prev_start, prev_end)


def iterate_per_n(sequence, number):
    for idx in range(0, len(sequence), number):
        yield sequence[idx:idx + number]


def run_parallel(inputs, func, n=3):
    """
    Yield output of function per given inputs.
    It maps function to given sequence of inputs staging in N parallel executions at the time.
    """
    for subgroup in iterate_per_n(inputs, n):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(func, item) for item in subgroup]

        results = [future.result() for future in futures]
        for result in results:
            yield result


def get_collection_absolut_path(filename):
    """
    Get absolute filepath to the star wars collection datalake.
    """
    app_config = apps.get_app_config('explorer')
    return os.path.join(settings.BASE_DIR, app_config.COLLECTIONS_PATH, filename)