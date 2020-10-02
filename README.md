# aws-billing-notification

Lambda function that notifies Slack of AWS usage charges at JST 09:00.

## Setup

### 1. venv

```
$ python -m venv slsvenv
$ make activate
```

### 2. pip install

```
$ make pip_install
```

### 3. Setup Serverless Framework

```
$ npm install -g serverless
$ npm install --save serverless-python-requirements
$ npm install --save serverless-pseudo-parameters
```

## Deploy to Your AWS Environment

```
$ make deploy PROFILE=${YOUR_AWS_PROFILE_NAME}
```
