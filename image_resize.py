import argparse
import sys
import os.path
from pathlib import Path

from PIL import Image


def calculate_output_image_size(source_image_size, given_size, scale):
    source_image_width, source_image_height = source_image_size
    given_width, given_height = given_size

    output_image_size = None

    if scale:
        output_image_size = (
            round(source_image_width * scale),
            round(source_image_height * scale),
        )
        return output_image_size

    if given_width and given_height:
        output_image_size = (
            given_width,
            given_height,
        )
    elif given_width:
        output_image_size = (
            given_width,
            round((source_image_height * given_width) / source_image_width),
        )
    elif given_height:
        output_image_size = (
            round((given_height * source_image_width) / source_image_height),
            given_height,
        )

    return output_image_size


def is_same_images_proportions(
        source_image_size, output_image_size, permissible_error=0.01):
    source_image_width, source_image_height = source_image_size
    output_image_width, output_image_height = output_image_size

    source_image_proportions = source_image_width / source_image_height
    output_image_proportions = output_image_width / output_image_height

    return abs(source_image_proportions - output_image_proportions
               ) < permissible_error


def get_command_line_arguments_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        'filepath',
        help='a path to the source image file',
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
        help='a directory for saving of output image file',
        default='',
        type=str,
    )

    return parser


def check_correct_optional_arguments(
        parser, width, height, scale, output_path):
    if not any((width, height, scale)):
        parser.error(
            'Parameters for resizing are not given',
        )
    if scale and (width or height):
        parser.error(
            'You should given either scale or size (width and/or height)',
        )
    if output_path and not os.path.isdir(output_path):
        parser.error(
            'Output path is not a directory or not exists',
        )


def create_output_image_filename(source_image_filepath, output_image_size):
    output_image_width, output_image_height = output_image_size

    base_filename, extension = Path(source_image_filepath).name.split('.')

    return '{}__{}x{}.{}'.format(
        base_filename, output_image_width, output_image_height, extension)


def create_output_image_filepath(
        source_image_filepath, output_directory, output_image_filename):
    source_image_directory = Path(source_image_filepath).parent

    if output_directory:
        output_image_filepath = Path(output_directory) / output_image_filename
    else:
        output_image_filepath = source_image_directory / output_image_filename

    return output_image_filepath


def load_source_image(source_image_filepath):
    try:
        source_image = Image.open(source_image_filepath)
        return source_image
    except OSError:
        return None


def save_image_to_file(output_image, output_image_filepath, image_format):
    try:
        output_image.save(output_image_filepath, format=image_format)
        return True
    except PermissionError:
        return False


def main():
    parser = get_command_line_arguments_parser()

    command_line_arguments = parser.parse_args()

    source_image_filepath = command_line_arguments.filepath
    width = command_line_arguments.width
    height = command_line_arguments.height
    scale = command_line_arguments.scale
    output_directory = command_line_arguments.output

    check_correct_optional_arguments(
        parser, width, height, scale, output_directory,
    )

    source_image = load_source_image(source_image_filepath)

    if not source_image:
        sys.exit('Source file not found or is not a image file')

    output_image_size = calculate_output_image_size(
        source_image_size=source_image.size,
        given_size=(width, height),
        scale=scale,
    )

    if not is_same_images_proportions(
            source_image_size=source_image.size,
            output_image_size=output_image_size):
        print('Warning: proportions of source image will not be saved')

    output_image = source_image.resize(output_image_size)

    output_image_filename = create_output_image_filename(
        source_image_filepath=source_image_filepath,
        output_image_size=output_image_size,
    )

    output_image_filepath = create_output_image_filepath(
        source_image_filepath=source_image_filepath,
        output_directory=output_directory,
        output_image_filename=output_image_filename,
    )

    if not save_image_to_file(
            output_image, output_image_filepath, source_image.format):
        sys.exit('Could not save image to given directory. Permission denied.')

    print('Resized image successfully saved to {}'.format(
        output_image_filepath,
    ))


if __name__ == '__main__':
    main()
