import os
import shutil
from typing import Optional

import docker
import tempfile

from nbformat import read


def create_model(tag: str,
                 src_folder: Optional[str],
                 main_nb_name: Optional[str] = "main.ipynb"):
    with tempfile.TemporaryDirectory() as tmpdir:
        target_dir = os.path.join(tmpdir, "container/")
        prediction_file = os.path.join(target_dir, "prediction.py")
        print("Preparing Docker env")
        _move_docker_content_to_temp_dir(target_dir)
        print("Moving content of the current dir to the temp location")
        shutil.copytree(src_folder, target_dir, dirs_exist_ok=True)
        print("Extracting prediction logic from the notebok")
        _extract_prediction_logic(main_nb_name, prediction_file)
        print("Building and pushing docker container")
        _build_and_push_docker(target_dir, tag)
        print("done")


def _move_docker_content_to_temp_dir(target_dir):
    src = os.path.join(os.path.dirname(__file__), "container/")
    shutil.copytree(src, target_dir, dirs_exist_ok=True)


def _extract_prediction_logic(nb_file_name, target_file):
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


def _build_and_push_docker(path, tag):
    client = docker.from_env()
    client.images.build(path=path, tag=tag)
    client.images.push(tag)


# create_model("us.gcr.io/ml-lab-152505/model-poc", main_nb_name="test.ipynb")
# create_model()
