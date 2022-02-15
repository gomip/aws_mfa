# aws_mfa

# vi ~/.aws/config
```
[aws-dev]
mfa_serial = MFA_SERIAL
output = json

[profile dev]
user_arn = USER_ARN
source_profile = aws-dev
region = ap-northeast-2
```

# vi ~/.aws/credentials
```
[aws-dev]
aws_access_key_id = ACCESS_KEY
aws_secret_access_key = SECRET_KEY
```

# generate session token
```
aws sts get-session-token --serial-number [MFA_SERIAL] --token-code [OTP] --profile dev
```

# allow permission
```
chmod 700 ./main.py
```

# run
```
./main.py PROFILE
```
