from zaiko.constant import KEY_ERR_CODE, KEY_MESSAGE, KEY_SUCCESS_CODE

BAD_REQUEST = {
    KEY_ERR_CODE: 400,
    KEY_MESSAGE: 'Bad Request'
}

DATA_ADDED_SUCCESSFULLY = {
    KEY_SUCCESS_CODE: 201,
    KEY_MESSAGE: 'Data Added Successfully'
}

SUCCESSFUL_SEND_MESSAGE = {
    KEY_SUCCESS_CODE: 200,
    KEY_MESSAGE: 'Email Send Successfully'
}

DATA_DOES_NOT_EXISTS = {
    KEY_ERR_CODE: 204,
    KEY_MESSAGE: 'Data does not exists'
}

DATA_FOUND_SUCCESSFUL = {
    KEY_SUCCESS_CODE: 200,
    KEY_MESSAGE: 'Data found successfully'
}

USER_CREATED_SUCCESSFULLY = {
    KEY_SUCCESS_CODE: 201,
    KEY_MESSAGE: 'User registration successful'
}

USER_ALREADY_EXISTS = {
    KEY_ERR_CODE: 400,
    KEY_MESSAGE: 'User with this email id already exists'
}

PASSWORD_WRONG_WITH_THIS_EMAIL_ID = {
    KEY_ERR_CODE: 400,
    KEY_MESSAGE: 'Password does not match with this email id'
}

EMAIL_ID_NOT_MATCH = {
    KEY_ERR_CODE: 400,
    KEY_MESSAGE: 'This email id does not exists'
}

USER_DOES_NOT_EXISTS_OR_DISABLED = {
    KEY_ERR_CODE: 1016,
    KEY_MESSAGE: "User doesn't exists or email doesn't verified"
}

INVALID_EMAIL_OR_PASSWORD = {
    KEY_ERR_CODE: 1003,
    KEY_MESSAGE: 'Invalid email or password'
}

INVALID_INVITATION_TOKEN = {
    KEY_ERR_CODE: 301,
    KEY_MESSAGE: "Invalid user invitation token."
}

EMAIL_VERIFIED_SUCCESSFULLY = {
    KEY_SUCCESS_CODE: 300,
    KEY_MESSAGE: "Email verified successfully."
}

USER_ROLE_LIST_SENT = {
    KEY_SUCCESS_CODE: 200,
    KEY_MESSAGE: 'User role sent successfully'
}
