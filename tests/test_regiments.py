import unittest

from verboselib import drop_language
from verboselib import set_language

from il2fb.commons.air_forces import AIR_FORCES

from il2fb.regiments import Regiment
from il2fb.regiments import Regiments
from il2fb.regiments import RegimentInfoLoader


class RegimentTestCase(unittest.TestCase):

  def tearDown(self):
    drop_language()

  def test_create_regiment(self):
    testee = Regiment(AIR_FORCES.VVS_RKKA, "foo")

    self.assertEqual(testee.air_force, AIR_FORCES.VVS_RKKA)
    self.assertEqual(testee.code_name, "foo")

  def test_unknown_verbose_name(self):
    testee = Regiment(AIR_FORCES.VVS_RKKA, "foo")

    set_language("en")
    self.assertIsNone(testee.verbose_name)

    set_language("ru")
    self.assertIsNone(testee.verbose_name)

    set_language("ja")
    self.assertIsNone(testee.verbose_name)

  def test_valid_verbose_name(self):
    testee = Regiment(AIR_FORCES.VVS_RKKA, "1st_AE_1AR")

    set_language("en")
    self.assertEqual(testee.verbose_name, "OIR AE of 1st AG VVS")

    set_language("ru")
    self.assertEqual(testee.verbose_name, "ОИРАЭ 1-й АГ")

    set_language("ja")
    self.assertEqual(testee.verbose_name, "OIR AE of 1st AG VVS")

  def test_verbose_name_missing_translation(self):
    testee = Regiment(AIR_FORCES.USN, "USN_VT_9B")

    set_language("en")
    self.assertEqual(testee.verbose_name, "VT-9 USS Essex CV-9")

    set_language("ru")
    self.assertEqual(testee.verbose_name, "VT-9 USS Essex CV-9")

    set_language("ja")
    self.assertEqual(testee.verbose_name, "VT-9 USS Essex CV-9")

  def test_unknown_help_text(self):
    testee = Regiment(AIR_FORCES.VVS_RKKA, "foo")

    set_language("en")
    self.assertIsNone(testee.help_text)

    set_language("ru")
    self.assertIsNone(testee.help_text)

    set_language("ja")
    self.assertIsNone(testee.help_text)

  def test_valid_help_text(self):
    testee = Regiment(AIR_FORCES.VVS_RKKA, "1st_AE_1AR")

    set_language("en")
    self.assertEqual(testee.help_text, "OIR AE of 1st AG VVS")

    set_language("ru")
    self.assertEqual(
      testee.help_text,
      (
        "Отдельная Истребительно-Разведываетльния Авиаэскадрилья "
        "1-й Авиагруппы"
      ),
    )  # yes, there are mistakes in word 'Разведываетльния'

    set_language("ja")
    self.assertEqual(testee.help_text, "OIR AE of 1st AG VVS")

  def test_help_text_missing_translation(self):
    testee = Regiment(AIR_FORCES.USN, "USN_VT_9B")

    self.assertEqual(
      testee.help_text,
      "US Navy Torpedo Squadron 9 USS Essex CV-9",
    )

    set_language("en")
    self.assertEqual(
      testee.help_text,
      "US Navy Torpedo Squadron 9 USS Essex CV-9",
    )

    set_language("ru")
    self.assertEqual(
      testee.help_text,
      "US Navy Torpedo Squadron 9 USS Essex CV-9",
    )

    set_language("ja")
    self.assertEqual(
      testee.help_text,
      "US Navy Torpedo Squadron 9 USS Essex CV-9",
    )

  def test_unknown_attributes(self):
    testee = Regiment(AIR_FORCES.USN, "USN_VT_9B")
    self.assertRaises(AttributeError, getattr, testee, 'abracadabra')

  def test_repr(self):
    testee = Regiment(AIR_FORCES.USN, "USN_VT_9B")
    self.assertEqual(repr(testee), "<Regiment 'USN_VT_9B'>")

  def test_to_primitive(self):
    testee = Regiment(AIR_FORCES.USN, "USN_VT_9B")
    primitive = testee.to_primitive()

    self.assertEqual(primitive.pop("code_name"), "USN_VT_9B")
    self.assertEqual(primitive.pop("verbose_name"), "VT-9 USS Essex CV-9")
    self.assertEqual(primitive.pop("help_text"), "US Navy Torpedo Squadron 9 USS Essex CV-9")

    air_force = primitive.pop("air_force")
    self.assertEqual(air_force.pop("name"), "USN")
    self.assertEqual(air_force.pop("default_flight_prefix"), "UN_NN")
    self.assertEqual(air_force.pop("value"), "un")
    self.assertEqual(air_force.pop("verbose_name"), "USN")
    self.assertEqual(air_force.pop("help_text"), "United States Navy")

    country = air_force.pop("country")
    self.assertEqual(country.pop("name"), "US")
    self.assertEqual(country.pop("verbose_name"), "United States")
    self.assertIsNone(country.pop("help_text"))

    self.assertFalse(country)
    self.assertFalse(air_force)
    self.assertFalse(primitive)


class RegimentsTestCase(unittest.TestCase):

  def setUp(self):
    self.regiments = Regiments()

  def test_get_by_code_name(self):
    result = self.regiments.get_by_code_name("1GvIAP")
    self.assertEqual(result.air_force, AIR_FORCES.VVS_RKKA)

  def test_get_by_code_name_is_cached(self):
    regiment1 = self.regiments.get_by_code_name("1GvIAP")
    regiment2 = self.regiments.get_by_code_name("1GvIAP")
    self.assertEqual(id(regiment1), id(regiment2))

  def test_get_by_code_name_invalid(self):
    self.assertRaises(LookupError, self.regiments.get_by_code_name, "foo")

  def test_filter_by_air_force(self):
    regiments = self.regiments.filter_by_air_force(AIR_FORCES.ALA)
    self.assertEqual(len(regiments), 119)

    result = self.regiments.get_by_code_name("NN")
    self.assertEqual(regiments[0], result)

  def test_filter_by_air_force_is_cached(self):
    regiments1 = self.regiments.filter_by_air_force(AIR_FORCES.ALA)
    regiments2 = self.regiments.filter_by_air_force(AIR_FORCES.ALA)

    for regiment1, regiment2 in zip(regiments1, regiments2):
      self.assertEqual(id(regiment1), id(regiment2))
