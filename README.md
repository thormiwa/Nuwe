# Nuwe Hackathon 

This is a flask app that includes an authentication API and a logging system for admin users to view the logs of the users.

## Installation
Install the requirements using pip
```bash
pip install -r requirements.txt
```
## Usage
Run the app using the following command
```bash
python app.py
```

Add the following to your config file
```bash

DATABASE_NAME = "nuwe"
JWT_SECRET_KEY = "secret"
```

## API Documentation
### Authentication Task 1 and 2
#### Register
```bash
POST /register
```
##### Parameters
| Name | Type | Description |
| ---- | ---- | ----------- |
| first_name | string | The first name of the user |
| last_name | string | The last name of the user |
| email | string | The email of the user |
| username | string | The username of the user |
| role | string | The role of the user |
| password | string | The password of the user |

##### Response
```json
{
    "message": "User created successfully"
}
```

#### Login
```bash
POST /login
```
##### Parameters
| Name | Type | Description |
| ---- | ---- | ----------- |
| username | string | The username of the user |
| password | string | The password of the user |

##### Response
```json
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9"
}
```

#### Home
```bash
GET /home
```
##### Parameters (Header)
| Name | Type | Description |
| ---- | ---- | ----------- |
| Authorization | string | The access token of the user |

##### Response
```json
{
    "message": "Welcome back {current_user}! Your current role is {user_role}. Great to have you back."
}
```

### Encyption Algorithm Used
The encryption algorithmm used is bcrypt. The password is hashed and stored in the database. When the user logs in, the password is hashed and compared to the hashed password in the database. I used bcrypt because it is a slow hashing algorithm and it is difficult to brute force.

### MFA AUTHENTICATION Used
I used the jwt token for the access control because it is a secure way to authenticate users and also to verify if a user is an admin or not which will be used for the logging system logic.

### Logging Task 3

#### Get Logs
```bash
GET /log
```
##### Parameters (Header)
| Name | Type | Description |
| ---- | ---- | ----------- |
| Authorization | string | The access token of the user |

##### Response
```json
{
    "latest_connections": [
        {
            "ip": "127.0.0.1",
            "date": "Jul 03, 2023",
            "http_verb": "GET",
            "endpoint": "/log"
        }
        {
            "ip": "127.0.0.1",
            "date": "Jul 03, 2023",
            "http_verb": "GET",
            "endpoint": "/register"
        }
    ],
    "all_connections": [
        {
            "ip": "127.0.0.1",
            "date": "Jul 01, 2023",
            "http_verb": "GET",
            "endpoint": "/home"
        },
        {
            "ip": "127.0.0.1",
            "date": "Jul 02, 2023",
            "http_verb": "GET",
            "endpoint": "/register"
}
```


