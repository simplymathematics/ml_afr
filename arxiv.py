import argparse
from pathlib import Path
import os
import shutil
import tempfile
import logging

logger = logging.getLogger(__name__)



def create_tmp_directory(tmp_directory):
    logger.info('Creating temporary directory: ' + tmp_directory)
    os.makedirs(tmp_directory, exist_ok=True)


def copy_files_to_tmp_directory(tmp_directory):
    logger.info('Copying files to temporary directory: ' + tmp_directory)
    for filename in Path('.').glob('*'):
        if Path(filename).is_dir():
            logger.info(f"{filename} is a directory - skipping.")
        else:
            logger.info(f"Copying {filename} to tmp directory.")
            shutil.copy(filename, str(Path(tmp_directory, filename).resolve()))


def remove_unused_files(directory, logfile, enc, filetype=".eps"):
    logger.info('Removing unused files in directory: ' + directory)
    for filename in Path(directory).glob(f'*{filetype}'):
        if filename in open(logfile, encoding=enc).read():
            pass
        else:
            if os.path.isfile(os.path.join(directory, filename)):
                logger.info(filename + ' not in use - deleting.')
                os.remove(os.path.join(directory, filename))
            else:
                logger.info(filename + ' is a directory.')


def remove_git_directories():
    logger.info('Removing git directories')
    git_directories = ['.git', '.github', '.gitignore', '.gitattributes']
    for filename in git_directories:
        if os.path.isfile(filename):
            logger.info(f'{filename} not in use - deleting.')
            os.remove(filename)
        elif os.path.isdir(filename):
            logger.info(f'{filename} is a directory.')
            shutil.rmtree(filename)
        else:
            pass


def delete_files_with_extension(extension):
    logger.info('Deleting files with extension: ' + extension)
    for filename in Path('.').glob(f'*.{extension}'):
        logger.info(f'{filename} not in use - deleting.')
        os.remove(filename)


def delete_image_directories(directories):
    logger.info('Deleting image directories')
    for directory in directories:
        if Path(directory).exists():
            logger.info('Removing ' + directory + ' directory.')
            os.rmdir(directory)


def zip_tmp_directory(title, tmp_directory):
    logger.info('Zipping temporary directory: ' + tmp_directory)
    shutil.make_archive(f"{title}", 'zip', tmp_directory)


def delete_tmp_directory_final(tmp_directory):
    logger.info('Deleting temporary directory: ' + tmp_directory)
    shutil.rmtree(tmp_directory)


def delete_tmp_directory(tmp_directory):
    logger.info('Deleting temporary directory: ' + tmp_directory)
    if Path(tmp_directory).exists():
        shutil.rmtree(tmp_directory)
    else:
        logger.info('tmp directory does not exist.')


def flatten_directories(directories):
    logger.info('Flattening directories')
    for directory in directories:
        if not Path(directory).exists():
            logger.info(directory + ' does not exist.')
            logger.info('Current working directory: ' + os.getcwd())
            logger.info('Contents of current working directory: ' + str(os.listdir()))
            input('Press enter to continue.')
            exit()
        else:
            logger.info('Flattening ' + directory + ' directory.')
        for filename in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, filename)):
                new_name = str(Path(Path(directory).parent, Path(directory).name + '_' + filename).resolve())
                shutil.copy(os.path.join(directory, filename), new_name)
            else:
                logger.info(filename + ' is a directory.')


def replace_contents(directories, tex_files):
    logger.info('Replacing contents')
    tex_files = []
    for dir in directories:
        tex_files.extend(Path(dir).glob(args.tex_files))
    for tex_file in tex_files:
        logger.info('Replacing image directory in ' + str(tex_file) + '.')
        with open(tex_file, 'r+') as f:
            content = f.read()
            for directory in directories:
                logger.info('Replacing ' + directory + ' with ' + directory + '_')
                content = content.replace(directory + '/', directory + '_')
            f.seek(0)
            f.write(content)
            f.truncate()
            f.close()


def main(args):
    directories = args.directories
    logfile = args.logfile
    enc = args.enc
    tex_files = args.tex_files
    old_directory = os.getcwd()
    tmp_directory = tempfile.mkdtemp()
    logger.info('Temporary directory: ' + tmp_directory)
    create_tmp_directory(tmp_directory)
    directories = [Path(tmp_directory, directory).name for directory in directories]
    flatten_directories(directories)
    os.chdir(tmp_directory)
    copy_files_to_tmp_directory(tmp_directory)
    directories = [Path(tmp_directory, directory).name for directory in directories]
    remove_git_directories()
    replace_contents(directories, tex_files)
    if args.extensions:
        for extension in args.extensions:
            delete_files_with_extension(extension)
    delete_image_directories(directories)
    for directory in directories:
        remove_unused_files(directory, logfile, enc)
    os.chdir(old_directory)
    zip_tmp_directory(args.title, tmp_directory)
    delete_tmp_directory_final(tmp_directory)
    assert Path(f"{args.title}.zip").exists(), "Zip file does not exist."


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Delete and zip files in the working directory.')
    parser.add_argument('--title', type=str, help='Title for the zip file', required=True)
    parser.add_argument('--extensions', nargs='+', help='Extensions of files to delete', default=["aux", "py", "log", "yaml"])
    parser.add_argument('--directories', nargs='+', help='Directories to clean', required=True)
    parser.add_argument('--logfile', help='Logfile to use.', default='output.log')
    parser.add_argument('--enc', help='Encoding to use.', default='Latin-1')
    parser.add_argument('--tex_files', help='Tex files to replace image directory in.', default='*.tex')
    parser.add_argument('--verbosity', help='Logging verbosity level.', default='INFO')
    parser.add_argument('--log_file', help='Log file to use.', default='arxiv.log')
    args = parser.parse_args()
    logger.setLevel(args.verbosity)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    # Create a stream handler and set the formatter
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    # Create a file handler and set the formatter
    file_handler = logging.FileHandler('arxiv.log')
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)
    # Add the stream handler to the logger
    logger.addHandler(stream_handler)
    main(args)
