from django import template

register = template.Library()


@register.filter
def format_runtime(value):
    if value in (None, "", 0):
        return ""

    try:
        total_minutes = int(value)
    except (TypeError, ValueError):
        return value

    hours = total_minutes // 60
    minutes = total_minutes % 60

    if hours > 0 and minutes > 0:
        return f"{hours} soat {minutes} min"
    if hours > 0:
        return f"{hours} soat"
    return f"{minutes} min"