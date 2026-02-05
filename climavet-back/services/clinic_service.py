from typing import List, Optional, Dict, Any
from database.prisma_client import database_manager
from schemas.clinic import ClinicCreate, ClinicUpdate, ClinicInDB
from prisma import Prisma
import logging

logger = logging.getLogger(__name__)

class ClinicService:
    def __init__(self, db_client: Prisma):
        self.db_client = db_client

    async def create_clinic(self, clinic_data: ClinicCreate) -> ClinicInDB:
        """Create a new clinic record in the database."""
        try:
            """check if clinic with same name and address exists"""
            existing_clinic = await self.db_client.clinic.find_unique(
                where={
                    "name": clinic_data.name,
                    "address": clinic_data.address
                }
            )
            if existing_clinic:
                raise ValueError("Clinic with the same name and address already exists.")
            
            created_clinic = await self.db_client.clinic.create(data=clinic_data.model_dump())
            logger.info(f"Clinic created with ID: {created_clinic.id}")
            return ClinicInDB(**created_clinic.dict())
        
        except Exception as e:
            logger.error(f"Error creating clinic: {e}")
            raise

    async def get_clinic(self, clinic_id: int) -> Optional[ClinicInDB]:
        """Retrieve a clinic record by its ID."""
        try:
            clinic = await self.db_client.clinic.find_unique(where={"id": clinic_id})
            if clinic:
                return ClinicInDB(**clinic.dict())
            return None
        except Exception as e:
            logger.error(f"Error retrieving clinic with ID {clinic_id}: {e}")
            return None
        
    async def update_clinic(self, clinic_id: int, clinic_data: ClinicUpdate) -> Optional[ClinicInDB]:
        """Update an existing clinic record."""
        clinic_dict = {k: v for k, v in clinic_data.model_dump().items() if v is not None}
        updated_clinic = await self.db_client.clinic.update(
            where={"id": clinic_id},
            data=clinic_dict
        )
        if updated_clinic:
            return ClinicInDB(**updated_clinic.dict())
        return None
    async def delete_clinic(self, clinic_id: int) -> bool:
        """Delete a clinic record by its ID."""
        try:
            await self.db_client.clinic.delete(where={"id": clinic_id})
            return True
        except Exception as e:
            logger.error(f"Error deleting clinic with ID {clinic_id}: {e}")
            return False
    async def list_clinics(self, skip: int = 0, limit: int = 100) -> List[ClinicInDB]:
        """List clinics with pagination."""
        clinics = await self.db_client.clinic.find_many(skip=skip, take=limit)
        return [ClinicInDB(**clinic.dict()) for clinic in clinics]
    

