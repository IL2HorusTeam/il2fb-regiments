# coding: utf-8
from __future__ import unicode_literals

import unittest

from verboselib import use_language, drop_language

from il2fb.commons.organization import AirForces

from il2fb.regiments import Regiment, Regiments


class RegimentTestCase(unittest.TestCase):

    def tearDown(self):
        drop_language()

    def test_create_regiment(self):
        testee = Regiment(AirForces.vvs_rkka, 'foo')
        self.assertEqual(testee.air_force, AirForces.vvs_rkka)
        self.assertEqual(testee.code_name, 'foo')

    def test_unknown_verbose_name(self):
        testee = Regiment(AirForces.vvs_rkka, 'foo')

        use_language('en')
        self.assertEqual(testee.verbose_name, "")

        use_language('ru')
        self.assertEqual(testee.verbose_name, "")

        use_language('ja')
        self.assertEqual(testee.verbose_name, "")

    def test_valid_verbose_name(self):
        testee = Regiment(AirForces.vvs_rkka, '1st_AE_1AR')

        use_language('en')
        self.assertEqual(testee.verbose_name, "OIR AE of 1st AG VVS")

        use_language('ru')
        self.assertEqual(testee.verbose_name, "ОИРАЭ 1-й АГ")

        use_language('ja')
        self.assertEqual(testee.verbose_name, "OIR AE of 1st AG VVS")

    def test_verbose_name_missing_translation(self):
        testee = Regiment(AirForces.usn, 'USN_VT_9B')

        use_language('en')
        self.assertEqual(testee.verbose_name, "VT-9 USS Essex CV-9")

        use_language('ru')
        self.assertEqual(testee.verbose_name, "VT-9 USS Essex CV-9")

        use_language('ja')
        self.assertEqual(testee.verbose_name, "VT-9 USS Essex CV-9")

    def test_unknown_help_text(self):
        testee = Regiment(AirForces.vvs_rkka, 'foo')

        use_language('en')
        self.assertEqual(testee.help_text, "")

        use_language('ru')
        self.assertEqual(testee.help_text, "")

        use_language('ja')
        self.assertEqual(testee.help_text, "")

    def test_valid_help_text(self):
        testee = Regiment(AirForces.vvs_rkka, '1st_AE_1AR')

        use_language('en')
        self.assertEqual(testee.help_text, "OIR AE of 1st AG VVS")

        use_language('ru')
        self.assertEqual(
            testee.help_text,
            "Отдельная Истребительно-Разведываетльния Авиаэскадрилья "
            "1-й Авиагруппы"
        )  # yes, there are mistakes in word 'Разведываетльния'

        use_language('ja')
        self.assertEqual(testee.help_text, "OIR AE of 1st AG VVS")

    def test_help_text_missing_translation(self):
        testee = Regiment(AirForces.usn, 'USN_VT_9B')

        self.assertEqual(
            testee.help_text,
            "US Navy Torpedo Squadron 9 USS Essex CV-9",
        )

        use_language('en')
        self.assertEqual(
            testee.help_text,
            "US Navy Torpedo Squadron 9 USS Essex CV-9",
        )

        use_language('ru')
        self.assertEqual(
            testee.help_text,
            "US Navy Torpedo Squadron 9 USS Essex CV-9",
        )

        use_language('ja')
        self.assertEqual(
            testee.help_text,
            "US Navy Torpedo Squadron 9 USS Essex CV-9",
        )

    def test_unknown_attributes(self):
        testee = Regiment(AirForces.usn, 'USN_VT_9B')
        self.assertRaises(AttributeError, getattr, testee, 'abracadabra')

    def test_repr(self):
        testee = Regiment(AirForces.usn, 'USN_VT_9B')
        self.assertEqual(repr(testee), "<Regiment 'USN_VT_9B'>")

    def test_to_primitive(self):
        primitive = Regiment(AirForces.usn, 'USN_VT_9B').to_primitive()

        self.assertEqual(primitive.pop('code_name'), "USN_VT_9B")
        self.assertEqual(primitive.pop('verbose_name'), "VT-9 USS Essex CV-9")
        self.assertEqual(primitive.pop('help_text'), "US Navy Torpedo Squadron 9 USS Essex CV-9")

        air_force = primitive.pop('air_force')
        self.assertEqual(air_force.pop('name'), "usn")
        self.assertEqual(air_force.pop('default_flight_prefix'), "UN_NN")
        self.assertEqual(air_force.pop('value'), "un")
        self.assertEqual(air_force.pop('verbose_name'), "USN")
        self.assertEqual(air_force.pop('help_text'), "United States Navy")

        country = air_force.pop('country')
        self.assertEqual(country.pop('name'), "us")
        self.assertEqual(country.pop('verbose_name'), "United States")
        self.assertIsNone(country.pop('help_text'))

        belligerent = country.pop('belligerent')
        self.assertEqual(belligerent.pop('name'), "red")
        self.assertEqual(belligerent.pop('verbose_name'), "allies")
        self.assertIsNone(belligerent.pop('help_text'))
        self.assertEqual(belligerent.pop('value'), 1)

        self.assertFalse(belligerent)
        self.assertFalse(country)
        self.assertFalse(air_force)
        self.assertFalse(primitive)


class RegimentsTestCase(unittest.TestCase):

    def test_create_regiments(self):

        def create():
            Regiments()

        self.assertRaises(TypeError, create)

    def test_get_by_code_name(self):
        result = Regiments.get_by_code_name('1GvIAP')
        self.assertEqual(result.air_force, AirForces.vvs_rkka)

    def test_get_by_code_name_is_cached(self):
        regiment1 = Regiments.get_by_code_name('1GvIAP')
        regiment2 = Regiments.get_by_code_name('1GvIAP')
        self.assertEqual(id(regiment1), id(regiment2))

    def test_get_by_code_name_invalid(self):
        self.assertRaises(ValueError, Regiments.get_by_code_name, 'foo')

    def test_filter_by_air_force(self):
        regiments = Regiments.filter_by_air_force(AirForces.ala)
        self.assertEquals(len(regiments), 1)

        result = Regiments.get_by_code_name('NN')
        self.assertEquals(regiments[0], result)

    def test_filter_by_air_force_is_cached(self):
        regiments1 = Regiments.filter_by_air_force(AirForces.ala)
        regiments2 = Regiments.filter_by_air_force(AirForces.ala)

        for regiment1, regiment2 in zip(regiments1, regiments2):
            self.assertEqual(id(regiment1), id(regiment2))
