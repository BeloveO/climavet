from django.shortcuts import render
from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from .models import ResourceChecklist, ChecklistTemplate, ClinicResourceChecklist, ResourceChecklistItem
from .serializers import ResourceChecklistSerializer, ResourceChecklistItemSerializer, ChecklistTemplateSerializer, ClinicResourceChecklistSerializer
from disasterplans.models import DisasterPlan, DisasterType
from clinics.models import Clinic
from .services.checklist_generator import ChecklistGenerator
from rest_framework.decorators import action

# Create your views here.

class ResourceChecklistViewSet(viewsets.ModelViewSet):
    queryset = ResourceChecklist.objects.all()
    serializer_class = ResourceChecklistSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        Optionally restricts the returned resource checklists to a given clinic or disaster type,
        by filtering against query parameters in the URL.

        :return: A queryset of ResourceChecklist instances filtered by clinic and/or disaster type if specified.
        """
        queryset = super().get_queryset()
        clinic_id = self.request.query_params.get('clinic')
        disaster_type = self.request.query_params.get('disaster_type')
        
        if clinic_id:
            queryset = queryset.filter(clinic_id=clinic_id)
        if disaster_type:
            queryset = queryset.filter(disaster_plan__disaster_type__category=disaster_type)
        
        return queryset
    
    @action(detail=False, methods=['post'], url_path='generate', permission_classes=[permissions.AllowAny])
    def generate(self, request, *args, **kwargs):
        """
        Generate a resource checklist for a given clinic and disaster plan.

        :param request: The HTTP request containing the clinic ID and disaster plan ID.
        :return: A response containing the generated resource checklist or an error message if generation fails.
        """
        data = request.data
        clinic_id = data.get('clinic')
        disaster_plan_id = data.get('disaster_plan')
        
        try:
            clinic = Clinic.objects.get(id=clinic_id)
        except Clinic.DoesNotExist:
            return Response({'error': 'Clinic not found'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            disaster_plan = DisasterPlan.objects.get(id=disaster_plan_id)
        except DisasterPlan.DoesNotExist:
            return Response({'error': 'Disaster Plan not found'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            resource_checklist = ChecklistGenerator.generate_checklist(clinic, disaster_plan)
            serializer = ResourceChecklistSerializer(resource_checklist)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], url_path='regenerate', permission_classes=[permissions.AllowAny])
    def regenerate(self, request, pk=None):
        """
        Regenerate a resource checklist for a given clinic and disaster plan.

        :param request: The HTTP request containing the clinic ID and disaster plan ID.
        :param pk: The primary key of the resource checklist to regenerate.
        :return: A response containing the regenerated resource checklist or an error message if regeneration fails.
        """
        try:
            checklist = self.get_object()
            clinic = checklist.clinic
            disaster_plan = checklist.disaster_plan

            ChecklistGenerator.delete_checklist(checklist)
            new_checklist = ChecklistGenerator.generate_checklist(clinic, disaster_plan)
            serializer = ResourceChecklistSerializer(new_checklist)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='items', permission_classes=[permissions.AllowAny])
    def items(self, request, pk=None):
        """
        Retrieve the items associated with a specific resource checklist.

        :param request: The HTTP request.
        :param pk: The primary key of the resource checklist for which to retrieve items.
        :return: A response containing the list of items in the specified resource checklist or an error message if retrieval fails.
        """
        try:
            checklist = self.get_object()
            items = checklist.items.all()
            serializer = ResourceChecklistItemSerializer(items, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ResourceChecklist.DoesNotExist:
            return Response({'error': 'Resource Checklist not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='mark_reviewed', permission_classes=[permissions.AllowAny])   
    def mark_reviewed(self, request, pk=None):
        """
        Mark a resource checklist as reviewed.

        :param request: The HTTP request.
        :param pk: The primary key of the resource checklist to mark as reviewed.
        :return: A response indicating success or failure of the operation.
        """
        try:
            checklist = self.get_object()
            checklist.is_reviewed = True
            checklist.save()
            return Response({'message': 'Resource Checklist marked as reviewed'}, status=status.HTTP_200_OK)
        except ResourceChecklist.DoesNotExist:
            return Response({'error': 'Resource Checklist not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, methods=['post'], url_path='mark_completed', permission_classes=[permissions.AllowAny])
    def mark_completed(self, request, pk=None):
        """
        Mark a resource checklist as completed.

        :param request: The HTTP request.
        :param pk: The primary key of the resource checklist to mark as completed.
        :return: A response indicating success or failure of the operation.
        """
        try:
            checklist = self.get_object()
            checklist.is_completed = True
            checklist.save()
            return Response({'message': 'Resource Checklist marked as completed'}, status=status.HTTP_200_OK)
        except ResourceChecklist.DoesNotExist:
            return Response({'error': 'Resource Checklist not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'], url_path="export_csv", permission_classes=[permissions.AllowAny])
    def export_csv(self, request, pk=None):
        """
        Export the resource checklist items as a CSV file.

        :param request: The HTTP request.
        :param pk: The primary key of the resource checklist to export.
        :return: A response containing the CSV file or an error message if export fails.
        """
        try:
            checklist = self.get_object()
            items = checklist.items.all()
            # Logic to generate CSV from items goes here
            csv_data = "name,description,quantity_needed,unit_of_measure,category,priority,is_essential\n"
            for item in items:
                csv_data += f"{item.name},{item.description},{item.quantity_needed},{item.unit_of_measure},{item.category},{item.priority},{item.is_essential}\n"
            response = Response(csv_data, content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{checklist.name}_items.csv"'
            return response
        except ResourceChecklist.DoesNotExist:
            return Response({'error': 'Resource Checklist not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, methods=['get'], url_path='export_pdf', permission_classes=[permissions.AllowAny])
    def export_pdf(self, request, pk=None):
        """
        Export the resource checklist items as a PDF file.

        :param request: The HTTP request.
        :param pk: The primary key of the resource checklist to export.
        :return: A response containing the PDF file or an error message if export fails.
        """
        try:
            checklist = self.get_object()
            items = checklist.items.all()
            # Logic to generate PDF from items goes here
            # This is a placeholder implementation, replace with actual PDF generation logic
            pdf_content = f"Resource Checklist: {checklist.name}\n\n"
            for item in items:
                pdf_content += f"Name: {item.name}\nDescription: {item.description}\nQuantity Needed: {item.quantity_needed} {item.unit_of_measure}\nCategory: {item.category}\nPriority: {item.priority}\nEssential: {item.is_essential}\n\n"
            response = Response(pdf_content, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{checklist.name}_items.pdf"'
            return response
        except ResourceChecklist.DoesNotExist:
            return Response({'error': 'Resource Checklist not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class ResourceChecklistItemViewSet(viewsets.ModelViewSet):
    queryset = ResourceChecklistItem.objects.all()
    serializer_class = ResourceChecklistItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        Optionally restricts the returned resource checklist items to a given checklist,
        by filtering against a query parameter in the URL.

        :return: A queryset of ResourceChecklistItem instances filtered by checklist if specified.
        """
        queryset = super().get_queryset()
        checklist_id = self.request.query_params.get('checklist')
        
        if checklist_id:
            queryset = queryset.filter(checklist_id=checklist_id)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save()
    
    def perform_update(self, serializer):
        serializer.save()
    
    def perform_destroy(self, instance):
        instance.delete()

    @action(detail=True, methods=['post'], url_path='mark_completed', permission_classes=[permissions.AllowAny])
    def mark_item_completed(self, request, pk=None):
        """
        Mark a specific resource checklist item as completed.

        :param request: The HTTP request.
        :param pk: The primary key of the resource checklist item to mark as completed.
        :return: A response indicating success or failure of the operation.
        """
        try:
            item = self.get_object()
            item.is_completed = True
            item.save()
            return Response({'message': 'Resource Checklist Item marked as completed'}, status=status.HTTP_200_OK)
        except ResourceChecklistItem.DoesNotExist:
            return Response({'error': 'Resource Checklist Item not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, methods=['post'], url_path='mark_incomplete', permission_classes=[permissions.AllowAny])
    def mark_item_incomplete(self, request, pk=None):
        """
        Mark a specific resource checklist item as incomplete.

        :param request: The HTTP request.
        :param pk: The primary key of the resource checklist item to mark as incomplete.
        :return: A response indicating success or failure of the operation.
        """
        try:
            item = self.get_object()
            item.is_completed = False
            item.save()
            return Response({'message': 'Resource Checklist Item marked as incomplete'}, status=status.HTTP_200_OK)
        except ResourceChecklistItem.DoesNotExist:
            return Response({'error': 'Resource Checklist Item not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, methods=['post'], url_path='update_status', permission_classes=[permissions.AllowAny])
    def update_status(self, request, pk=None):
        """
        Update the status of a specific resource checklist item based on current inventory and needs.

        :param request: The HTTP request.
        :param pk: The primary key of the resource checklist item to update.
        :return: A response indicating success or failure of the operation.
        """
        try:
            item = self.get_object()
            item.update_status()
            return Response({'message': 'Resource Checklist Item status updated', 'status': item.status}, status=status.HTTP_200_OK)
        except ResourceChecklistItem.DoesNotExist:
            return Response({'error': 'Resource Checklist Item not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    
class ChecklistTemplateViewSet(viewsets.ModelViewSet):
    queryset = ChecklistTemplate.objects.all()
    serializer_class = ChecklistTemplateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()

class ClinicResourceChecklistViewSet(viewsets.ModelViewSet):
    queryset = ClinicResourceChecklist.objects.all()
    serializer_class = ClinicResourceChecklistSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()