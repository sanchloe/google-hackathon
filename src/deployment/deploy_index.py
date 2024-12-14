from google.cloud import aiplatform
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()

UID = datetime.now().strftime("%m%d%H%M")
PROJECT_ID = os.getenv("PROJECT_ID")
REGION = os.getenv("REGION")
DIMENSIONS = 768
APPROXIMATE_NEIGHBORS_COUNT = 10
DISTANCE_MEASURE_TYPE = "DOT_PRODUCT_DISTANCE"
INDEX_UPDATE_METHOD = "STREAM_UPDATE"
DISPLAY_NAME = f"resources-index-{UID}"
DEPLOYED_INDEX_ID = f"resources_deployed_{UID}"

aiplatform.init(project=PROJECT_ID, location=REGION)

def create_index(display_name, dimensions, neighbors_count, distance_measure, update_method):
    """Create a Matching Engine Index."""
    print(f"Creating Matching Engine Index: {display_name}")
    return aiplatform.MatchingEngineIndex.create_tree_ah_index(
        display_name=display_name,
        dimensions=dimensions,
        approximate_neighbors_count=neighbors_count,
        distance_measure_type=distance_measure,
        index_update_method=update_method,
    )

def create_endpoint(display_name):
    """Create a Matching Engine Index Endpoint."""
    print(f"Creating Matching Engine Index Endpoint: {display_name}")
    return aiplatform.MatchingEngineIndexEndpoint.create(
        display_name=f"{display_name}-endpoint", public_endpoint_enabled=True
    )

def deploy_index(endpoint, index, deployed_index_id):
    """Deploy an index to an endpoint."""
    print(f"Deploying Index: {deployed_index_id}")
    return endpoint.deploy_index(index=index, deployed_index_id=deployed_index_id)

if __name__ == "__main__":

    my_index = create_index(
        display_name=DISPLAY_NAME,
        dimensions=DIMENSIONS,
        neighbors_count=APPROXIMATE_NEIGHBORS_COUNT,
        distance_measure=DISTANCE_MEASURE_TYPE,
        update_method=INDEX_UPDATE_METHOD,
    )

    my_index_endpoint = create_endpoint(DISPLAY_NAME)

    deployed_index = deploy_index(
        endpoint=my_index_endpoint,
        index=my_index,
        deployed_index_id=DEPLOYED_INDEX_ID,
    )

    print("Index successfully deployed")
