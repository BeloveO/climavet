from django.db import models
from disasterplans.models import DisasterType, DisasterPlan
from clinics.models import Clinic
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

# Create your models here.
class ChecklistTemplate(models.Model):
    # Predefined checklist templates for different disaster types
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    disaster_type = models.ForeignKey(DisasterType, on_delete=models.CASCADE)
    category = models.CharField(max_length=100, 
                                choices=[('RECORDS_AND_DOCUMENTS', 'Records and Documents'),
                                         ('MEDICAL_SUPPLIES', 'Medical Supplies'),
                                         ('SUSTENANCE', 'Sustenance'),
                                         ('EVACUATION_HANDLING_AND_TRANSPORTATION_RESOURCES', 'Evacuation Handling and Transportation Resources'),
                                         ('SANITATION', 'Sanitation'),
                                         ('COMMUNICATION_DEVICES_AND_OPERATIONAL_TOOLS', 'Communication Devices and Operational Tools'), 
                                         ('FACILITY_AND_SAFETY_GEAR', 'Facility and Safety Gear'), 
                                         ('SHELTER_AND_BEDDING', 'Shelter and Bedding'), 
                                         ('STAFF_AND_OWNER_RESOURCES', 'Staff and Owner Resources')])
    is_system_template = models.BooleanField(default=False)  # Indicates if this is a system template or a custom one. system templates are predefined and cannot be edited by users.

    def __str__(self):
        return f"{self.name} ({self.disaster_type.name})"

class ResourceChecklistItem(models.Model):
    # Individual checklist items that belong to a checklist template
    UNIT_CHOICES = [
        ('BOX', 'Box'),
        ('BAG', 'Bag'),
        ('BOTTLE', 'Bottle'),
        ('CANISTER', 'Canister'),
        ('CASE', 'Case'),
        ('PACK', 'Pack'),
        ('LITER', 'Liter'),
        ('GALLON', 'Gallon'),
        ('KILOGRAM', 'Kilogram'),
        ('GRAM', 'Gram'),
        ('ROLL', 'Roll'),
        ('TUBE', 'Tube'),
        ('UNIT', 'Unit'),
    ]
    checklist_template = models.ForeignKey(ChecklistTemplate, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=100, 
                                choices=[('RECORDS_AND_DOCUMENTS', 'Records and Documents'),
                                         ('MEDICAL_SUPPLIES', 'Medical Supplies'),
                                         ('SUSTENANCE', 'Sustenance'),
                                         ('EVACUATION_HANDLING_AND_TRANSPORTATION_RESOURCES', 'Evacuation Handling and Transportation Resources'),
                                         ('SANITATION', 'Sanitation'),
                                         ('COMMUNICATION_DEVICES_AND_OPERATIONAL_TOOLS', 'Communication Devices and Operational Tools'), 
                                         ('FACILITY_AND_SAFETY_GEAR', 'Facility and Safety Gear'), 
                                         ('SHELTER_AND_BEDDING', 'Shelter and Bedding'), 
                                         ('STAFF_AND_OWNER_RESOURCES', 'Staff and Owner Resources')])
    unit_of_measure = models.CharField(max_length=20, choices=UNIT_CHOICES, default='UNIT')
    units_needed = models.IntegerField(default=1)
    current_units = models.IntegerField(default=0)
    storage_recommendations = models.TextField(blank=True, null=True)
    is_essential = models.BooleanField(default=False)  # Indicates if this item is essential
    status = models.CharField(max_length=20, choices=[('IN_STOCK', 'In Stock'), 
                                                      ('LOW_STOCK', 'Low Stock'), 
                                                      ('OUT_OF_STOCK', 'Out of Stock'),
                                                      ('ORDERED', 'Ordered'),
                                                      ('NOT_NEEDED', 'Not Needed')], 
                                                      default='OUT_OF_STOCK') # Status of the item based on current inventory and needs
    priority = models.CharField(max_length=20, choices=[('CRITICAL', 'Critical'),
                                                        ('HIGH', 'High'),
                                                        ('MEDIUM', 'Medium'),
                                                        ('LOW', 'Low')],
                                                        default='MEDIUM') # Priority level for acquiring this item
    
    # Optional fields for tracking inventory and procurement
    last_updated = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, null=True)
    supplier_info = models.TextField(blank=True, null=True)  # Information about suppliers for this item
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Estimated cost for acquiring the needed units
    expiry_date = models.DateField(blank=True, null=True)  # Expiry date for perishable items
    storage_location = models.CharField(max_length=255, blank=True, null=True)  # Where the item is stored in the clinic
    species_specific = models.BooleanField(default=False)  # Indicates if this item is specific to certain species
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['priority', 'name']  # Order items by priority and then by name

    def update_status(self):
        # Method to update the status of the item based on current inventory and needs
        if self.current_units >= self.units_needed:
            self.status = 'IN_STOCK'
        elif 0 < self.current_units < self.units_needed:
            self.status = 'LOW_STOCK'
        else:
            self.status = 'OUT_OF_STOCK'
        self.save()

class ClinicResourceChecklist(models.Model):
    # A custom checklist for a specific clinic and disaster plan, based on a template
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='resource_checklists')
    disaster_plan = models.ForeignKey(DisasterPlan, on_delete=models.CASCADE, related_name='resource_checklists')
    checklist_template = models.ForeignKey(ChecklistTemplate, on_delete=models.SET_NULL, null=True, blank=True)  # The template this checklist is based on
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    last_reviewed = models.DateTimeField(blank=True, null=True)  # When the checklist was last reviewed and updated
    review_frequency = models.CharField(max_length=20, choices=[('NONE', 'None'),
                                                                ('WEEKLY', 'Weekly'),
                                                                ('BIWEEKLY', 'Biweekly'),
                                                                ('MONTHLY', 'Monthly'),
                                                                ('QUARTERLY', 'Quarterly'),
                                                                ('ANNUALLY', 'Annually'),
                                                                ('BIANNUALLY', 'Biannually')], default='NONE')  # How often the checklist should be reviewed and updated
    review_notes = models.TextField(blank=True, null=True)  # Notes from the last review
    is_active = models.BooleanField(default=True)  # Indicates if this checklist is currently active
    is_completed = models.BooleanField(default=False)  # Indicates if the checklist has been completed for the current disaster plan
    completion_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # Percentage of checklist items that have been completed

    class Meta:
        ordering = ['-created_at']  # Order by most recently created

    def calculate_completion_percentage(self):
        # Method to calculate the completion percentage based on the status of the checklist items
        total_items = self.items.count()
        if total_items == 0:
            self.completion_percentage = 100.00
        else:
            completed_items = self.items.filter(status='IN_STOCK').count()
            self.completion_percentage = (completed_items / total_items) * 100
        self.save()
    
    def review_alarm(self):
        # Method to check if the checklist is due for review based on the review frequency and last reviewed date
        if self.review_frequency == 'NONE':
            return False
        if not self.last_reviewed:
            return True  # If it has never been reviewed, it's due for review
        now = timezone.now()
        next_review_date = None
        if self.review_frequency == 'WEEKLY':
            next_review_date = self.last_reviewed + timedelta(weeks=1)
        elif self.review_frequency == 'BIWEEKLY':
            next_review_date = self.last_reviewed + timedelta(weeks=2)
        elif self.review_frequency == 'MONTHLY':
            next_review_date = self.last_reviewed + timedelta(days=30)
        elif self.review_frequency == 'QUARTERLY':
            next_review_date = self.last_reviewed + timedelta(days=90)
        elif self.review_frequency == 'ANNUALLY':
            next_review_date = self.last_reviewed + timedelta(days=365)
        elif self.review_frequency == 'BIANNUALLY':
            next_review_date = self.last_reviewed + timedelta(days=182)
        
        return now >= next_review_date if next_review_date else False

    def __str__(self):
        return f"{self.name} - {self.clinic.name} ({self.disaster_plan.name})"