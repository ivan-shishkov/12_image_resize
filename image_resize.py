import argparse
import sys
import os.path
from pathlib import Path

from PIL import Image


def calculate_output_image_size(source_image_size, given_size, scale):
    source_image_width, source_image_height = source_image_size

    given_width, given_height = given_size

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
    else:
        output_image_size = (0, 0)

    return output_image_size


def check_saving_images_proportions(
        source_image_size, output_image_size, permissible_error=0.01):
    source_image_width, source_image_height = source_image_size

    output_image_width, output_image_height = output_image_size

    source_image_proportions = source_image_width / source_image_height

    output_image_proportions = output_image_width / output_image_height

    return abs(source_image_proportions - output_image_proportions
               ) < permissible_error


def parse_command_line_arguments():
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
        help='a path for saving of output image file',
        default='',
        type=str,
    )

    command_line_arguments = parser.parse_args()

    return command_line_arguments


def check_correct_optional_arguments(width, height, scale, output_path):
    if not any((width, height, scale)):
        return 'Parameters for resizing are not given'

    if scale and (width or height):
        return 'You should given either scale or size (width and/or height)'

    if output_path and not os.path.isdir(output_path):
        return 'Output path is not a directory or not exists'


def create_output_image_filename(source_image_filepath, output_image_size):
    output_image_width, output_image_height = output_image_size

    base_filename, extension = Path(source_image_filepath).name.split('.')

    return '{}__{}x{}.{}'.format(
        base_filename, output_image_width, output_image_height, extension)


def create_output_image_filepath(
        source_image_filepath, output_directory, output_image_filename):
    source_image_directory = Path(source_image_filepath).parent

    if output_directory:
        output_image_filepath = os.path.join(
            output_directory,
            output_image_filename,
        )
    else:
        output_image_filepath = os.path.join(
            str(source_image_directory),
            output_image_filename,
        )

    return output_image_filepath


def main():
    command_line_arguments = parse_command_line_arguments()

    source_image_filepath = command_line_arguments.filepath
    width = command_line_arguments.width
    height = command_line_arguments.height
    scale = command_line_arguments.scale
    output_directory = command_line_arguments.output

    error_message = check_correct_optional_arguments(
        width, height, scale, output_directory,
    )

    if error_message:
        sys.exit(error_message)

    try:
        source_image = Image.open(source_image_filepath)
    except FileNotFoundError:
        sys.exit('File not found')
    except OSError:
        sys.exit('This file is not a image')

    output_image_size = calculate_output_image_size(
        source_image_size=source_image.size,
        given_size=(width, height),
        scale=scale,
    )

    if not check_saving_images_proportions(
            source_image_size=source_image.size,
            output_image_size=output_image_size):
        print('Warning: proportions of source image will not be saved')

    output_image = source_image.resize(output_image_size)

    output_image_filename = create_output_image_filename(
        source_image_filepath,
        output_image_size,
    )

    output_image_filepath = create_output_image_filepath(
        source_image_filepath,
        output_directory,
        output_image_filename,
    )

    try:
        output_image.save(output_image_filepath, format=source_image.format)
    except PermissionError:
        sys.exit('Permission denied to save image')


if __name__ == '__main__':
    main()
