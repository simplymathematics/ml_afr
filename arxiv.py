import argparse
from pathlib import Path
import os
import shutil
import argparse
from pathlib import Path
import os
import shutil
import tempfile

title = "Survival Analysis for Deep Convolutional Neural Networks"
def create_tmp_directory(tmp_directory):
        os.makedirs(tmp_directory, exist_ok=True)


    def copy_files_to_tmp_directory(tmp_directory):
        for filename in Path('.').glob('*'):
            if Path(filename).is_dir():
                print(f"{filename} is a directory - skipping.")
            else:
                print(f"Copying {filename} to tmp directory.")
                shutil.copy(filename, str(Path(tmp_directory, filename).resolve()))


    def remove_git_directories():
        git_directories = ['.git', '.github', '.gitignore', '.gitattributes']
        for filename in git_directories:
            if os.path.isfile(filename):
                print(f'{filename} not in use - deleting.')
                os.remove(filename)
            elif os.path.isdir(filename):
                print(f'{filename} is a directory.')
                shutil.rmtree(filename)
            else:
                print(f'{filename} does not exist.')


    def delete_files_with_extension(extension):
        for filename in Path('.').glob(f'*.{extension}'):
            print(f'{filename} not in use - deleting.')
            os.remove(filename)


    def delete_image_directories(directories):
        for directory in directories:
            if Path(directory).exists():
                print('Removing ' + directory + ' directory.')
                os.rmdir(directory)


    def zip_tmp_directory(title, tmp_directory):
        shutil.make_archive(f"{title}", 'zip', tmp_directory)


    def delete_tmp_directory_final(tmp_directory):
        shutil.rmtree(tmp_directory)
        
    def delete_tmp_directory(tmp_directory):
        if Path(tmp_directory).exists():
            shutil.rmtree(tmp_directory)
        else:
            print('tmp directory does not exist.')
            
def main():
    parser = argparse.ArgumentParser(description='Delete and zip files in the working directory.')
    parser.add_argument('--title', type=str, help='Title for the zip file')
    parser.add_argument('--extensions', nargs='+', help='Extensions of files to delete', default=["aux", "py", "log", "yaml"])
    parser.add_argument('--directories', nargs='+', help='Image directories to delete')
    args = parser.parse_args()
    old_directory = os.getcwd()
    tmp_directory = tempfile.mkdtemp()
    create_tmp_directory(tmp_directory)
    os.chdir(tmp_directory)
    copy_files_to_tmp_directory(tmp_directory)
    remove_git_directories()

    if args.extensions:
        for extension in args.extensions:
            delete_files_with_extension(extension)

    if args.directories:
        delete_image_directories(args.directories)

    os.chdir(old_directory)
    zip_tmp_directory(args.title, tmp_directory)
    delete_tmp_directory_final(tmp_directory)


if __name__ == '__main__':
    main()

   




    


    

    if __name__ == '__main__':
        main()
