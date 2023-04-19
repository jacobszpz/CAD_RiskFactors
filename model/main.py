import argparse
from dataset import Dataset

def main(folder_path: str) -> int:
    """
    Create a dataset from the directory

    Args:
        folder_path (str): The path to the folder to load.

    Returns:
        int: The return code of the function (always 0 in this implementation).
    """

    data = Dataset(folder_path)
    return 0

if __name__ == '__main__':
    # create the argument parser
    parser = argparse.ArgumentParser(description='Iterate over files in a folder')
    parser.add_argument('folder', type=str, help='the path to the folder')

    # parse the arguments
    args = parser.parse_args()

    # get the path to the folder from the parsed arguments
    folder_path: str = args.folder

    # call the main function and raise SystemExit with its return value
    raise SystemExit(main(folder_path))

