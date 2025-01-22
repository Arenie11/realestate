from django.shortcuts import get_object_or_404
from rest_framework import status,permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from.serializers import *
from. models import *

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
    def get(self,request, pk):
        try:
            listing = get_object_or_404(Listing, pk=pk, published=True, is_available=True)
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
