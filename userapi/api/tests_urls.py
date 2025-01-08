from django.test import TestCase, Client

class urlsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = {"name" : "test", "mail": "test@gmail.com", "age": 20, "profession": "test"}
        self.user2 = {"name" : "test", "mail": "test@gmailcom.", "age": 20, "profession": "test"}
        self.user3 = {"name" : "test", "mail": "test2@gmail.com", "age": 800, "profession": "test"}
        self.user1 = {"name" : "test", "mail": "test@gmail.com", "age": 20, "profession": "test"}

    def create_user(self):
        response = self.client.post("/api/users/", self.user1)
        self.assertEqual(response.status_code, 201)

    def invalid_mail(self):
        response = self.client.post("/api/users/", self.user2)
        self.assertEqual(response.status_code, 400)
    
    def invalid_age(self):
        response = self.client.post("/api/users/", self.user3)
        self.assertEqual(response.status_code, 400)

    def duplicated_mail(self):
        response = self.client.post("/api/users/", self.user3)
        self.assertEqual(response.status_code, 400)

    def get_user(self):
        response = self.client.get("/api/users/")
        self.assertEqual(response.status_code, 200)
    
    def update_user(self):
        response = self.client.put("/api/users/?id=1", {"name": "loic"}, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "loic")

    def delete_user(self):
        response = self.client.delete("/api/users/?id=1")
        self.assertEqual(response.status_code, 204)

    
    def no_user(self):
        response = self.client.get("/api/users/?id=1")
        self.assertEqual(response.status_code, 404)
    

    def test_all(self):
        self.create_user()
        self.invalid_mail()
        self.invalid_age()
        self.duplicated_mail()
        self.get_user()
        self.update_user()
        self.delete_user()
        self.no_user()