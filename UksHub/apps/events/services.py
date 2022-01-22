from UksHub.apps.events.models import UserAssignment


def event_user_to_artefact(creator, artefact, users, removal=False):
    assignment = UserAssignment.objects.create(creator=creator, is_removal=removal, artefact=artefact)
    assignment.users.set(users)