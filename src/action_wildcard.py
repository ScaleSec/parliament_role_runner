
def check_for_wildcard(policy):
    """
    Checks for wildcards in policy statements
    """
    # Make sure Statement is a list
    if type(policy.policy_json['Statement']) is dict:
        policy.policy_json['Statement'] = [ policy.policy_json['Statement'] ]

    for sid in policy.policy_json['Statement']:
        if 'Action' in sid:
            # Action should be a list for easy iteration
            if type(sid['Action']) is str:
                sid['Action'] = [ sid['Action'] ]

            # Check each action in the list if it has a wildcard, add finding if so.
            for action in sid['Action']:
                if '*' in action:
                    policy.add_finding('Action_Wildcard', location={"action": action})