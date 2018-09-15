from django import template
from django.utils.safestring import mark_safe

import bs4

register = template.Library()


@register.filter
def set_attrs(element, attrs):
    # To parse our attrs with BeautifulSoup we have to add any tag
    # to get valid html.
    attrs_soup = bs4.BeautifulSoup("<tag " + attrs + "></tag>")
    element_soup = bs4.BeautifulSoup(str(element))
    for child in element_soup.children:
        # Checking type of child to avoid NavigableString objects
        if isinstance(child, bs4.Tag):
            child.attrs.update(attrs_soup.tag.attrs)
    return mark_safe(str(element_soup))
