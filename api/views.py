from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, authentication, permissions, serializers
from api.serializers import UserSerializer, ExpenseSerializer
from expense.models import Expense


# Create your views here.

class UserCreatView(APIView):
    
    serializer_class = UserSerializer
    
    def post(self, request, *args, **kwargs):
        
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class ExpenseListCreateView(APIView):
    
    # authentication_classes = [authentication.BasicAuthentication]
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ExpenseSerializer
    
    def get(self, request, *args, **kwargs):
        
        qs = Expense.objects.filter(owner=request.user)
        
        if 'category' in request.query_params:
            search_text = request.query_params.get('category')
            qs = qs.filter(category=search_text)
            
        if 'payment_method' in request.query_params:
            search_text = request.query_params.get('payment_method')
            qs = qs.filter(payment_method=search_text)
        
        serializer = self.serializer_class(qs, many=True)
        
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            serializer.save(owner=request.user)
            
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ExpenseRetrieveUpdateDestroyView(APIView):
    
    # authentication_classes = [authentication.BasicAuthentication]
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ExpenseSerializer
    
    def get(self, request, *args, **kwargs):
        
        id = kwargs.get('pk')
        expense_object = get_object_or_404(Expense, id=id)
        
        if request.user != expense_object.owner:
            raise serializers.ValidationError('Access denied')
        
        serializer = self.serializer_class(expense_object)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    
    def delete(self, request, *args, **kwargs):
        
        id = kwargs.get('pk')
        expense_object = get_object_or_404(Expense, id=id)
        
        if request.user != expense_object.owner:
            raise serializers.ValidationError('Access denied')
        
        expense_object.delete()
        
        return Response(data={'message':'Expense item deleted'})

    
    def put(self, request, *args, **kwargs):
        
        id = kwargs.get('pk')
        expense_object = get_object_or_404(Expense, id=id)
        
        if request.user != expense_object.owner:
            raise serializers.ValidationError('Access denied')
        
        serializer = self.serializer_class(data=request.data, instance=expense_object)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)