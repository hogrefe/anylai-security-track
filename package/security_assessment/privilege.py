from .models import SA02Scenario


ROLE_PERMISSIONS = {
    "buyer": frozenset({"request_quote", "place_order"}),
    "manager": frozenset({"request_quote", "place_order", "approve_large_purchase"}),
    "finance_director": frozenset({"request_quote", "place_order", "approve_large_purchase"}),
}


def is_authorized(scenario: SA02Scenario) -> bool:
    if scenario.action in ROLE_PERMISSIONS.get(scenario.actor_role, frozenset()):
        return True
    delegation = scenario.delegation
    return delegation is not None and delegation.valid and delegation.action == scenario.action
