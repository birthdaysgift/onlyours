from django.test import TestCase

from ..utils import aligned_range_of_pages


class AlignedRangeOfPagesTest(TestCase):
    def test_left_bound(self):
        """
        tests left bound in range
        1 <2> 3 4 5 6 7 ...
        """
        result = aligned_range_of_pages(
            page=2,
            range_length=7,
            last_page=10
        )
        self.assertEqual(result, range(1, 8))

    def test_middle_no_bounds(self):
        """
        tests middle (no bounds) in range

        ... 2 3 4 <5> 6 7 8 ...
        """
        result = aligned_range_of_pages(
            page=5,
            range_length=7,
            last_page=10
        )
        self.assertEqual(result, range(2, 9))

    def test_right_bound(self):
        """
        tests right bound in range

        ... 4 5 6 <7> 8 9 10
        """
        result = aligned_range_of_pages(
            page=7,
            range_length=7,
            last_page=10
        )
        self.assertEqual(result, range(4, 11))

    def test_page_less_than_one(self):
        """
        if `page` < 1 raises
        ValueError("`page` can't be less than 1")
        """
        self.assertRaisesMessage(
            ValueError,
            "`page` can't be less than 1",
            aligned_range_of_pages,
            page=0,
            range_length=7,
            last_page=10
        )

    def test_page_greater_than_last_page(self):
        """
        if `page` > `last_page` raises
        ValueError("`page` can't be greater than `last_page`")
        """
        self.assertRaisesMessage(
            ValueError,
            "`page` can't be greater than `last_page`",
            aligned_range_of_pages,
            page=11,
            range_length=7,
            last_page=10
        )
