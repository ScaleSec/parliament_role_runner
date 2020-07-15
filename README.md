# parliament_role_runner

See [blog post](https://scalesec.com/blog) for more info.

This is a script to run [Parliament](https://github.com/duo-labs/parliament/) on an IAM role to lint and analyze all of it's attached policies for misconfigurations. 


## Usage:
Create your virtual environment and install requirements:
```
python3 -m venv my_venv
source my_venv/bin/activate
pip install -r requirements.txt
```

Run with:
```
python3 run_parliament.py --rolename <rolename> --profile <profile>
```


## Output

If the role has findings, it will print the findings to the console

```
{
    "issue": "RESOURCE_STAR",
    "title": "Unnecessary use of Resource *",
    "severity": "LOW",
    "description": "",
    "detail": null,
    "location": {
        "actions": [
        "ec2:*"
        ],
        "filepath": "policy.json"
    }
}
```

## Custom Checks
[Action_Wildcard](action_wildcard.py) checks for actions which have wildcards in them.