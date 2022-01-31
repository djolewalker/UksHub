from UksHub.apps.events.models import StateChange, UserAssignment


def event_user_to_artefact(creator, artefact, users, removal=False):
    assignment = UserAssignment.objects.create(
        creator=creator, is_removal=removal, artefact=artefact)
    assignment.users.set(users)


def event_artefact_state_change(creator, artefact, state):
    change = StateChange.objects.create(
        creator=creator, artefact=artefact, new_state=state)
