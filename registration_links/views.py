from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from models import RegistrationLink
from django.http import HttpResponseForbidden, HttpResponseNotFound
from django.utils.translation import ugettext as _


def check_registration_link(request, code):
    """If link is correct, set session and redirect to registration view (where session is checked)"""
    reg_link = None
    try:
        reg_link = RegistrationLink.objects.get(code=code)
    except RegistrationLink.DoesNotExist:
        return HttpResponseNotFound(_("Such code does not exist"))
    if not reg_link.active:
        return HttpResponseForbidden(_("Sorry but this code is not valid anymore"))
    elif reg_link.used_times >= reg_link.use_threshold:
        return HttpResponseForbidden(_("Sorry, but this code is not valid anymore"))

    # Update session
    request.session["reg_link"] = reg_link.id
    return redirect(reverse('registration_register'))
