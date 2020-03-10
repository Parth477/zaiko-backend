from rest_framework.views import APIView
from .serializer import *
from .task import send_email_task
from rest_framework.response import Response
from zaiko import responses
from rest_framework import status
from zaiko import custom_status_code
from zaiko.permissions import IsAuthenticated

class PostCustomerRegistration(APIView):
    """
       User registration
       #sample data
       {
           "first_name": "Parth",
           "last_name": "Ghinaiya",
           "email": "parth@yopmail.com",
           "contact_no": "9974179352",
           "address": "Ahemdabad",
           "organization": "GPS tech",
           "password":"parth",
           "user_role": 2

        }

       # Success response
       {
            "success": true,
            "message": "User registration successful",
            "payload": {
                "id": 2,
                "last_login": null,
                "first_name": "Parth",
                "last_name": "Ghinaiya",
                "email": "parth@yopmail.com",
                "is_email_verified": false,
                "organization": "GPS tech",
                "contact_no": "9974179352",
                "address": "Ahemdabad",
                "created": "2020-03-10T06:32:18.426026Z",
                "user_role": 2
            }
        }
       """

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            if Users.objects.filter(email=request.data['email']).exists():
                return Response(responses.generate_failure_response
                                (custom_status_code.USER_ALREADY_EXISTS, {}),
                                status=status.HTTP_400_BAD_REQUEST)
            user = Users.objects.create_user(email=request.data['email'])
            user.first_name = request.data['first_name']
            user.set_password(request.data['password'])
            user.last_name = request.data['last_name']
            user.user_role_id = request.data['user_role']
            user.contact_no = request.data['contact_no']
            user.address = request.data['address']
            user.organization = request.data['organization']
            user.save()

            # retrive token
            Token.objects.create(user=user)
            token = Token.objects.get(user_id=user.id)
            token_obj = TokenList.objects.create(user_id=user.id, token=token.key)
            token_obj.save()

            # registration link send into mail...
            send_email_task.delay(user.email, token.key)
            user_serializer = UserSerializer(user)
            return Response(responses.generate_success_response(
                custom_status_code.USER_CREATED_SUCCESSFULLY,
                payload=user_serializer.data), status=status.HTTP_200_OK)

        return Response(
            responses.generate_failure_response(
                custom_status_code.BAD_REQUEST,
                serializer.errors), status=status.HTTP_400_BAD_REQUEST)

class VerifyMailAPI(APIView):
    """
    Verify Email usimng token sent to user into mail
    """
    def get(self, request, token):
        try:
            user_id = TokenList.objects.filter(token=token)
            user = Users.objects.get(id=user_id[0].user_id)
            user.is_email_verified = True
            user.save()

            return Response(
                responses.generate_success_response(custom_status_code.EMAIL_VERIFIED_SUCCESSFULLY,
                                                    payload={}), status=status.HTTP_200_OK)
        except:
            return Response(
                responses.generate_failure_response(custom_status_code.INVALID_INVITATION_TOKEN,
                                                    payload={}), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserLogin(APIView):
    """
    # Sample data
    {
        "email": "parth@yopmail.com",
        "password":"parth"
    }

    # Success response
    {
        "success": true,
        "message": "Login Successfull",
        "payload": {
            "user": {
                "id": 2,
                "last_login": null,
                "first_name": "Parth",
                "last_name": "Ghinaiya",
                "email": "parth@yopmail.com",
                "is_email_verified": true,
                "organization": "GPS tech",
                "contact_no": "9974179352",
                "address": "Ahemdabad",
                "created": "2020-03-10T06:32:18.426026Z",
                "user_role": 2
            },
            "token": "03d6bde4a8cf30b5a032b04e4c53a973f119ce9c"
        }
    }
    """
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                responses.generate_failure_response(custom_status_code.BAD_REQUEST,
                    payload=serializer.errors),
                status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Users.objects.get(email=request.data['email'])
            if user.is_email_verified is False:
                return Response(
                    responses.generate_failure_response(custom_status_code.USER_DOES_NOT_EXISTS_OR_DISABLED,
                                                        payload={}), status=status.HTTP_400_BAD_REQUEST)
            # print(user.first_name)
            if user.check_password(request.data['password']):

                token = Token.objects.get(user_id=user.id)
                user_serializer = UserSerializer(user)

                return Response(responses.generate_response(
                    success=True,
                    msg="Login Successfull",
                    payload={
                        'user': user_serializer.data,
                        'token': token.key
                    }),
                    status=status.HTTP_200_OK)
            else:
                return Response(
                    responses.generate_failure_response(custom_status_code.INVALID_EMAIL_OR_PASSWORD,
                                                        payload={}), status=status.HTTP_400_BAD_REQUEST)
        except Users.DoesNotExist:
            return Response(
                responses.generate_failure_response(custom_status_code.INVALID_EMAIL_OR_PASSWORD,
                                                    payload={}), status=status.HTTP_400_BAD_REQUEST)



class UserRoleAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
            # User Roles Get APi

            #  Response

                {
                    "success": true,
                    "message": " User role sent successfully",
                    "payload": { },
                    }
                }
        """
        # get the list of roles
        roles = UserRole.objects.all().order_by('id')

        serializer = UserRoleSerializer(roles, many=True)

        return Response(
            responses.generate_success_response(
                custom_status_code.USER_ROLE_LIST_SENT,
                payload=serializer.data),
            status=status.HTTP_200_OK)
