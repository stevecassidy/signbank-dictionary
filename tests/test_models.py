from django.test import TestCase

from dictionary.models import Keyword, Gloss, Translation, Dialect, Region

class TestKeyword(TestCase):
    fixtures = ["test_data.json"]

    def test_str_method(self):
        keyword = Keyword.objects.get(pk=1)
        self.assertEqual(str(keyword), keyword.text)


class TestTranslation(TestCase):
    fixtures = ["test_data.json"]

    def test_str_method(self):
        translation = Translation.objects.get(pk=1)
        string_of_translation = "%s-%s-%s"%(translation.gloss.sn,
            translation.gloss.idgloss, translation.translation.text)
        self.assertEqual(str(translation), string_of_translation)

    def test_ordering(self):
        """Ordering of translations for a keyword should be
        ordered by the dialect of the gloss"""

        g1, g2, g3 = Gloss.objects.all()[:3]
        # add regions for each gloss
        auswide = Dialect.objects.get(name="Australia Wide")
        north = Dialect.objects.get(name="Northern Dialect")
        nsw = Dialect.objects.get(name="New South Wales")

        r1 = Region.objects.create(gloss=g1, dialect=nsw)
        r2 = Region.objects.create(gloss=g2, dialect=auswide)
        r3 = Region.objects.create(gloss=g3, dialect=north)

        # all three are translations of the same keyword
        kw = Keyword.objects.create(text="testkeyword")
        tr2 = Translation.objects.create(translation=kw, gloss=g2, index=1)
        tr1 = Translation.objects.create(translation=kw, gloss=g1, index=1)
        tr3 = Translation.objects.create(translation=kw, gloss=g3, index=1)

        # now find the translations of our keyword
        trans = kw.translation_set.all()

        # should be three of them
        self.assertEqual(3, trans.count())
        # order should be g2, g3, g1 (Auswide > Northern > NSW)
        self.assertEqual(g2, trans[0].gloss)
        self.assertEqual(g3, trans[1].gloss)
        self.assertEqual(g1, trans[2].gloss)

        tr, length = kw.match_request(1, searchall=True, safe=False)
        self.assertEqual(3, length)
        self.assertEqual(g2, tr.gloss)

        # now prefer the nsw dialect
        tr, length = kw.match_request(1, searchall=True, safe=False, preferdialect=nsw)
        self.assertEqual(3, length)
        self.assertEqual(g1, tr.gloss)


class TestGloss(TestCase):
    fixtures = ["test_data.json"]

    def test_str_method(self):
        gloss = Gloss.objects.get(sn=1)
        self.assertTrue(str(gloss), '%s-%s'%(gloss.sn, gloss.idgloss))
