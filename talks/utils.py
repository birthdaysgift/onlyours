import math


def aligned_range_of_pages(page=1, range_length=5, last_page=10):
    if page < 1:
        raise ValueError("`page` can't be less than 1")
    if page > last_page:
        raise ValueError("`page` can't be greater than `last_page`")
    middle = math.ceil(range_length / 2)
    delta = range_length - middle
    if page > last_page:
        raise[]
    if last_page <= range_length:
        a = 1
        b = last_page
    elif page <= middle:
        a = 1
        b = range_length
    elif page >= last_page - delta:
        a = last_page - range_length + 1
        b = last_page
    else:
        a = page - delta
        b = page + delta
    return range(a, b+1)
