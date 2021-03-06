from django.test import TestCase
from django.test.client import Client
from django.contrib.messages import get_messages
from classes.CmdHandler import CmdHandler


class EditInfoTests(TestCase):

    def setUp(self):
        self.ui = CmdHandler()

    def test_no_login_get(self):

        client = Client()
        response = client.get('/edit_info/')
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(all_messages[0].tags, "error")
        self.assertEqual(all_messages[0].message, "Please login first.")
        self.assertEqual(response.get('location'), '/login/')

    def test_admin_get(self):

        self.ui.parse_command("setup")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()
        response = client.get('/edit_info/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(len(all_messages), 0)

    def test_super_get(self):

        self.ui.parse_command("setup")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'supervisor'
        session.save()
        response = client.get('/edit_info/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(len(all_messages), 0)

    def test_instructor_get(self):

        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        self.ui.parse_command("create_account instructor@uwm.edu password instructor")
        self.ui.parse_command("logout")
        self.ui.parse_command("login instructor@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'instructor@uwm.edu'
        session['type'] = 'instructor'
        session.save()
        response = client.get('/edit_info/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(len(all_messages), 0)

    def test_ta_get(self):

        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        self.ui.parse_command("create_account ta@uwm.edu password ta")
        self.ui.parse_command("logout")
        self.ui.parse_command("login ta@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta@uwm.edu'
        session['type'] = 'ta'
        session.save()
        response = client.get('/edit_info/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(len(all_messages), 0)

    def test_admin_change_email(self):

        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()
        response = client.post('/edit_info/', data={'email': "admin@uwm.edu", 'password': "", 'name': "",
                                                    'phone': ""}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Email address changed.")

    def test_super_change_email(self):

        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'supervisor'
        session.save()
        response = client.post('/edit_info/', data={'email': "super@uwm.edu", 'password': "", 'name': "",
                                                    'phone': ""}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Email address changed.")

    def test_instructor_change_email(self):

        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        self.ui.parse_command("create_account instructor@uwm.edu password instructor")
        self.ui.parse_command("logout")
        self.ui.parse_command("login instructor@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'instructor@uwm.edu'
        session['type'] = 'instructor'
        session.save()
        response = client.post('/edit_info/', data={'email': "inst@uwm.edu", 'password': "", 'name': "",
                                                    'phone': ""}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Email address changed.")

    def test_ta_change_email(self):

        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        self.ui.parse_command("create_account ta@uwm.edu password ta")
        self.ui.parse_command("logout")
        self.ui.parse_command("login ta@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta@uwm.edu'
        session['type'] = 'ta'
        session.save()
        response = client.post('/edit_info/', data={'email': "tee_ayy@uwm.edu", 'password': "", 'name': "",
                                                    'phone': ""}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Email address changed.")

    def test_bad_email(self):

        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()
        response = client.post('/edit_info/', data={'email': "admin@uwm.com", 'password': "", 'name': "",
                                                    'phone': ""}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Invalid/taken email address.")

    def test_weird_email(self):

        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()
        response = client.post('/edit_info/', data={'email': "admin@uwm.edu@uwm.edu", 'password': "", 'name': "",
                                                    'phone': ""}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Invalid/taken email address.")

    def test_taken_email(self):

        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()
        response = client.post('/edit_info/', data={'email': "ta_assign_super@uwm.edu", 'password': "", 'name': "",
                                                    'phone': ""}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Invalid/taken email address.")

    def test_admin_change_password(self):

        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()
        response = client.post('/edit_info/', data={'email': "", 'password': "new_password", 'name': "",
                                                    'phone': ""}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Password changed.")

    def test_super_change_password(self):

        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'supervisor'
        session.save()
        response = client.post('/edit_info/', data={'email': "", 'password': "new_password", 'name': "",
                                                    'phone': ""}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Password changed.")

    def test_instructor_change_password(self):

        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        self.ui.parse_command("create_account instructor@uwm.edu password instructor")
        self.ui.parse_command("logout")
        self.ui.parse_command("login instructor@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'instructor@uwm.edu'
        session['type'] = 'instructor'
        session.save()
        response = client.post('/edit_info/', data={'email': "", 'password': "new_password", 'name': "",
                                                    'phone': ""}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Password changed.")

    def test_ta_change_password(self):

        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        self.ui.parse_command("create_account ta@uwm.edu password ta")
        self.ui.parse_command("logout")
        self.ui.parse_command("login ta@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta@uwm.edu'
        session['type'] = 'ta'
        session.save()
        response = client.post('/edit_info/', data={'email': "", 'password': "new_password", 'name': "",
                                                    'phone': ""}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Password changed.")

    def test_admin_change_name(self):

        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()
        response = client.post('/edit_info/', data={'email': "", 'password': "", 'name': "Admin",
                                                    'phone': ""}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Name changed.")

    def test_super_change_name(self):

        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'supervisor'
        session.save()
        response = client.post('/edit_info/', data={'email': "", 'password': "", 'name': "Super",
                                                    'phone': ""}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Name changed.")

    def test_instructor_change_name(self):

        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        self.ui.parse_command("create_account instructor@uwm.edu password instructor")
        self.ui.parse_command("logout")
        self.ui.parse_command("login instructor@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'instructor@uwm.edu'
        session['type'] = 'instructor'
        session.save()
        response = client.post('/edit_info/', data={'email': "", 'password': "", 'name': "Instructor",
                                                    'phone': ""}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Name changed.")

    def test_ta_change_name(self):

        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        self.ui.parse_command("create_account ta@uwm.edu password ta")
        self.ui.parse_command("logout")
        self.ui.parse_command("login ta@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta@uwm.edu'
        session['type'] = 'ta'
        session.save()
        response = client.post('/edit_info/', data={'email': "", 'password': "", 'name': "TA",
                                                    'phone': ""}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Name changed.")

    def test_big_name(self):

        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()
        response = client.post('/edit_info/', data={'email': "", 'password': "", 'name': "Jim Joe Bob Henry Bob Bob",
                                                    'phone': ""}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Name changed.")

    def test_admin_change_phone(self):

        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()
        response = client.post('/edit_info/', data={'email': "", 'password': "", 'name': "",
                                                    'phone': "414.867.5309"}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Phone number changed.")

    def test_super_change_phone(self):

        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'supervisor'
        session.save()
        response = client.post('/edit_info/', data={'email': "", 'password': "", 'name': "",
                                                    'phone': "414.867.5309"}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Phone number changed.")

    def test_instructor_change_phone(self):

        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        self.ui.parse_command("create_account instructor@uwm.edu password instructor")
        self.ui.parse_command("logout")
        self.ui.parse_command("login instructor@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'instructor@uwm.edu'
        session['type'] = 'instructor'
        session.save()
        response = client.post('/edit_info/', data={'email': "", 'password': "", 'name': "",
                                                    'phone': "414.867.5309"}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Phone number changed.")

    def test_ta_change_phone(self):

        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_super@uwm.edu password")
        self.ui.parse_command("create_account ta@uwm.edu password ta")
        self.ui.parse_command("logout")
        self.ui.parse_command("login ta@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta@uwm.edu'
        session['type'] = 'ta'
        session.save()
        response = client.post('/edit_info/', data={'email': "", 'password': "", 'name': "",
                                                    'phone': "414.867.5309"}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Phone number changed.")

    def test_bad_phone(self):

        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()
        response = client.post('/edit_info/', data={'email': "", 'password': "", 'name': "",
                                                    'phone': "414-867-5309"}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Invalid phone format.")

    def test_bad_phone_two(self):

        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()
        response = client.post('/edit_info/', data={'email': "", 'password': "", 'name': "",
                                                    'phone': "4148675309"}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "Invalid phone format.")

    def test_nothing(self):

        self.ui.parse_command("setup")
        self.ui.parse_command("login ta_assign_admin@uwm.edu password")
        client = Client()
        session = client.session
        session['email'] = 'ta_assign_admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()
        response = client.post('/edit_info/', data={'email': "", 'password': "", 'name': "",
                                                    'phone': ""}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Info")
        self.assertContains(response, "You should pick something to change.")
