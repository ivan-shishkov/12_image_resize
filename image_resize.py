import argparse
import sys

from PIL import Image


def resize_image(path_to_original, path_to_result):
    pass


def parse_command_line_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        'filename',
        help='a image file for resizing (should be either JPEG or PNG)',
        type=str,
    )

    parser.add_argument(
        '--width',
        help='a width of output image file (in pixels)',
        default=0,
        type=int,
    )

    parser.add_argument(
        '--height',
        help='a height of output image file (in pixels)',
        default=0,
        type=int,
    )

    parser.add_argument(
        '--scale',
        help='a scaling coefficient of output image file (should be > 0)',
        default=0.0,
        type=float,
    )

    parser.add_argument(
        '--output',
        help='a path for saving of output image file',
        default='',
        type=str,
    )

    command_line_arguments = parser.parse_args()

    return command_line_arguments


def main():
    command_line_arguments = parse_command_line_arguments()

    filename = command_line_arguments.filename

    try:
        source_image = Image.open(filename)
    except FileNotFoundError:
        sys.exit('File not found')
    except OSError:
        sys.exit('This file is not a image')


if __name__ == '__main__':
    main()
