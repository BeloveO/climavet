from django.shortcuts import render
from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import DisasterPlan, DisasterType
from .services.plan_generator import DisasterPlanGenerator
from datetime import datetime
from .serializers import DisasterPlanSerializer, DisasterTypeSerializer
from clinics.models import Clinic
from .data.disaster_protocols import DISASTER_PROTOCOLS

# Create your views here.
class DisasterPlanViewSet(viewsets.ModelViewSet):
    queryset = DisasterPlan.objects.all()
    serializer_class = DisasterPlanSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Adjust permissions as needed

    def get_queryset(self):
        """
        Optionally restricts the returned disaster plans to a given clinic or disaster type,
        by filtering against query parameters in the URL.

        :return: A queryset of DisasterPlan instances filtered by clinic and/or disaster type if specified.
        """
        queryset = super().get_queryset()
        clinic_id = self.request.query_params.get('clinic')
        disaster_type = self.request.query_params.get('disaster_type')
        
        if clinic_id:
            queryset = queryset.filter(clinic_id=clinic_id)
        if disaster_type:
            queryset = queryset.filter(disaster_type__category=disaster_type)
        
        return queryset

    def create(self, request, *args, **kwargs):
        """
        Create a new disaster plan based on the provided clinic, disaster type, and risk assessment data.

        :param request: The HTTP request containing the clinic ID, disaster type ID, and risk assessment data.
        :return: A response containing the created disaster plan or an error message if creation fails.
        """
        data = request.data
        disaster_type_id = data.get('disaster_type')
        try:
            disaster_type = DisasterType.objects.get(id=disaster_type_id)
        except DisasterType.DoesNotExist:
            return Response({'error': 'Disaster Type not found'}, status=status.HTTP_404_NOT_FOUND)
        try:
            protocol = DISASTER_PROTOCOLS.get(disaster_type.category)
            if not protocol:
                return Response({'error': 'No protocol found for this disaster type'}, status=status.HTTP_404_NOT_FOUND)
            return Response({'protocol': protocol}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['post', 'get'], url_path='generate', permission_classes=[permissions.AllowAny])
    def generate(self, request, *args, **kwargs):
        """
        Get plans from ones saved in disaster protocol data based on the type of disaster provided in request body. This endpoint can be used to generate plans without needing to go through the full risk assessment process, using predefined protocols as a starting point.
        """
        if request.method == 'GET':
            disaster_type_id = request.query_params.get('disaster_type')
        else:  # POST
            disaster_type_id = request.data.get('disaster_type')
        
        if not disaster_type_id:
            return Response(
                {'error': 'disaster_type is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Convert to integer if it's a string
            if isinstance(disaster_type_id, str):
                disaster_type_id = int(disaster_type_id)
                
            disaster_type_obj = DisasterType.objects.get(id=disaster_type_id)
            
            # Get protocol using the category
            protocol = DISASTER_PROTOCOLS.get(disaster_type_obj.category)
            
            if not protocol:
                return Response(
                    {'error': f'No protocol found for disaster category: {disaster_type_obj.category}'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Add metadata to the response
            response_data = protocol.copy()
            response_data['created_at'] = datetime.now().isoformat()
            response_data['disaster_type_info'] = {
                'id': disaster_type_obj.id,
                'name': disaster_type_obj.name,
                'category': disaster_type_obj.category,
                'description': disaster_type_obj.description
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
            
        except DisasterType.DoesNotExist:
            return Response(
                {'error': f'Disaster Type with id {disaster_type_id} not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except ValueError:
            return Response(
                {'error': 'Invalid disaster_type ID format'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            print(f"Error generating plan: {str(e)}")
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
    @action(detail=False, methods=['get'], url_path='templates')
    def templates(self, request):
        """
        Retrieve a list of available disaster plan templates based on predefined protocols.

        :param request: The HTTP request.
        :return: A response containing a list of disaster plan templates.
        """
        # Logic to retrieve and return disaster plan templates goes here
        return Response({'templates': list(DISASTER_PROTOCOLS.keys())})
    
    @action(detail=True, methods=['get'], url_path='download')
    def download_plan(self, request, pk=None):
        """
        Download the disaster plan as a PDF.

        :param request: The HTTP request.
        :param pk: The primary key of the disaster plan to download.
        :return: A response containing the PDF file.
        """
        # PDF generation logic goes here
        pass
        
class DisasterTypeViewSet(viewsets.ModelViewSet):
    queryset = DisasterType.objects.all()
    serializer_class = DisasterTypeSerializer
    permission_classes = [permissions.AllowAny]  # Adjust permissions as needed

    @action(detail=False, methods=['get'], url_path='categories')
    def categories(self, request):
        """
        Retrieve a list of unique disaster categories.

        :param request: The HTTP request.
        :return: A response containing a list of unique disaster categories.
        """
        categories = DisasterType.objects.values_list('category', flat=True).distinct()
        return Response({'categories': categories})
    
    @action(detail=True, methods=['get'], url_path='templates')
    def templates(self, request, pk=None):
        """
        Retrieve templates for a specific disaster type.

        :param request: The HTTP request.
        :param pk: The primary key of the disaster type.
        :return: A response containing templates for the specified disaster type.
        """
        try:
            disaster_type = self.get_object()
            template = DISASTER_PROTOCOLS.get(disaster_type.category)
            if not template:
                return Response({'error': 'No template available for this disaster type'}, status=status.HTTP_404_NOT_FOUND)
            return Response({'template': template})
        except DisasterType.DoesNotExist:
            return Response({'error': 'Disaster type not found'}, status=status.HTTP_404_NOT_FOUND)