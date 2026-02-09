class User:
    def __init__(self, username):
        self.username = username
class Admin:
    def access_level(self):
        return "ALL"
class Editor:
    def can_edit(self):
        return True
class AdminEditor(User, Admin, Editor):
    pass  # inherits from all parents


u = AdminEditor("Rozie")
print(u.username)        # from User
print(u.access_level())  # from Admin
print(u.can_edit())      # from Editor
