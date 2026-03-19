from pydantic import BaseModel, Field
from typing import Optional

class EChallanData(BaseModel):
    challan_number: str = Field(description="The unique identification number of the challan")
    vehicle_number: str = Field(description="Registration number of the vehicle")
    violation_date: str = Field(description="Date and time when the violation occurred")
    amount: float = Field(description="Total fine amount in numeric format")
    offence_description: str = Field(description="Brief description of the traffic law broken")
    payment_status: str = Field(description="Current status (e.g., Paid, Pending, Unpaid)")

class NAPermissionData(BaseModel):
    survey_number: str = Field(description="The specific land survey number")
    land_area: str = Field(description="The total area of the land mentioned in the document")
    owner_name: str = Field(description="Name of the primary land owner or applicant")
    order_date: str = Field(description="The date the NA permission order was issued")
    authority_details: str = Field(description="The office or officer who granted the permission")

class AuditLogEntry(BaseModel):
    """Schema for the internal database audit trail"""
    filename: str
    doc_type: str
    raw_prompt: str
    raw_response: str
    status: str  # Success or Failure