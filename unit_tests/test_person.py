# created by Grant

from django.test import TestCase
from classes.Person import Person
from ta_assign import models


class TestPerson(TestCase):

    def test_init_(self):
        self.person1 = Person("person1@uwm.edu", "DEFAULT_PASSWORD", "DEFAULT")
        self.assertEquals(self.person1.email, "person1@uwm.edu")
        self.assertEquals(self.person1.password, "DEFAULT_PASSWORD")

    def test_change_password(self):
        self.person1 = Person("person1@uwm.edu", "DEFAULT_PASSWORD", "DEFAULT")
        self.assertTrue(self.person1.change_password("password"))
        self.assertEquals(self.person1.password, "password")
        self.assertNotEquals(self.person1.password, "DEFAULT_PASSWORD")
        model_person1 = models.ModelPerson.objects.get(email=self.person1.email)
        self.assertEquals(model_person1.password, "password")

    def test_change_email(self):
        self.person1 = Person("person1@uwm.edu", "DEFAULT_PASSWORD", "DEFAULT")
        self.person2 = Person("goober@uwm.edu", "DEFAULT_PASSWORD", "DEFAULT")
        self.person1.change_email("snoop@uwm.edu")
        self.assertEquals(self.person1.email, "snoop@uwm.edu")
        self.assertNotEquals(self.person1.email, "person1@uwm.edu")
        model_person1 = models.ModelPerson.objects.get(email=self.person1.email)
        self.assertEquals(model_person1.email, "snoop@uwm.edu")
        self.assertFalse(self.person1.change_email("snoop@gmail.com"))
        self.assertFalse(self.person1.change_email("no_at_symbol_or_dot_something"))
        self.assertFalse(self.person1.change_email("goober@uwm.edu"))

    def test_change_phone(self):
        self.person1 = Person("person1@uwm.edu", "DEFAULT_PASSWORD", "DEFAULT")
        self.person1.change_phone("414.414.4141")
        model_person1 = models.ModelPerson.objects.get(email=self.person1.email)
        self.assertEquals(model_person1.phone, "414.414.4141")
        self.assertEquals(self.person1.phone_number, "414.414.4141")
        self.assertNotEquals(self.person1.phone_number, "000.000.0000")
        self.assertFalse(self.person1.change_phone("1234567890"))
        self.assertFalse(self.person1.change_phone("414-414-4141"))
        self.assertFalse(self.person1.change_phone("(414)414-4141"))
        self.assertFalse(self.person1.change_phone("abc.abc.abcd"))
        self.assertFalse(self.person1.change_phone("1234.1234.1234"))

    def test_change_name(self):
        self.person1 = Person("person1@uwm.edu", "DEFAULT_PASSWORD", "DEFAULT")
        self.person1.change_name("Snoop Doggy Dog")
        model_person1 = models.ModelPerson.objects.get(email=self.person1.email)
        self.assertEquals(model_person1.name, "Snoop Doggy Dog")
        self.assertEquals(self.person1.name, "Snoop Doggy Dog")
        self.assertNotEquals(self.person1.name, "DEFAULT")

    def test_get_contact_info(self):
        self.person1 = Person("person1@uwm.edu", "DEFAULT_PASSWORD", "DEFAULT")
        self.assertEquals(self.person1.get_contact_info(), "Snoop Doggy Dog, snoop@uwm.edu, 4144244343")
        self.assertNotEquals(self.person1.get_contact_info(), "DEFAULT, person1@uwm.edu, 0000000000")

    def test_login(self):
        self.person1 = Person("person1@uwm.edu", "DEFAULT_PASSWORD", "DEFAULT")
        self.person2 = Person("person2@uwm.edu", "DEFAULT_PASSWORD", "DEFAULT")
        self.assertEquals(Person.login("snoop@uwm.edu", "password"), "Invalid login info")
        self.assertEquals(Person.login("person1@uwm.edu", "DEFAULT_PASSWORD"), "Login successful")
        model_person1 = models.ModelPerson.objects.get(email=self.person1.email)
        self.assertTrue(model_person1.isLoggedOn)
        self.assertEquals(Person.login("person1@uwm.edu", "DEFAULT_PASSWORD"), "User already logged in")
        self.assertEquals(Person.login("person2@uwm.edu", "DEFAULT_PASSWORD"), "User already logged in")

    def test_logout(self):
        self.person1 = Person("person1@uwm.edu", "DEFAULT_PASSWORD", "DEFAULT")
        self.person2 = Person("person2@uwm.edu", "DEFAULT_PASSWORD", "DEFAULT")
        self.assertEquals(Person.login("person1@uwm.edu", "DEFAULT_PASSWORD"), "Login successful")
        self.assertEquals(Person.login("person2@uwm.edu", "DEFAULT_PASSWORD"), "User already logged in")
        self.assertTrue(self.person1.logout())

    def test_view_info(self):
        self.person1 = Person("person1@uwm.edu", "DEFAULT_PASSWORD", "DEFAULT")
        self.person2 = Person("person2@uwm.edu", "DEFAULT_PASSWORD", "DEFAULT")
        self.assertEquals(self.person1.view_info(), ["person1@uwm.edu", "DEFAULT_PASSWORD", "DEFAULT", "000.000.0000"])
        self.assertEquals(self.person2.view_info(), ["person2@uwm.edu", "DEFAULT_PASSWORD", "DEFAULT", "000.000.0000"])
