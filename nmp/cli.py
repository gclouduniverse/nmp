import argparse

from nmp.package_builder import create_model
from nmp.package_deployer import deploy_model


def main():
    parser = argparse.ArgumentParser(prog="nmp",
                                     description="Notebooks Model Publisher")
    builder_group = parser.add_argument_group("builder")
    builder_group.add_argument("build", action="store_true", const=True,
                                default=False, dest="build",
                                help="Build Model")
    builder_group.add_argument("--tag", action="store_const", dest="tag",
                                help="Docker Tag To Build")
    builder_group.add_argument("--path", action="store_const", dest="path", default=".",
                                help="path with Notebook and other files")
    builder_group.add_argument("--notebook", action="store_const", dest="notebook",
                                help="notebook name (should be in the path)",
                                default="main.ipynb")
    deployer_group = parser.add_argument_group("deploy")
    deployer_group.add_argument("deploy", action="store_true", const=True,
                                default=False, dest="deploy",
                                help="Deploy The Model")
    deployer_group.add_argument("--tag", action="store_const", dest="tag",
                                help="Docker Tag To Deploy")
    deployer_group.add_argument("--project", action="store_const", dest="project",
                                help="GCP Project (Vertex AI API should be enabled)")
    deployer_group.add_argument("--location", action="store_const", dest="location",
                                help="Vertex AI location")
    deployer_group.add_argument("--name", action="store_const", dest="name",
                                help="model name")

    args = parser.parse_args()

    if args.build:
        create_model(args.tag, args.path, args.notebook)
    if args.deploy:
        deploy_model(args.project, args.location, args.name, args.tag)