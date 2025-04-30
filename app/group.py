import random
from Polynomials.generate_polynomial import generate_polynomial, gen_intergroup_polynomial
from Polynomials.evaluate_polynomial import evaluate_polynomial
from Cryptography_Utilities.encrypt_polynomial import encrypt_polynomial
from Cryptography_Utilities.decrypt_polynomial import decrypt_polynomial
from app.colors import bcolors

class Group:
    _l = 127  # default
    _h = 128

    @classmethod
    def set_key_range(cls, l, h):
        cls._l = l
        cls._h = h

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.members = {}
        self.secret_keys = []
        self.group_polynomial = None
        self.intergroup_polynomial = None
        self.messages = []
        self.intergroup_messages = []
        self.admin_id = None
        print(f"\nGroup {self.id} ({self.name}) created.")


    def add_member(self, member):
        if member.group_id is not None:
            print(f"\nMember {member.id} already part of Group {member.group_id}")
            return False

        print("\n****** Re-keying Process *******")
        member_key = random.randint(2**self._l, 2**self._h)
        member.set_group_id(self.id)
        member.set_secret_key(member_key)
        self.members[member.id] = member
        self.secret_keys.append(member_key)

        print(f"\n{bcolors.BOLD}{bcolors.OKGREEN}Member {member.id} with key {member_key} added to Group {self.id}.{bcolors.ENDC}")
        if len(self.secret_keys) == 1:
            self.admin_id = member.id
            print(f"{bcolors.BOLD}{bcolors.OKGREEN}Member {member.id} is now the admin of Group {self.id}.{bcolors.ENDC}")

        self.group_polynomial = generate_polynomial(self.secret_keys)
        group_key = evaluate_polynomial(self.group_polynomial, self.secret_keys[0])
        poly = gen_intergroup_polynomial(len(self.secret_keys))
        self.intergroup_polynomial = encrypt_polynomial(poly, group_key)
        print(f"{bcolors.BOLD}{bcolors.OKGREEN}Encrypted Intergroup Polynomial: {self.intergroup_polynomial}{bcolors.ENDC}")
        return True

    def remove_member(self, member_id):
        if member_id not in self.members or member_id == self.admin_id:
            print(f"{bcolors.ERROR}Invalid removal request.{bcolors.ENDC}")
            return False

        print("\n****** Re-keying Process *******")
        member = self.members.pop(member_id)
        member.set_group_id(None)
        self.secret_keys.remove(member.secret_key)

        print(f"{bcolors.BOLD}{bcolors.OKGREEN}Removed Member {member.id} from Group {self.id}.{bcolors.ENDC}")
        self.group_polynomial = generate_polynomial(self.secret_keys)
        group_key = evaluate_polynomial(self.group_polynomial, self.secret_keys[0])
        poly = gen_intergroup_polynomial(len(self.secret_keys))
        self.intergroup_polynomial = encrypt_polynomial(poly, group_key)
        print(f"{bcolors.BOLD}{bcolors.OKGREEN}New Intergroup Polynomial: {self.intergroup_polynomial}{bcolors.ENDC}")
        return True

    def get_group_polynomial(self):
        return self.group_polynomial

    def print_members_list(self):
        print(f"\nGroup {self.id} Members: {list(self.members.keys())}")

    def add_message_to_group(self, message):
        print(f"{bcolors.OKGREEN}Adding encrypted message to Group {self.id}: {message}{bcolors.ENDC}")
        self.messages.append(message)

    def add_intergroup_message(self, message, sender_id):
        print(f"{bcolors.OKGREEN}Inter-group message from {sender_id} added to Group {self.id}{bcolors.ENDC}")
        self.intergroup_messages.append((message, sender_id))

    def request_intergroup_key(self, sender_id):
        group_key = evaluate_polynomial(self.group_polynomial, self.secret_keys[0])
        decrypted = decrypt_polynomial(self.intergroup_polynomial, group_key)
        inter_key = evaluate_polynomial(decrypted, sender_id)
        print(f"{bcolors.OKGREEN}Inter-group key for {sender_id}: {inter_key}{bcolors.ENDC}")
        return inter_key
