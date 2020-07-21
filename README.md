# parliament_role_runner

See the [blog post](https://scalesec.com/aws-series/analyzing-iam-policies-at-scale-with-parliament/) for more info.

This is a script to run [Parliament](https://github.com/duo-labs/parliament/) on an IAM role to lint and analyze all of it's attached policies for misconfigurations. 


## Usage:
Create your virtual environment and install requirements:
```
python3 -m venv my_venv
source my_venv/bin/activate
pip3 install -U git+https://github.com/ScaleSec/parliament_role_runner.git
```

Run with:
```
analyze_role --rolename <rolename> --profile <profile>
```


## Output Example
Given a policy on the role:
```
{
    "Statement": [
        {
            "Sid": "ElasticComputeCloudFull",
            "Action": [
                "ec2:*"
            ],
            "Effect": "Allow",
            "Resource": [
                "*"
            ]
        },
        {
            "Sid": "RDSFull",
            "Action": [
                "rds:ModifyDBInstance"
            ],
            "Effect": "Allow",
            "Resource": [
                "*"
            ]
        },
        {
            "Sid": "S3Full",
            "Action": [
                "s3:GetObject",
                "s3:ListBucket"
            ],
            "Effect": "Allow",
            "Resource": [
                "arn:aws:s3:::myprivatebucket"
            ]
        }
    ],
    "Version": "2012-10-17"
}
```
When this script is run against the role, then it will output findings for Action Wildcard, Resource Star, and Resource Mismatch: 
```
[
  {
    "issue": "Action_Wildcard",
    "title": "",
    "severity": "",
    "description": "",
    "detail": "",
    "location": {
      "action": "ec2:*",
      "filepath": null
    },
    "policy_name": "arn:aws:iam::954013203577:policy/test-policy"
  },
  {
    "issue": "RESOURCE_STAR",
    "title": "",
    "severity": "",
    "description": "",
    "detail": null,
    "location": {
      "actions": [
        "ec2:*"
      ],
      "filepath": null
    },
    "policy_name": "arn:aws:iam::123456789012:policy/test-policy"
  },
  {
    "issue": "RESOURCE_STAR",
    "title": "",
    "severity": "",
    "description": "",
    "detail": null,
    "location": {
      "actions": [
        "rds:ModifyDBInstance"
      ],
      "filepath": null
    },
    "policy_name": "arn:aws:iam::123456789012:policy/test-policy"
  },
  {
    "issue": "RESOURCE_MISMATCH",
    "title": "",
    "severity": "",
    "description": "",
    "detail": [
      {
        "action": "s3:GetObject",
        "required_format": "arn:*:s3:::*/*"
      }
    ],
    "location": {
      "actions": [
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "filepath": null
    },
    "policy_name": "arn:aws:iam::123456789012:policy/test-policy"
  }
]
```

## Custom Checks
[Action_Wildcard](action_wildcard.py) checks for actions which have wildcards in them.
