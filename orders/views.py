from rest_framework.views import APIView
from .models import Orders
from .serializers import OrdersSerializer
from zaiko import responses, custom_status_code
from rest_framework.response import Response
from rest_framework import status


# Create your views here.

class GetPostOrder(APIView):
    def get(self, request):
        """
        ### All Register Customer Data

        ### Request URL

             SYNTAX URL : https://HOST-IP/api/v1/orders

             SAMPLE URL : https://HOST-IP/api/v1/orders

        ### IF DATA RESISTS IN DATABASE

            {
                "success": true,
                "message": "Data found successfully",
                "payload": {
                    "Order Data:": [
                        {
                            "id": 1,
                            "amount": 55,
                            "total_amount": 181,
                            "order_date": "1997-02-12",
                            "shipping_date": "1997-03-12",
                            "shipping_address": "Ahemdabad",
                            "customer": 1,
                            "product": 1
                        },
                        {
                            "id": 2,
                            "amount": 55,
                            "total_amount": 181,
                            "order_date": "1997-02-12",
                            "shipping_date": "1997-03-12",
                            "shipping_address": "Ahemdabad",
                            "customer": 1,
                            "product": 1
                        }
                    ]
                }
            }

        ### IF DATA NOT EXISTS

             {
                "success": false,
                "message": "Data does not exists",
                "payload": {},
                "error_code": 204
            }

        """

        orders = Orders.objects.all()
        if orders.exists():
            orders_details = OrdersSerializer(orders, many=True)
            payload = {'Order Data:': orders_details.data}
            return Response(responses.generate_success_response
                            (custom_status_code.DATA_FOUND_SUCCESSFUL, payload=payload),
                            status=status.HTTP_200_OK)
        return Response(responses.generate_failure_response
            (custom_status_code.DATA_DOES_NOT_EXISTS, payload={}),
            status=status.HTTP_204_NO_CONTENT)

    def post(self, request):
        """
        ### User Registrations Details


        ### Request URL


             SYNTAX URL : https://HOST-IP/api/v1/orders

             SAMPLE URL : https://HOST-IP/api/v1/orders

        ### Request data
             {
                "amount": float(require),
                "total_amount": float(require),
                "order_date": "1997-02-12",
                "shipping_date": string(required) format YYYY-MM-DD,
                "shipping_address": string(required),
                "customer": integer(required),
                "product": integer(required)
            }

        ### Sample Sample request data
            {
                "amount": 55,
                "total_amount": 181,
                "order_date": "1997-02-12",
                "shipping_date": "1997-03-12",
                "shipping_address": "Ahemdabad",
                "customer": 1,
                "product": 1
            }

        ### Error Responses


        ### Invalid data
            {
                "success": false,
                "message": "Bad Request",
                "payload": {
                    "order_date": [
                        "Date has wrong format. Use one of these formats instead: YYYY-MM-DD."
                    ],
                    "customer": [
                        "This field is required."
                    ]
                },
                "error_code": 400
            }


        ### Success responses
            {
                "success": true,
                "message": "Data Added Successfully",
                "payload": {
                    "id": 3,
                    "amount": 55,
                    "total_amount": 181,
                    "order_date": "1997-02-12",
                    "shipping_date": "1997-03-01",
                    "shipping_address": "Ahemdabad",
                    "customer": 1,
                    "product": 1
                }
            }

        """

        add_order = OrdersSerializer(data=request.data)
        if add_order.is_valid():
            add_order.save()
            return Response(responses.generate_success_response
                            (custom_status_code.DATA_ADDED_SUCCESSFULLY, payload=add_order.data),
                            status=status.HTTP_201_CREATED)
        return Response(responses.generate_failure_response
                        (custom_status_code.BAD_REQUEST, payload=add_order.errors),
                        status=status.HTTP_400_BAD_REQUEST)

