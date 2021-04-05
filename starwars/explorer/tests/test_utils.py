import unittest

from explorer.utils import iterate_per_n, EfficientPagination


class TestCase(unittest.TestCase):

    def test_iterate_per_n(self):
        chunks = list(iterate_per_n([1, 2, 3, 4, 5, 6], 2))
        self.assertEqual(chunks[0], [1, 2])
        self.assertEqual(chunks[1], [3, 4])
        self.assertEqual(chunks[2], [5, 6])

        chunks = list(iterate_per_n([1, 2, 3, 4, 5, 6, 7], 3))
        self.assertEqual(chunks[0], [1, 2, 3])
        self.assertEqual(chunks[1], [4, 5, 6])
        self.assertEqual(chunks[2], [7])

    def test_pagination(self):
        paginator = EfficientPagination('0:10', 82)
        self.assertEqual(paginator.start, 0)
        self.assertEqual(paginator.end, 10)
        self.assertFalse(paginator.has_previous())
        self.assertTrue(paginator.has_next())
        self.assertEqual(paginator.get_next_range(), '0:20')
        paginator = EfficientPagination('0:20', 82)
        self.assertTrue(paginator.has_next())
        self.assertEqual(paginator.get_next_range(), '0:30')
        paginator = EfficientPagination('0:30', 82)
        self.assertTrue(paginator.has_next())
        self.assertEqual(paginator.get_next_range(), '0:40')
        paginator = EfficientPagination('0:40', 82)
        self.assertTrue(paginator.has_next())
        self.assertEqual(paginator.get_next_range(), '0:50')
        paginator = EfficientPagination('0:50', 82)
        self.assertTrue(paginator.has_next())
        self.assertEqual(paginator.get_next_range(), '10:60')
        paginator = EfficientPagination('10:60', 82)
        self.assertTrue(paginator.has_next())
        self.assertEqual(paginator.get_next_range(), '20:70')
        paginator = EfficientPagination('20:70', 82)
        self.assertTrue(paginator.has_next())
        self.assertEqual(paginator.get_next_range(), '30:80')
        paginator = EfficientPagination('30:80', 82)
        self.assertTrue(paginator.has_next())
        self.assertEqual(paginator.get_next_range(), '40:90')
        paginator = EfficientPagination('40:90', 82)
        self.assertFalse(paginator.has_next())
        self.assertTrue(paginator.has_previous())
        self.assertEqual(paginator.get_previous_range(), '30:80')
        paginator = EfficientPagination('30:80', 82)
        self.assertTrue(paginator.has_previous())
        self.assertEqual(paginator.get_previous_range(), '20:70')
        paginator = EfficientPagination('20:70', 82)
        self.assertTrue(paginator.has_previous())
        self.assertEqual(paginator.get_previous_range(), '10:60')
        paginator = EfficientPagination('10:60', 82)
        self.assertTrue(paginator.has_previous())
        self.assertEqual(paginator.get_previous_range(), '0:50')
        paginator = EfficientPagination('0:50', 82)
        self.assertFalse(paginator.has_previous())
