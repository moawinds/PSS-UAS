from ninja.throttling import BaseThrottle
import time


class SimpleRateThrottle(BaseThrottle):
    rate = 5  # maksimal 5 request
    duration = 60  # dalam 60 detik

    cache = {}

    def get_ident(self, request):
        """Ambil IP address client dari request header."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', '')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', 'unknown')

    def allow_request(self, request):
        ip = self.get_ident(request)
        now = time.time()

        history = self.cache.get(ip, [])

        history = [
            t for t in history
            if now - t < self.duration
        ]

        if len(history) >= self.rate:
            return False

        history.append(now)
        self.cache[ip] = history

        return True