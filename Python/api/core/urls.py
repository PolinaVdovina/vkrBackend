from core.auth.urls import urls as auth_urls
from core.Lists.urls import urls as lists_urls
from core.request.urls import urls as request_urls
from core.Analytic.urls import urls as anal_urls

urls = [
    *auth_urls,
    *lists_urls,
    *request_urls,
    *anal_urls
]




