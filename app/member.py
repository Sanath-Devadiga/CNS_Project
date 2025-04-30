from Cryptography_Utilities.encode import encode
from Cryptography_Utilities.encrypt import encrypt
from Cryptography_Utilities.decode import decode
from Cryptography_Utilities.decrypt import decrypt
from Polynomials.evaluate_polynomial import evaluate_polynomial
from Cryptography_Utilities.decrypt_polynomial import decrypt_polynomial
from app.colors import bcolors

class Member:
    _l = 127
    _h = 128

    @classmethod
    def set_key_range(cls, l, h):
        cls._l = l
        cls._h = h

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.secret_key = None
        self.group_id = None
        self.message_history = []
        print(f"Member {self.id} ({self.name}) created.")


    def set_group_id(self, group_id):
        self.group_id = group_id

    def set_secret_key(self, key):
        self.secret_key = key

    def add_message_to_group(self, group, message):
        if self.group_id != group.id:
            print(f"Sending inter-group message from {self.id} to Group {group.id}: {message}")
            key = group.request_intergroup_key(self.id)
            encoded_key = bin(key)[2:]
            encrypted = encrypt(encode(message), encoded_key)
            group.add_intergroup_message(encrypted, self.id)
            print("Message sent successfully.")
        else:
            print(f"{bcolors.WARNING}Sending intra-group message from {self.id} to Group {group.id}: {message}{bcolors.ENDC}")
            poly = group.get_group_polynomial()
            group_key = evaluate_polynomial(poly, self.secret_key)
            encoded_key = bin(group_key)[2:]
            encrypted = encrypt(encode(message), encoded_key)
            group.add_message_to_group(encrypted)
            print("Message added to the group.")
        return True

    def read_latest_message_of_group(self, group):
        if self.group_id != group.id or not group.messages:
            print(f"{bcolors.ERROR}Cannot read group {group.id} messages.{bcolors.ENDC}")
            return False

        poly = group.get_group_polynomial()
        group_key = evaluate_polynomial(poly, self.secret_key)
        encoded_key = bin(group_key)[2:]
        decrypted = decrypt(group.messages[-1], encoded_key)
        decoded = decode(decrypted)
        print(f"{bcolors.OKGREEN}Member {self.id} read: {decoded}{bcolors.ENDC}")
        self.message_history.append((decoded, "Intra-Group"))
        return True

    def read_latest_intergroup_message(self, group):
        if self.group_id != group.id or not group.intergroup_messages:
            print(f"{bcolors.ERROR}No intergroup messages for group {group.id}.{bcolors.ENDC}")
            return False

        enc_msg, sender_id = group.intergroup_messages[-1]
        poly = group.get_group_polynomial()
        group_key = evaluate_polynomial(poly, self.secret_key)
        inter_poly = decrypt_polynomial(group.intergroup_polynomial, group_key)
        key = evaluate_polynomial(inter_poly, sender_id)
        encoded_key = bin(key)[2:]
        decrypted = decrypt(enc_msg, encoded_key)
        decoded = decode(decrypted)
        print(f"{bcolors.OKGREEN}Member {self.id} read from {sender_id}: {decoded}{bcolors.ENDC}")
        self.message_history.append((decoded, sender_id))
        return True

    def add_member_to_group(self, member, group):
        if self.id != group.admin_id:
            print("Only group admin can add members.")
            return False
        return group.add_member(member)

    def remove_member_from_group(self, member, group):
        if self.id != group.admin_id:
            print("Only group admin can remove members.")
            return False
        return group.remove_member(member.id)
