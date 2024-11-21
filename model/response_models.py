from typing import Any

from pydantic import BaseModel, Field


class SbomPayload(BaseModel):
    content: str = Field(None, description='Sbom Json or component in Sbom Json')


class SbomResponsePayload(BaseModel):
    def __init__(self, content: str, **data: Any) -> None:
        super().__init__(**data)
        self.data = content

    data: SbomPayload = Field(None)

    model_config = dict(
        openapi_extra={
            "examples": {
                "Example 01": {
                    "summary": "An example",
                    "value": {
                        "SPDXID": "SPDXRef-e35e1a9f-471d-45ae-8165-1250d7fb9349",
                        "copyrightText": "NOASSERTION",
                        "downloadLocation": "registry.redhat.io/openshift4/oc-mirror-plugin-rhel8:v4.14.0-202410182001.p0.ga0733c1.assembly.stream.el8",
                        "externalRefs": [
                            {
                                "referenceCategory": "PACKAGE_MANAGER",
                                "referenceLocator": "pkg:oci/oc-mirror-plugin-rhel8@sha256:2c702c8921d9f1fe2be10177da677f6b2aea9417d5965a5a311d66d8b9b9d174?repository_url=registry.redhat.io/openshift4/oc-mirror-plugin-rhel8&tag=v4.14.0-202410182001.p0.ga0733c1.assembly.stream.el8",
                                "referenceType": "purl"
                            },
                            {
                                "referenceCategory": "SECURITY",
                                "referenceLocator": "cpe:/a:redhat:openshift:4.14::el8",
                                "referenceType": "cpe22Type"
                            }
                        ],
                        "filesAnalyzed": "false",
                        "homepage": "registry.redhat.io/openshift4/oc-mirror-plugin-rhel8",
                        "licenseConcluded": "NOASSERTION",
                        "licenseDeclared": "LicenseRef-0",
                        "name": "oc-mirror-plugin-rhel8",
                        "originator": "NOASSERTION",
                        "supplier": "Organization: Red Hat",
                        "versionInfo": "v4.14.0-202410182001.p0.ga0733c1.assembly.stream.el8"
                    }

                }

            }
        }
    )


class SbomResponse(SbomResponsePayload):

    def __init__(self, code: int, message: str,  **data: Any) -> None:
        super().__init__("", **data)
        self.code = code
        self.message = message

    code: int = Field(0, description="status code")
    message: str = Field("ok", description="exception information")

    model_config = dict(
        openapi_extra={
            "examples": {
                "Example 01": {
                    "code": 400,
                    "value": "Wrong product_id input format, must conform to regex pattern"
                },
                "Example 02": {
                    "code": 404,
                    "value": "Can't find Sbom for product openshift 4.13"
                }
            }
        }
    )
