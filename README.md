# Sbom Scanner Microservice

This Rest API Service download SPDX sbom of Redhat products, and get details of components from it.

## Quick Start

1. Build the container image
```shell
podman build -t quay.io/your_name/sbom-scanner:1.0.0 .
```

2. Run the service
```shell
podman run -p 8081:8081 quay.io/your_name/sbom-scanner:1.0.0 .
```

3. For documentation of the service, visit the Swagger UI of the service
```shell
xdg-open http://localhost:8081/openapi/swagger
```