import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-s", "--saved-exts", action="store_true")
parser.add_argument("-n", "--normal-flow", action="store_true")
parser.add_argument("-i", "--input-file",
                    type=str,
                    required=True,
                    help="File path for xml file saved from Burp")
parser.add_argument("-o", "--output-folder", default=".",
                    type=str,
                    help="Folder to save analyze files")


args = parser.parse_args()
