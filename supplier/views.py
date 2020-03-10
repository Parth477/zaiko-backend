from rest_framework.views import APIView
from .serializers import SupplierSerializer
from .models import Supplier
from rest_framework.response import Response
from rest_framework import status
from zaiko.responses import *
from zaiko.custom_status_code import DATA_ADDED_SUCCESSFULLY, DATA_DOES_NOT_EXISTS, \
    BAD_REQUEST, DATA_FOUND_SUCCESSFUL


class SupplierGetAndPostView(APIView):

    def post(self, request):
        """
        ### Stores the Supplier details

        ### Request URL

             SYNTAX URL : https://HOST-IP/api/v1/suppliers

             SAMPLE URL : https://HOST-IP/api/v1/suppliers

        ### Sample request data
            {
                "supplier_name": "Philips",
                "supplier_office_address": "Banglore",
                "supplier_phone_number": "9326541236"
            }

        ### Error response
            {
                "success": false,
                "message": "Bad Request",
                "payload": {
                    "supplier_phone_number": [
                        "Ensure this field has no more than 10 characters."
                    ]
                },
                "error_code": 400
            }

        ### Success response
            {
                "success": true,
                "message": "Data Added Successfully",
                "payload": {
                    "id": 1,
                    "supplier_name": "Philips",
                    "supplier_office_address": "Banglore",
                    "supplier_phone_number": "9326541236",
                    "created_at": "2019-03-26T09:31:05.944860Z",
                    "modified_at": "2019-03-26T09:31:05.944880Z"
                }
            }
        """

        serializer = SupplierSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(generate_success_response(DATA_ADDED_SUCCESSFULLY, payload=serializer.data),
                            status=status.HTTP_200_OK)

        return Response(generate_failure_response(BAD_REQUEST, payload=serializer.errors),
                        status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        """
        ### Fetch all Supplier Data

        ### Request URL

            SYNTAX URL : https://HOST-IP/api/v1/suppliers

            SAMPLE URL : https://HOST-IP/api/v1/suppliers

        ### If data resist in database
            {
                "success": true,
                "message": "Data found successfully",
                "payload": [
                    {
                        "id": 1,
                        "supplier_name": "Philips",
                        "supplier_office_address": "Banglore",
                        "supplier_phone_number": "9326541236",
                        "created_at": "2019-03-26T09:31:05.944860Z",
                        "modified_at": "2019-03-26T09:31:05.944880Z"
                    }
                ]
            }

        ### If data does not exists in database
            {
                "success": false,
                "message": "Data does not exists",
                "payload": {},
                "error_code": 204
            }

        """

        supplier = Supplier.objects.all()

        if supplier.exists():
            serializer = SupplierSerializer(supplier, many=True)
            return Response(generate_success_response(DATA_FOUND_SUCCESSFUL, payload=serializer.data),
                            status=status.HTTP_200_OK)

        return Response(generate_failure_response(DATA_DOES_NOT_EXISTS,
                                                  payload={}),
                        status=status.HTTP_404_NOT_FOUND)
