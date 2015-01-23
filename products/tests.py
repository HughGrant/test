from django.test import TestCase
from products.models import Category


class CategoryTests(TestCase):

    def test_auto_create(self):
        result = Category.auto_create(['a', 'b', 'c'])
        c = Category.objects.count()
        self.assertEqual(c, 3)
        self.assertEqual(result.slug_name(), 'a>b>c')

        result = Category.auto_create(['a', 'b', 'd'])
        c = Category.objects.count()
        self.assertEqual(c, 4)
        self.assertEqual(result.slug_name(), 'a>b>d')

        result = Category.auto_create(['a', 'e', 'c'])
        c = Category.objects.count()
        self.assertEqual(c, 6)
        self.assertEqual(result.slug_name(), 'a>e>c')

        result = Category.auto_create(['c', 'b', 'a'])
        c = Category.objects.count()
        self.assertEqual(c, 9)

        p = Category.objects.filter(name='c', parent=None).get()
        p = Category.objects.filter(name='b', parent=p).get()
        name = Category.objects.filter(name='a', parent=p).get().slug_name()
        self.assertEqual(name, 'c>b>a')

        result = Category.auto_create(['a', 'b', 'c', 'd'])
        c = Category.objects.count()
        self.assertEqual(c, 10)

        result = Category.auto_create(['d', 'c', 'b', 'a'])
        c = Category.objects.count()
        self.assertEqual(c, 14)
