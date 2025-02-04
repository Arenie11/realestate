from django.shortcuts import get_object_or_404
from rest_framework import status,permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from.serializers import *
from. models import *
import requests
from django.conf import settings

#listingview
class ListingView(APIView):
    def get(self,request):
        try:
            listings = Listing.objects.filter(published=True, is_available=True)
            serializer = ListingSerializer(listings, many=True)
            return Response (serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response ({'error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#get single
class GetListingView(APIView):
    def get(self,request,):
        try:
            listing = get_object_or_404(Listing, published=True, is_available=True)
            serializer = ListingSerializer(listing)
            return Response (serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response ({'error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#inquiryview  
class InquiryView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def post(self,request):
        try:
            serializer= InquirySerializer(data=request.data)
            if serializer .is_valid():
                serializer.save()
                return Response (serializer.data, status=status.HTTP_200_OK)
            return Response (serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
             return Response ({'error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#search view
class SearchListingsView(APIView):
    def get(self,request):
        query = request.GET.get('q', '')
        category = request.GET.get('category', '')
        listings = Listing.objects.filter(published=True, is_available=True)

        if query:
            listings = listings.filter(title__icontains=query)

        if category:
            listings = listings.filter(category=category)

        serializer = ListingSerializer(listings, many=True)
        return Response(serializer.data)

#payment
class PaymentPageView(APIView):
    def get(self, request, id):
        try:
            listing = get_object_or_404(Listing, id=id)
        except Listing.DoesNotExist:
            return Response({'Error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({
            'listing' :listing.id,
            'total' :listing.amount,
            'paystack_public_key' :settings.PAYSTACK_PUBLIC_KEY
        }, status=status. HTTP_200_OK)
    
#verify payment
class VerifyPaymentView(APIView):
    def get (self, request,ref):
        try:
            order= get_object_or_404(Listing,ref=ref)
            url = f'https://api.paystack.co/transaction/verify/(ref)'
            headers= {"Authorization": f"Bearer {settings. PAYSTACK_SECRET_KEY}"}
            response = request. get (url, headers=headers)
            response_data = response. json()
            
            if response_data["status"] and response_data ["data"] ["status"] =="success":
                listingpayment_complete = True
                Listing.save()
                return Response ({"Message": "Payment verify successfully"}, status-status.
                HTTP_200_0K)
            else:
                return Response({"Error": "Payment verify failed"}, status=status.
                HTTP_400_BAD_REQUEST)
        except Listing.DoesNotExist:
            return Response({'error': 'invalid payment reference'}, status=status.
            HTTP_400._BAD_REQUEST)
        except Exception as e:
            return Response({'error': str (e)},  status=status.HTTP_500_INTERNAL_SERVER_ERROR)

