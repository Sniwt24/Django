import datetime
import logging
from django.http import HttpRequest
from django.shortcuts import render

from requestdataapp.views import error_view

log = logging.getLogger(__name__)
def set_useragent_on_req_middleware(get_response):

        def middleware(request: HttpRequest):
            # befor view
            if request.META.get("HTTP_USER_AGENT"):
                request.user_agent = request.META["HTTP_USER_AGENT"]
            else:
                request.user_agent = ""

            # view
            response = get_response(request)

            # after view

            return response

        return middleware


class CountRequestsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exceptions_count = 0
        self.session_ip_rec_list = {}

    def __call__(self, request: HttpRequest):
        # before request

        # Get IP address of request
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            client_ip = request.META['HTTP_X_FORWARDER_FOR']
            client_ip = client_ip.split(",")[0] # Real ip address
        else:
            client_ip = request.META['REMOTE_ADDR'] # Proxi ip address

        # looking for last request and update ip
        if self.session_ip_rec_list.get(client_ip, False):
            if (datetime.datetime.now() - self.session_ip_rec_list.get(client_ip)) < datetime.timedelta(seconds=0.0001):

                # print(f"Request redirect! Too often requests! Try again later!")
                log.info("Request redirect! Too often requests! Try again later!")

                self.session_ip_rec_list[client_ip] = datetime.datetime.now()

                context = {
                    "dsc": f'Too often requests for period from your IP address ({client_ip})',
                }
                return render(request, "requestdataapp/error.html", context)
                # or just raise Exception
                # raise Exception("Too many requests for period!!!")
        self.session_ip_rec_list[client_ip] = datetime.datetime.now()

        # if everything Ok
        # request
        response = self.get_response(request)

        # after request
        # print(f"Request registered from ip {client_ip}")
        log.info("Request registered from ip %s", client_ip)
        return response

    def process_exception(self, request: HttpRequest, exception: Exception):
        self.exceptions_count += 1
        print(self.exceptions_count, "exception(s) registered")
