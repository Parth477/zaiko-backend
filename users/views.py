# from django.shortcuts import render
from rest_framework.views import APIView
from .serializer import *
import coreapi
from rest_framework.schemas import AutoSchema
from .task import send_email_task
from rest_framework.response import Response
from zaiko import responses
from rest_framework import status
from zaiko import custom_status_code

class PostCustomerRegistration(APIView):
    """
       User registration
       #sample data
       {
           "first_name": "Darshit",
           "last_name": "Ghinaiya",
           "email": "parth13@yopmail.com",
           "contact_no": "9974179352",
           "address": "Ahemdabad",
           "organization": "GPS tech",
           "password":"parth"

       }

       # Success response
       {
           "success": true,
           "message": "User registration successful",
           "payload": {
               "first_name": "Darshit",
               "last_name": "Ghinaiya",
               "email": "parth13@yopmail.com",
               "contact_no": "9974179352",
               "address": "Ahemdabad",
               "organization": "GPS tech"
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
        "email": "sunny@yopmail.com",
        "password":"parth"
    }

    # Success response
    {
        "success": true,
        "message": "Login Successfull",
        "payload": {
            "user": {
                "id": 4,
                "last_login": null,
                "first_name": "Sunny",
                "last_name": "Kalola",
                "email": "sunny@yopmail.com",
                "is_email_verified": true,
                "organization": "GPS tech",
                "contact_no": "9974179352",
                "address": "Ahemdabad",
                "created": "2020-02-26T17:38:42.050353Z"
            },
            "token": "45e3cddf67c27c60a77a8fdea86411cdb27a2643"
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









#
# # Get Customer list
# class GetCutomer(APIView):
#
#     def get(self, request):
#         """
#             Get Customer list
#
#             ### IF DATA EXIST IN DATABASE
#
#             {
#                 "success": true,
#                 "message": "Data found successfully",
#                 "payload": [
#                     {
#                         "id": 1,
#                         "first_name": "Parth",
#                         "last_name": "Ghinaiya",
#                         "email": "sparth@yopmail.com",
#                         "avatar_url": "http://a.com",
#                         "phone_no": "9974179352",
#                         "organization": "Own Business",
#                         "address": "Ahemdabad",
#                         "created": "2019-03-26T11:46:01.836491Z",
#                         "modified": "2019-03-26T11:46:01.836511Z",
#                         "role": 1
#                     }
#                 ]
#             }
#
#         ### IF DATA NOT EXISTS
#
#              {
#                 "success": false,
#                 "message": "Data does not exists",
#                 "payload": {},
#                 "error_code": 204
#             }
#
#         """
#         users = Users.objects.all().order_by('-modified')
#         if users.exists() :
#             serializer = CustomerDetailsSerializer(users, many = True)
#             return Response(responses.generate_success_response(custom_status_code.DATA_FOUND_SUCCESSFUL,
#                                                                 payload=serializer.data),status=status.HTTP_200_OK)
#
#         else:
#             return Response(responses.generate_failure_response(custom_status_code.DATA_DOES_NOT_EXISTS, payload={}),status=status.HTTP_204_NO_CONTENT)
#
#
# #Login Details
# class PostLogin(APIView):
#
#     def post(self, request):
#         """
#             Store login time and date as well as authenticate user
#
#         ### Request data
#              {
#                 "email":string (required),
#                 "password":string (required),
#              }
#
#         ### Sample Sample request data
#             {
#                 "email":"parth@yopmail.com",
#                 "password":"parth123"
#             }
#
#         ### Error Responses
#
#         ### Invalid data
#             {
#                 "success": false,
#                 "message": "Bad Request",
#                 "payload": {
#                     "email": [
#                             "Enter a valid email address."
#                         ]
#                     },
#                     "error_code": 400
#                 }
#                 "error_code": 400
#             }
#             HTTP status code 400:- Bad Request
#             {
#                 "success": false,
#                 "message": "This email id does not exists",
#                 "payload": {},
#                 "error_code": 400
#             }
#
#              {
#                 "success": false,
#                 "message": "Password does not match with this email id",
#                 "payload": {},
#                 "error_code": 400
#             }
#
#             {
#                 "success": false,
#                 "message": "User with this email id already exists",
#                 "payload": {},
#                 "error_code": 400
#             }
#         ### Success responses
#             {
#                 "success": true,
#                 "message": "Data found successfully",
#                 "payload": {
#                     "Token": "9a799258e90c570b3eb23b61f31d06d4b60e4de4"
#                 }
#             }
#
#         """
#         serializer = LoginSerializer(data=request.data)
#
#         if serializer.is_valid():
#             try :
#                 user = Users.objects.get(email=request.data['email'])
#                 user_pass = UserLogin.objects.get(user_id=user.pk)
#                 token = Token.objects.get(user=user)
#
#                 if user_pass.check_password(request.data['password']):
#                     return Response(responses.generate_success_response
#                                     (custom_status_code.DATA_FOUND_SUCCESSFUL
#                                      ,payload={"Token":token.key},),status=status.HTTP_200_OK)
#                 return Response(responses.generate_failure_response
#                                 (custom_status_code.PASSWORD_WRONG_WITH_THIS_EMAIL_ID,
#                                  payload={})
#                                 ,status=status.HTTP_400_BAD_REQUEST)
#
#             except Users.DoesNotExist:
#                 return Response(
#                     responses.generate_failure_response
#                     (custom_status_code.EMAIL_ID_NOT_MATCH,
#                      payload={}),
#                     status=status.HTTP_400_BAD_REQUEST
#                 )
#         else :
#             return Response(responses.generate_failure_response
#                             (custom_status_code.BAD_REQUEST,
#                              serializer.errors),status=status.HTTP_400_BAD_REQUEST)
#
#
