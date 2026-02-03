from pydantic import BaseModel
from typing import Optional

class ProjectFields(BaseModel):
    # BASIC INFO
    project_name: Optional[str]
    proponent_name: Optional[str]
    company_name: Optional[str]

    # TECHNICAL
    capacity_mw: Optional[float]
    production_capacity: Optional[str]
    raw_material: Optional[str]

    # FINANCIAL
    total_investment_cr: Optional[float]
    land_cost_cr: Optional[float]
    equipment_cost_cr: Optional[float]

    # LOCATION
    plot_area_ha: Optional[float]
    latitude: Optional[float]
    longitude: Optional[float]
    state: Optional[str]
    district: Optional[str]

    # ENVIRONMENT (examples)
    water_requirement_kld: Optional[float]
    power_requirement_mw: Optional[float]

    # 👉 ADD REMAINING FIELDS TILL 185
