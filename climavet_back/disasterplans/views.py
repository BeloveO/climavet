from urllib import request

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import DisasterPlan, DisasterType, ClinicTypes, ServiceTypes, SpeciesTypes, DisasterScenario
from .services.plan_generator import IntelligentDisasterPlanGenerator as DisasterPlanGenerator
from .serializers import ( DisasterPlanSerializer, DisasterTypeSerializer, 
                          SpeciesTypeSerializer, ServiceTypeSerializer, 
                          ClinicTypeSerializer, DisasterPlanCreateSerializer)
from .data.disaster_protocols import DISASTER_PROTOCOLS


DISASTER_NAME_TO_PROTOCOL = {
    'Flash Flood': 'FLOOD',
    'Flood': 'FLOOD',
    'Wildfire': 'WILDFIRE',
    'Forest Fire': 'WILDFIRE',
    'Heat Wave': 'HEATWAVE',
    'Extreme Heat': 'HEATWAVE',
    'Power Outage': 'POWER_OUTAGE',
    'Air Pollution': 'AIR_POLLUTION',
    'Erosion': 'EROSION',
    'Hurricane': 'HURRICANE',
    'Tornado': 'TORNADO',
    'Cold Wave': 'COLD_WAVE',
    'Extreme Cold': 'COLD_WAVE',
    'Blizzard': 'BLIZZARD',
    'Earthquake': 'EARTHQUAKE',
    'Avalanche': 'AVALANCHE',
}

# Create your views here.
class DisasterPlanViewSet(viewsets.ModelViewSet):
    queryset = DisasterPlan.objects.all().prefetch_related(
        'scenarios', 
        'scenarios__disaster_type',
        'service_types',
        'species_types'
    )
    serializer_class = DisasterPlanSerializer
    permission_classes = [permissions.AllowAny]  # Adjust permissions as needed

    def get_queryset(self):
        """
            Returns the disaster plans to a given scenario or disaster type,
        """
        return DisasterPlan.objects.all().prefetch_related(
            'scenarios', 
            'scenarios__disaster_type',
            'service_types',
            'species_types'
        )
    
    def get_serializer_class(self):
        if self.action == 'create':
            return DisasterPlanCreateSerializer
        return DisasterPlanSerializer

    def create(self, request, *args, **kwargs):
        """Create intelligent disaster plan"""
        print("\n" + "="*80)
        print("Received request to create disaster plan")
        print("="*80)
        print(f"Raw request data: {request.data}")
        print(f"Data type: {type(request.data)}")
        serializer = DisasterPlanCreateSerializer(data=request.data)

        print("Validating serializer...")
        is_valid = serializer.is_valid()
        print(f"Serializer valid: {is_valid}")
        if not is_valid:
            print("Serializer errors:")
            for field, errors in serializer.errors.items():
                print(f" - {field}: {errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        print(f"✅ Validation passed!")
        print(f"Validated data: {serializer.validated_data}")
           
        
        try:
            # Create the plan
            plan = serializer.save(created_by=None)
            print(f"Plan created with ID: {plan.id}")

            # Generate with intelligent system
            print(f"\n🔄 Generating intelligent disaster plan...")
            from .services.plan_generator import IntelligentDisasterPlanGenerator
            generator = IntelligentDisasterPlanGenerator(plan)
            plan = generator.generate()
            print(f"✅ Intelligent plan generated: {plan.scenarios.count()} scenarios")

            print(f"✅ Plan generated successfully!")
            print(f"   Scenarios: {plan.scenarios.count()}")
            print(f"   Risk score: {plan.risk_score}")
            print("="*80 + "\n")
            
            output_serializer = DisasterPlanSerializer(plan)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()
            print("="*80 + "\n")
            
            try:
                plan.delete()
            except:
                pass
            
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # output_serializer = DisasterPlanSerializer(plan)
        # return Response(output_serializer.data, status=status.HTTP_201_CREATED)


    @action(detail=False, methods=['post', 'get'], url_path='generate')
    def generate(self, request, *args, **kwargs):
        """
        Get plans from ones saved in disaster protocol data based on the type of disaster provided in request body. 
        This endpoint can be used to generate plans without needing to go through the full risk assessment process, 
        using predefined protocols as a starting point.
        """
        disaster_type_id = (
            request.query_params.get('disaster_type') 
            if request.method == 'GET' 
            else request.data.get('disaster_type')
        )
        
        if not disaster_type_id:
            return Response(
                {'error': 'disaster_type is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            disaster_type_obj = DisasterType.objects.get(id=int(disaster_type_id))
            
            # Map the disaster type name to protocol key
            protocol_key = DISASTER_NAME_TO_PROTOCOL.get(disaster_type_obj.name)
            
            if not protocol_key:
                return Response(
                    {'error': f'No protocol mapping found for "{disaster_type_obj.name}". Please contact administrator.'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            protocol = DISASTER_PROTOCOLS.get(protocol_key)
            
            if not protocol:
                return Response(
                    {'error': f'No protocol found for {protocol_key}'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            return Response(protocol, status=status.HTTP_200_OK)
            
        except DisasterType.DoesNotExist:
            return Response(
                {'error': f'Disaster Type with id {disaster_type_id} not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            print(f"Error in generate: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


        # data = request.data
        #disaster_type_id = data.get('disaster_type')
        #try:
        #    disaster_type = DisasterType.objects.get(id=disaster_type_id)
        #except DisasterType.DoesNotExist:
        #    return Response({'error': 'Disaster Type not found'}, status=status.HTTP_404_NOT_FOUND)
        #try:
        #    protocol = DISASTER_PROTOCOLS.get(disaster_type.category)
        #    if not protocol:
        #        return Response({'error': 'No protocol found for this disaster type'}, status=status.HTTP_404_NOT_FOUND)
        #    return Response({'protocol': protocol}, status=status.HTTP_200_OK)
        #except ValueError as e:
        #    return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

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
    

class ClinicTypeViewSet(viewsets.ModelViewSet):
    """List facility types"""
    queryset = ClinicTypes.objects.all()
    serializer_class = ClinicTypeSerializer
    permission_classes = [permissions.AllowAny]

class ServiceTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """List service types"""
    queryset = ServiceTypes.objects.all()
    serializer_class = ServiceTypeSerializer
    permission_classes = [permissions.AllowAny]

class SpeciesTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """List species categories"""
    queryset = SpeciesTypes.objects.all()
    serializer_class = SpeciesTypeSerializer
    permission_classes = [permissions.AllowAny]