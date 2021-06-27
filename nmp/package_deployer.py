from typing import Optional, Dict, Sequence, Tuple

from google.cloud import aiplatform


def create_endpoint_sample(project: str, display_name: str, location: str):
    aiplatform.init(project=project, location=location)

    endpoint = aiplatform.Endpoint.create(
        display_name=display_name, project=project, location=location,
    )

    print(endpoint.display_name)
    print(endpoint.resource_name)
    return endpoint


def upload_model_sample(
    project: str,
    location: str,
    display_name: str,
    serving_container_image_uri: str,
):

    aiplatform.init(project=project, location=location)

    model = aiplatform.Model.upload(
        display_name=display_name,
        serving_container_image_uri=serving_container_image_uri,
        serving_container_predict_route="/predict",
        serving_container_health_route="/ping",
        serving_container_ports=[8080],
        sync=True,
    )

    model.wait()

    print(model.display_name)
    print(model.resource_name)
    return model


def deploy_model_with_automatic_resources_sample(
    project,
    location,
    model_name: str,
    endpoint: Optional[aiplatform.Endpoint] = None,
    deployed_model_display_name: Optional[str] = None,
):
    aiplatform.init(project=project, location=location)

    model = aiplatform.Model(model_name=model_name)

    model.deploy(
        endpoint=endpoint,
        deployed_model_display_name=deployed_model_display_name,
        traffic_percentage=100,
        machine_type="n1-standard-2",
        min_replica_count=1,
        max_replica_count=1,
        sync=True,
    )

    model.wait()

    print(model.display_name)
    print(model.resource_name)
    return model


# create_endpoint_sample("ml-lab-152505", "test-poc", "us-west1")
# projects/183488370666/locations/us-west1/endpoints/7882003035340144640
# upload_model_sample("ml-lab-152505", "us-west1", "test-poc", "us.gcr.io/ml-lab-152505/model-poc")
# projects/183488370666/locations/us-west1/models/2080170446635925504
deploy_model_with_automatic_resources_sample("ml-lab-152505", "us-west1", "projects/183488370666/locations/us-west1/models/2080170446635925504", deployed_model_display_name="test-poc")