"""Run Parliament on a role
Usage:
    analyze_role --rolename <rolename> --profile <profile>

Options:
    -h --help                               Show this screen.
    --version                               Show version.
    --rolename rolename                     Name of role to check.
    --profile profile                       AWS Profile name.

Examples:
    analyze_role --rolename my-aws-role --profile my-aws-profile
"""

import boto3
import json
from parliament import Policy
from docopt import docopt
from action_wildcard import check_for_wildcard

def get_policies_for_role(rolename, iam):
    all_policies = {}
    
    # two possible types of policies - inline and managed
    inline_policies = iam.list_role_policies(RoleName=rolename)['PolicyNames']
    attached_policies = iam.list_attached_role_policies(RoleName=rolename)['AttachedPolicies']

    # Get each inline policy
    for policy in inline_policies:
        all_policies[policy] = iam.get_role_policy(
            RoleName=rolename,
            PolicyName=policy)['PolicyDocument']
    
    # Get the default VersionId, then use that to retrieve that version of the policy.
    for policy in attached_policies:
        policy_version = iam.get_policy(
            PolicyArn=policy['PolicyArn']
        )['Policy']['DefaultVersionId']

        all_policies[policy['PolicyArn']] = iam.get_policy_version(
            PolicyArn=policy['PolicyArn'],
            VersionId=policy_version
            )['PolicyVersion']['Document']

    return all_policies

def run_parliament(policy_json, policy_name):
    policy = Policy(policy_json)
    policy.analyze()
    check_for_wildcard(policy)
    
    # Assign finding details
    findings = [
        {
        "issue": finding.issue,
        "title": finding.title,
        "severity": finding.severity,
        "description": finding.description,
        "detail": finding.detail,
        "location": finding.location,
        "policy_name": policy_name
        }
        for finding in policy.findings
    ]

    # Deduplicate the findings for easy output
    deduped_findings = []
    for f in findings:
        if f not in deduped_findings:
            deduped_findings.append(f)

    return deduped_findings

def check_role(**arguments):
    session = boto3.Session(profile_name=arguments['profile'])
    iam = session.client('iam')

    policies = get_policies_for_role(arguments['rolename'], iam)
    all_findings = [ finding for policy_name,policy_json in policies.items() for finding in run_parliament(policy_json, policy_name) if finding != [] ]

    print(json.dumps(all_findings, indent=2))

def main():
    arguments = {
        k.lstrip('-'): v for k, v in docopt(__doc__, version='Parliament Role Runner v0.01').items()
    }
    check_role(**arguments)

if __name__ == '__main__':
    main()