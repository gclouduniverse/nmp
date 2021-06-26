import docker

from nbformat import read

def extract_prediction_logic(nb_file_name, target_file):
    notebook = read(nb_file_name, as_version=4.0)
    prediction_logic = _find_cell_with_prediction_logic(notebook)
    if not prediction_logic:
        raise RuntimeError("No prediction logic found in the notebook")
    with open(target_file, "w") as text_file:
        text_file.write(prediction_logic)


def _find_cell_with_prediction_logic(nb_object):
    for cell in nb_object["cells"]:
        if cell["cell_type"] == "code":
            if ("deployment_target" in cell["metadata"] and
                    cell["metadata"]["deployment_target"] == "prediction"):
                return cell["source"]
    return None


def build_docker(tag):
    client = docker.from_env()
    path = "container"
    client.images.build(path=path, tag=tag)
    client.images.push(tag)


build_docker("us.gcr.io/ml-lab-152505/model-poc")

