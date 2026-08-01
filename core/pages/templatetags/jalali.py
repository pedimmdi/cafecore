import jdatetime
from django import template

register = template.Library()

_PERSIAN_DIGITS = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")


@register.filter
def to_jalali(value, fmt="%Y/%m/%d"):
    if not value:
        return "—"
    try:
        if hasattr(value, "hour"):
            jdt = jdatetime.datetime.fromgregorian(datetime=value)
            return jdt.strftime("%Y/%m/%d %H:%M").translate(_PERSIAN_DIGITS)
        jdate = jdatetime.date.fromgregorian(date=value)
        return jdate.strftime(fmt).translate(_PERSIAN_DIGITS)
    except Exception:
        return str(value)


@register.filter
def to_persian(value):
    """تبدیل ارقام انگلیسی به فارسی"""
    if value is None:
        return ""
    return str(value).translate(_PERSIAN_DIGITS)


@register.filter
def persian_price(value):
    """جداکننده سه‌رقمی + ارقام فارسی — مثال: ۲۴۵,۰۰۰"""
    if value is None or value == "":
        return "۰"
    try:
        number = int(float(value))
        formatted = f"{number:,}"
        return formatted.translate(_PERSIAN_DIGITS)
    except (ValueError, TypeError):
        return str(value).translate(_PERSIAN_DIGITS)
