from django import template
import re

register = template.Library()

@register.simple_tag
def device_is_mobile(request):
    try:
        MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)", re.IGNORECASE)
        return True if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']) else False
    except:
        return False