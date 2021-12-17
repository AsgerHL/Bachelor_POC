from time import time, sleep
from random import random

import structlog

logger = structlog.get_logger(__name__)


class Retrier:
    """A Retrier is a helper object used to repeat certain operations when a
    transient exception is raised. A concrete instance of Retrier or of one of
    its subclasses is a stateful object representing a strategy for repeat
    execution."""
    def __init__(self, *exception_set: Exception):
        self._exception_set = tuple(exception_set)

    @property
    def _should_proceed(self):
        """Indicates whether or not the state of this Retrier indicates that
        another attempt should be made."""
        return True

    def _should_retry(self, ex: Exception) -> bool:
        """Examines an exception to determine whether or not it represents a
        transient error."""
        return isinstance(ex, self._exception_set)

    def _before_retry(self, ex: Exception, op):
        """Called after _should_retry has indicated that an exception is
        transient, but before _should_proceed has been called for the next
        attempt. (The operation being executed is made available for the sake
        of debug logging.)

        This is the main hook method of the Retrier class. Subclasses might
        want to extend it to update internal state or to insert a delay."""
        pass

    def run(self, operation, *args, **kwargs):
        """Repeatedly calls operation(*args, **kwargs) until it returns without
        raising a transient error. Returns whatever that function eventually
        returns.

        Subclasses may wish to extend this method to, for example, reset parts
        of their internal state before calling this implementation."""
        while self._should_proceed:
            try:
                return operation(*args, **kwargs)
            except Exception as ex:
                if self._should_retry(ex):
                    self._before_retry(ex, operation)
                    if self._should_proceed:
                        continue
                raise

    def bind(self, operation):
        def _bind(*args, **kwargs):
            return self.run(operation, *args, **kwargs)
        return _bind


class CountingRetrier(Retrier):
    """A CountingRetrier tracks the number of attempts made to call an
    operation, and gives up after a certain number."""
    def __init__(self, *exception_set, max_tries=10, warn_after=6, **kwargs):
        super().__init__(*exception_set, **kwargs)
        self._tries = 0
        self._warn_after = warn_after
        self._max_tries = max_tries

    @property
    def _should_proceed(self):
        return self._max_tries is None or self._tries < self._max_tries

    def _before_retry(self, ex, op):
        self._tries += 1
        if self._warn_after is not None and self._tries >= self._warn_after:
            logger.info(
                "backoff failed, delaying",
                op=str(op),
                iterations=self._tries
            )

    def run(self, operation, *args, **kwargs):
        self._tries = 0
        return super().run(operation, *args, **kwargs)


class SleepingRetrier(CountingRetrier):
    """A SleepingRetrier is a CountingRetrier that also adds a delay after
    each attempt. (This is by default a static delay of one second, but
    subclasses can specify something more sophisticated by overriding the
    _compute_delay method.)"""

    def _compute_delay(self):
        return 1.0

    def _before_retry(self, ex, op):
        super()._before_retry(ex, op)
        # Only bother delaying if there's going to *be* a next attempt
        if self._should_proceed:
            sleep(self._compute_delay())


class ExponentialBackoffRetrier(SleepingRetrier):
    def __init__(self, *exception_set, base=1, ceiling=7, fuzz=0.2, **kwargs):
        super().__init__(*exception_set, **kwargs)
        self._base = base
        self._fuzz = 0
        self._ceiling = ceiling

    def _compute_delay(self):
        max_delay = self._base * (2 ** min(self._tries, self._ceiling) - 1)
        if self._fuzz:
            fuzz_diff = (max_delay * self._fuzz)
            adj = -fuzz_diff + (2 * random() * fuzz_diff)
            max_delay += adj
        return max_delay


DefaultRetrier = ExponentialBackoffRetrier
"""DefaultRetrier is an alias for whichever Retrier the project considers to be
the best choice at any given point. If you just want to retry a function a
reasonable number of times with sensible default behaviour and don't need any
particular tuning parameters, then instantiate one of these."""


class Testing:
    """Helper utilities for testing the Retrier classes."""
    @classmethod
    def requires_k_attempts(cls, k, exception_class):
        """Returns a function that will raise a TryAgain exception k-1 times
        before eventually succeeding."""
        attempts = 0

        def _requires_k_attempts(p, q, *, scale_factor):
            nonlocal attempts
            try:
                if attempts <= k:
                    raise exception_class()
                else:
                    return (p + q) * scale_factor
            finally:
                attempts += 1
        return _requires_k_attempts

    @classmethod
    def requires_k_seconds(cls, k, exception_class):
        """Returns a function that will raise a TryAgain exception unless at
        least k seconds have passed since the last call to it."""
        start = time()

        def _requires_k_seconds(p, q, *, scale_factor):
            nonlocal start
            now = time()
            try:
                if now - start < k:
                    raise exception_class()
                else:
                    return (p + q) * scale_factor
            finally:
                start = now
        return _requires_k_seconds
