# aws-billing-notification

## About

Lambda function that notifies Slack of AWS usage charges at JST 09:00.

## Directories

```
├── config
│   └── variables.py
├── src
│   └── handler.py
└── tests
    └── test_handler.py
```

- `config/variables.py` : The directory that contains the files to set the variables.
- `src/handler.py` : The directory that contains a group of functions, including handler.
- `tests/test_handler.py` : The directory to store the test code.

## Setup

### 1. venv

```
$ python -m venv slsvenv
$ source ./slsvenv/bin/activate
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
