import logging
from django.utils.timezone import now
from django.core.cache import cache
from django.http import JsonResponse

logger = logging.getLogger(__name__)

class IPLoggingAndRateLimitMiddleware:
    """
    Logs IPs, implements simple rate limiting with temporary block.
    """

    # Max requests per period
    MAX_REQUESTS = 20
    PERIOD = 60  # seconds
    BLOCK_TIME = 300  # 5 minutes

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        path = request.path
        timestamp = now()

        # Log request
        logger.info(f"IP {ip} accessed {path} at {timestamp}")

        # Check if IP is blocked
        blocked = cache.get(f"blocked:{ip}")
        if blocked:
            return JsonResponse({"error": "Too many requests. Try again later."}, status=429)

        # Track requests
        request_count = cache.get(f"req_count:{ip}", 0) + 1
        cache.set(f"req_count:{ip}", request_count, timeout=self.PERIOD)

        if request_count > self.MAX_REQUESTS:
            cache.set(f"blocked:{ip}", True, timeout=self.BLOCK_TIME)
            logger.warning(f"IP {ip} temporarily blocked for excessive requests")
            return JsonResponse({"error": f"Too many requests. You are blocked for {self.BLOCK_TIME} seconds."}, status=429)

        return self.get_response(request)
