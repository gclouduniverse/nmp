import os
import shutil
from typing import Optional
from vaip import model_builder
from vaip import constants

import docker
import tempfile

from nbformat import read


def create_model(tag: str,
                 src_folder: Optional[str],
                 main_nb_name: Optional[str] = "main.ipynb"):
    with tempfile.TemporaryDirectory() as tmpdir:
        target_dir = os.path.join(
            tmpdir, constants.TEMP_DIR_FOR_BUILDING_CONTAINERS)
        prediction_file = os.path.join(
            target_dir, constants.MAIN_PREDICTION_FILE)
        shutil.copytree(src_folder, target_dir, dirs_exist_ok=True)
        print("Extracting prediction logic from the notebok")
        _extract_prediction_logic(main_nb_name, prediction_file)
        model_builder.build_model(tag, target_dir)


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

