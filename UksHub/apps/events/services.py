from UksHub.apps.events.models import MilestoneAssignment, StateChange, UserAssignment


def event_user_to_artefact(creator, artefact, users, removal=False):
    assignment = UserAssignment.objects.create(
        creator=creator, is_removal=removal, artefact=artefact)
    assignment.users.set(users)


def event_artefact_state_change(creator, artefact, state):
    StateChange.objects.create(
        creator=creator, artefact=artefact, new_state=state)


def event_artefact_to_milestone(creator, artefact, milestone):
    MilestoneAssignment.objects.create(
        creator=creator, artefact=artefact, milestone=milestone)
