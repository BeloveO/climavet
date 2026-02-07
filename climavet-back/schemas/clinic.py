from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional, List
from datetime import date
from enum import Enum

# Enums for clinic types and services
class ClinicType(str, Enum):
    PRIVATE = "private"
    CORPORATE = "corporate"
    MOBILE = "mobile"
    ANIMAL_SHELTER = "animal_shelter"
    TEACHING_HOSPITAL = "teaching_hospital"
    WILDLIFE_FACILITY = "wildlife_facility"

class ServiceType(str, Enum):
    GENERAL = "general"
    EMERGENCY_OR_CRITICAL = "emergency_or_critical"
    URGENT = "urgent"
    SPECIALTY = "specialty"

class SpeciesType(str, Enum):
    SMALL_ANIMAL = "small_animal"
    EQUINE = "equine"
    FELINE = "feline"
    MIXED = "mixed"
    EXOTIC_AND_AVIAN = "exotic_and_avian"

# Clinic request schema
class ClinicBase(BaseModel):
    name: str = Field(..., description="Name of the clinic")
    address: str = Field(..., description="Physical address of the clinic")
    city: str = Field(..., description="City where the clinic is located")
    province: str = Field(..., description="Province or state of the clinic")
    postal_code: str = Field(..., description="Postal or ZIP code of the clinic")
    email: Optional[EmailStr] = Field(None, description="Contact email of the clinic")
    phone_number: Optional[str] = Field(None, description="Contact phone number of the clinic")
    clinic_type: ClinicType = Field(..., description="Type of the clinic")
    services_offered: List[ServiceType] = Field(..., description="List of services offered by the clinic")
    species_treated: List[SpeciesType] = Field(..., description="List of species treated at the clinic")
    latitude: Optional[float] = Field(None, description="Latitude coordinate of the clinic")
    longitude: Optional[float] = Field(None, description="Longitude coordinate of the clinic")

class ClinicCreate(ClinicBase):
    pass

class ClinicUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Name of the clinic")
    address: Optional[str] = Field(None, description="Physical address of the clinic")
    city: Optional[str] = Field(None, description="City where the clinic is located")
    province: Optional[str] = Field(None, description="Province or state of the clinic")
    postal_code: Optional[str] = Field(None, description="Postal or ZIP code of the clinic")
    email: Optional[EmailStr] = Field(None, description="Contact email of the clinic")
    phone_number: Optional[str] = Field(None, description="Contact phone number of the clinic")
    clinic_type: Optional[ClinicType] = Field(None, description="Type of the clinic")
    services_offered: Optional[List[ServiceType]] = Field(None, description="List of services offered by the clinic")
    species_treated: Optional[List[SpeciesType]] = Field(None, description="List of species treated at the clinic")
    latitude: Optional[float] = Field(None, description="Latitude coordinate of the clinic")
    longitude: Optional[float] = Field(None, description="Longitude coordinate of the clinic")

# Response schema with metadata
class ClinicInDB(ClinicBase):
    id: int = Field(..., description="Unique identifier of the clinic")
    createdAt: date = Field(..., description="Date when the clinic record was created")
    updatedAt: date = Field(..., description="Date when the clinic record was last updated")

    class Config:
        orm_mode = True

class ClinicResponse(ClinicInDB):
    pass

class ClinicWithRelations(ClinicInDB):
    # Placeholder for related entities e.g risk assessments etc.
    risk_assessments: Optional[List[dict]] = Field(None, description="List of risk assessments related to the clinic")
    disaster_plans: Optional[List[dict]] = Field(None, description="List of disaster plans related to the clinic")
    resource_checklists: Optional[List[dict]] = Field(None, description="List of resource checklists related to the clinic")