from typing import Optional

from pydantic import BaseModel, Field


class ProductIdPath(BaseModel):
    product_id: str = Field(..., description='Product Id', json_schema_extra={"example": "openshift:4.15"})


class ComponentQuery(BaseModel):
    component: Optional[str] = Field("", description='Component Name in Product Sbom',
                                     json_schema_extra={
                                         "example": "registry.redhat.io/openshift4/oc-mirror-plugin-rhel8"})
