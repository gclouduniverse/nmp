# Notebook Model Packer

Simple SDK and CLI that allows to extract prediction logic directly from the Jupyter Notebooks and deploy them on the GCP Vertex AI Prediction service.

# Usage Example

Before using make sure that following requirements are met:
* Docker installed
* Python 3.8+

Install it:

```bash
pip3 install -U nmp
```

In the notebook, create a cell that includes prediction logic. Requirements for the cell:

* should be self contained (you can restart the kernel and check is the cell still can be executed)
* should include prediciton function (more on this later)
* should have metadata: "deployment_target": "prediction" (this part is critical, this is how nmp found which cell to use)

prediction function shuold look like this:

```python
def predict(instance, **kwarg):
  pass
```

in the same cell you *can* have:
* tests for this funciton
* other functions

you aslo can read any artifacts in the same folder (or any folder below) as your notebook, this example will work:

```python
def predict(instance, **kwarg):
  return open("test_message.txt", "r").read()
```

If all requirenments are met one can deploy your model in two setps:

build model:
```bash
TAG=... # your tag that you have permissions to push, example: us.gcr.io/ml-lab-152505/model-poc2
PATH_TO_PROJECT=... # example: . . all files from the folder will be copoied over to the model container
NOTEBOOK_PATH=... # example: 10_nlp.ipynb. Relative path to the notebook with the prediciton logic in the project path
nmp build --tag "${TAG}" --path "${PATH_TO_PROJECT}" --notebook "${NOTEBOOK_PATH}"
```

test it, start container locally:

```bash
TAG=... # your tag that you can push somewhere, e.g."us.gcr.io/ml-lab-152505/model-poc"
docker run -p 8080:8080 "${TAG}"
```

run the prediction:
```bash
curl -X POST -d '{"parameters": {}, "instances": ["1", "2"]}' -H "Content-Type: application/json" http://localhost:8080/predict
```

you should see:

```
{"predictions":["Hello Vertex","Hello Vertex"]}
```

As soon as model is create you can deploy it to Vertex AI either by ```gcloud``` or ```vaip``` or with ```nmp```:

```bash
TAG=... # your tag that you have permissions to push, example: us.gcr.io/ml-lab-152505/model-poc2
GCP_PROJECT=...
GCP_LOCATION=...
GCP_MODEL_NAME=...
nmp deploy --project "${GCP_PROJECT}" --location "${GCP_LOCATION}" --name "${GCP_MODEL_NAME}" --tag "${TAG}"
```

If everything is correct you should be able to test it like this:

```bash
curl \
-X POST \
-H "Authorization: Bearer $(gcloud auth print-access-token)" \
-H "Content-Type: application/json" \
https://us-west1-aiplatform.googleapis.com/v1/projects/${PROJECT_ID}/locations/us-west1/endpoints/${ENDPOINT_ID}:predict \ 
-d '{"parameters": {}, "instances": ["1", "2"]}'
{
  "predictions": [
    "1",
    "1"
  ],
  "deployedModelId": "..."
}
```

# Details

It is based on the High level GCP Vertex AI Prediction SDK: vaip.
