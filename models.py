from pydantic import BaseModel, Field
from typing import Annotated

class PredictFeatures(BaseModel):
    epdm_content: Annotated[float,Field(..., description="EPDM content")]
    talc_content: Annotated[float,Field(..., description="TALC content")]
    processing_temp: Annotated[float,Field(..., description="Processing Temperature")]
    screw_speed_rpm: Annotated[float,Field(..., description="Screw Speed in RM")]

