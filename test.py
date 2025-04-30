from app.group import Group
from app.member import Member

# Set key range globally
Group.set_key_range(127, 128)
Member.set_key_range(127, 128)

# Create a group
g = Group(id=1)

# Create members
admin = Member(id=0)
member1 = Member(id=1)
member2 = Member(id=2)
member3 = Member(id=3)

# Admin creates the group
g.add_member(admin)

# Admin adds other members
admin.add_member_to_group(member1, g)
admin.add_member_to_group(member2, g)

# Unauthorized member tries to add — should fail
member1.add_member_to_group(member3, g)

# Admin removes a member
admin.remove_member_from_group(member2, g)

# Unauthorized member tries to remove — should fail
member1.remove_member_from_group(admin, g)

# Admin tries to remove self — should fail
admin.remove_member_from_group(admin, g)

# Show members in group
g.print_members_list()

# Send and read an intra-group message
msg1 = "Attack at midnight"
member1.add_message_to_group(g, msg1)
admin.read_latest_message_of_group(g)

# Member not in group tries to read — should fail
member3.read_latest_message_of_group(g)

# Inter-group communication test
msg2 = "Don't attack"
member3.add_message_to_group(g, msg2)
member1.read_latest_intergroup_message(g)
