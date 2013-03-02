from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils import simplejson
from django.http import HttpResponse
from django.core.validators import email_re
from django.core.mail import send_mail


def home(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        message = request.POST["message"]
        to_return = {"success": True, "error_fields": {}, "email_failed": False }
        if name == "":
            to_return["success"] = False
            to_return["error_fields"]["name"] = "Please enter your name"
        if message == "":
            to_return["success"] = False
            to_return["error_fields"]["message"] = "Please enter a message"
        if not email_re.match(email):
            to_return["success"] = False
            to_return["error_fields"]["email"] = "Please enter a valid email address"
        if to_return["success"]:
            sent_email = send_mail("New message from coderfly", message, email, ["ramseydsilva@gmail.com"], fail_silently=False)
            if not sent_email:
                to_return["email_failed"] = True
        return HttpResponse(simplejson.dumps(to_return), mimetype="application/json")
    context = {}
    return render_to_response("index.html", context, context_instance = RequestContext(request))
