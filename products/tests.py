from django.test import TestCase
from products.models import Category


class CategoryTests(TestCase):

    def test_auto_create(self):
        Category.auto_create(['a', 'b', 'c'])
        c = Category.objects.count()
        self.assertEqual(c, 3)

        name = Category.objects.filter(name='c').get().slug_name()
        self.assertEqual(name, 'a>b>c')

        Category.auto_create(['a', 'b', 'd'])
        c = Category.objects.count()
        self.assertEqual(c, 4)

        name = Category.objects.filter(name='d').get().slug_name()
        self.assertEqual(name, 'a>b>d')

        Category.auto_create(['a', 'e', 'c'])
        c = Category.objects.count()
        self.assertEqual(c, 6)

        p = Category.objects.filter(name='e').get()
        name = Category.objects.filter(name='c', parent=p).get().slug_name()
        self.assertEqual(name, 'a>e>c')

        Category.auto_create(['c', 'b', 'a'])
        c = Category.objects.count()
        self.assertEqual(c, 9)

        p = Category.objects.filter(name='c', parent=None).get()
        p = Category.objects.filter(name='b', parent=p).get()
        name = Category.objects.filter(name='a', parent=p).get().slug_name()
        self.assertEqual(name, 'c>b>a')

        Category.auto_create(['a', 'b', 'c', 'd'])
        c = Category.objects.count()
        self.assertEqual(c, 10)
        print(Category.objects.filter(name='d').all())