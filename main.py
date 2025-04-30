# main.py (formerly demo.py - refactored with argparse)
import argparse
from app.group import Group
from app.member import Member
from app.colors import bcolors
import random

members = {}
groups = {}

def print_members_and_groups():
    print("\nMembers :", list(members.keys()))
    print("Groups :", list(groups.keys()))
    if groups:
        print("Members of Groups:")
    for group in groups.values():
        print(f"Group {group.id} has members {list(group.members.keys())}")

def run_app(args):
    l, h = args.lower, args.upper
    Member.set_key_range(l, h)
    Group.set_key_range(l, h)

    print("\n************* Welcome *************\n")
    while True:
        print_members_and_groups()
        print(bcolors.BOLD + bcolors.WARNING + "\nPlease select an action:" + bcolors.ENDC)
        print(bcolors.BOLD + bcolors.WARNING + "1. Sign Up as a New Member" + bcolors.ENDC)
        print(bcolors.BOLD + bcolors.WARNING + "2. Log In as an Existing Member" + bcolors.ENDC)
        print(bcolors.BOLD + bcolors.WARNING + "3. Exit" + bcolors.ENDC)

        choice = input("\nEnter your choice of action: ")

        if choice == '1':
            mem_id = len(members) + 1
            m = Member(id=mem_id)
            members[mem_id] = m
            print(f"Member created with member id: {mem_id}")

        elif choice == '2':
            try:
                mem_id = int(input("\nEnter your member ID: "))
                member = members[mem_id]
            except (ValueError, KeyError):
                print(bcolors.ERROR + "Invalid member ID!" + bcolors.ENDC)
                continue

            print(f"\n******** Welcome member {mem_id} ********\n")

            while True:
                print_members_and_groups()
                print(bcolors.BOLD + bcolors.WARNING + "\nActions:" + bcolors.ENDC)
                print("1. Create a new group")
                print("2. Add member to group")
                print("3. Remove member from group")
                print("4. Send message")
                print("5. Read messages")
                print("6. Logout\n")

                option = input("Enter your choice: ")

                if option == '1':
                    if member.group_id:
                        print("You are already in a group!")
                        continue
                    group_id = len(groups) + 1
                    g = Group(id=group_id)
                    g.add_member(member)
                    groups[group_id] = g

                elif option == '2':
                    try:
                        m = int(input("Select member: "))
                        mem = members[m]
                        group = groups[member.group_id]
                        member.add_member_to_group(mem, group)
                    except:
                        print("Error adding member.")

                elif option == '3':
                    try:
                        m = int(input("Select member: "))
                        mem = members[m]
                        group = groups[member.group_id]
                        member.remove_member_from_group(mem, group)
                    except:
                        print("Error removing member.")

                elif option == '4':
                    msg = input("Enter message: ")
                    g = int(input("Target group ID: "))
                    if g in groups:
                        member.add_message_to_group(groups[g], msg)
                        for mem in groups[g].members.values():
                            if g == member.group_id:
                                mem.read_latest_message_of_group(groups[g])
                            else:
                                mem.read_latest_intergroup_message(groups[g])

                elif option == '5':
                    print("Messages:")
                    for m in member.message_history:
                        print(f"\"{m[0]}\" - from {m[1]}")

                elif option == '6':
                    break

        elif choice == '3':
            print("Exiting...")
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cryptography Project")
    parser.add_argument("--lower", "-l", type=int, default=127, help="Lower bound for key size")
    parser.add_argument("--upper", "-h", type=int, default=128, help="Upper bound for key size")
    args = parser.parse_args()
    run_app(args)
