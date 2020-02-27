from rest_framework.views import APIView
from .serializers import CategorySerializer, ProductSerializer
from .models import Category, Product
from rest_framework.response import Response
from rest_framework import status
from zaiko.responses import *
from zaiko.custom_status_code import DATA_ADDED_SUCCESSFULLY, DATA_DOES_NOT_EXISTS, \
    DATA_FOUND_SUCCESSFUL, BAD_REQUEST
from zaiko.permissions import IsAuthenticated


class CategoryGetAndPostView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        """
        ### Stores the Category details

        ### Request URL

             SYNTAX URL : https://HOST-IP/api/v1/categories

             SAMPLE URL : https://HOST-IP/api/v1/categories

        ### Sample request data
            {
                "category_name": "Electronic"
            }

        ### Success response
            {
                "success": true,
                "message": "Data Added Successfully",
                "payload": {
                    "id": 1,
                    "category_name": "Electronic",
                    "created_at": "2019-03-26T09:17:05.657045Z",
                    "modified_at": "2019-03-26T09:17:05.657131Z"
                }
            }
        """

        serializer = CategorySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(generate_success_response(DATA_ADDED_SUCCESSFULLY, payload=serializer.data),
                            status=status.HTTP_200_OK)

        return Response(generate_failure_response(BAD_REQUEST, payload=serializer.errors),
                        status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        """
        ### Fetch all the Categories

        ### Request URL

            SYNTAX URL : https://HOST-IP/api/v1/categories

            SAMPLE URL : https://HOST-IP/api/v1/categories

        ### If data resist in database

            {
                "success": true,
                "message": "Data found successfully",
                "payload": [
                    {
                        "id": 1,
                        "category_name": "Electronic",
                        "created_at": "2019-03-26T09:17:05.657045Z",
                        "modified_at": "2019-03-26T09:17:05.657131Z"
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

        category = Category.objects.all()

        if category.exists():
            serializer = CategorySerializer(category, many=True)
            return Response(generate_success_response(DATA_FOUND_SUCCESSFUL, payload=serializer.data),
                            status=status.HTTP_200_OK)

        return Response(generate_failure_response(DATA_DOES_NOT_EXISTS, payload={}),
                        status=status.HTTP_404_NOT_FOUND)


class ProductGetAndPostView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
        ### Stores the Product details

        ### Request URL

             SYNTAX URL : https://HOST-IP/api/v1/products

             SAMPLE URL : https://HOST-IP/api/v1/products

        ### Sample request data
            {
                "product_name": "Grinder",
                "product_description": "Easy to prepare smooth paste and fine powder,
                 Different jars and blades to process different types of ingredients",
                "supplier": "1",
                "category": "1",
                "unit_in_stock": "350",
                "product_sell_amount": "3495",
                "product_cost_amount": "2000"
            }

        ### Error response
            {
                "success": false,
                "message": "Bad Request",
                "payload": {
                    "supplier": [
                        "Invalid pk \"2\" - object does not exist."
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
                    "product_name": "Grinder",
                    "product_description": "Easy to prepare smooth paste and fine powder,
                     Different jars and blades to process different types of ingredients",
                    "unit_in_stock": 350,
                    "product_sell_amount": 3495,
                    "product_cost_amount": 2000,
                    "created_at": "2019-03-26T09:37:06.253563Z",
                    "modified_at": "2019-03-26T09:37:06.253581Z",
                    "supplier": 1,
                    "category": 1
                }
            }
        """

        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()
            return Response(generate_success_response(DATA_ADDED_SUCCESSFULLY, payload=serializer.data),
                            status=status.HTTP_200_OK)

        return Response(generate_failure_response(BAD_REQUEST, payload=serializer.errors),
                        status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        """
        ### Fetch all the Products data

        ### Request URL

            SYNTAX URL : https://HOST-IP/api/v1/products

            SAMPLE URL : https://HOST-IP/api/v1/products

        ### If data resist in database

            {
                "success": true,
                "message": "Data found successfully",
                "payload": [
                    {
                        "id": 1,
                        "product_name": "Grinder",
                        "product_description": "Easy to prepare smooth paste and fine powder,
                         Different jars and blades to process different types of ingredients",
                        "unit_in_stock": 350,
                        "product_sell_amount": 3495,
                        "product_cost_amount": 2000,
                        "created_at": "2019-03-26T09:37:06.253563Z",
                        "modified_at": "2019-03-26T09:37:06.253581Z",
                        "supplier": 1,
                        "category": 1
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

        product = Product.objects.all()

        if product.exists():

            serializer = ProductSerializer(product, many=True)
            return Response(generate_success_response(DATA_FOUND_SUCCESSFUL, payload=serializer.data),
                            status=status.HTTP_200_OK)

        return Response(generate_failure_response(DATA_DOES_NOT_EXISTS, payload={}),
                        status=status.HTTP_404_NOT_FOUND)
