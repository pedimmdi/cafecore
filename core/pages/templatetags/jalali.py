import jdatetime
from django import template

register = template.Library()


@register.filter
def to_jalali(value, fmt="%Y/%m/%d"):
    if not value:
        return "—"
    try:
        if hasattr(value, "hour"):
            jdt = jdatetime.datetime.fromgregorian(datetime=value)
            return jdt.strftime("%Y/%m/%d %H:%M")
        jdate = jdatetime.date.fromgregorian(date=value)
        return jdate.strftime(fmt)
    except Exception:
        return str(value)
