import os
from pathlib import Path
import shutil



def remove_unused_files(directories, logfile, enc):
    for directory in directories:
        print('Cleaning ' + directory + ' directory.')
        for filename in os.listdir(directory):
            if filename in open(logfile, encoding=enc).read():
                pass
            else:
                if os.path.isfile(os.path.join(directory, filename)):
                    print(filename + ' not in use - deleting.')
                    os.remove(os.path.join(directory, filename))
                else:
                    print(filename + ' is a directory.')


                
                


def flatten_directories(directories):
    for directory in directories:
        for filename in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, filename)):
                new_name = str(Path(Path(directory).parent, Path(directory).name + '_' + filename).resolve())   
            # move file
                shutil.copy(os.path.join(directory, filename), new_name)
            else:
                print(filename + ' is a directory.')


def replace_contents(directories, tex_files):
    for tex_file in tex_files:
        print('Replacing image directory in ' + str(tex_file) + '.')
        with open(tex_file, 'r+') as f:
            content = f.read()
            for directory in directories:
                print('Replacing ' + directory + ' with ' + directory + '_')
                content = content.replace(directory + '/', directory + '_')
            f.seek(0)
            f.write(content)
            f.truncate()
            f.close()




if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--directories', nargs='+', help='List of directories to flatten.', required=True)
    parser.add_argument('--logfile', help='Logfile to use.', default='output.log')
    parser.add_argument('--enc', help='Encoding to use.', default='Latin-1')
    parser.add_argument('--tex_files', nargs='+', help='List of .tex files to modify.', default='*.tex')
    args = parser.parse_args()
    directories = args.directories
    logfile = args.logfile
    enc = args.enc
    tex_files = []
    for dir in directories:
        tex_files.extend(Path(dir).glob(args.tex_files))
    # Remove unused files according to logfile with encoding enc
    remove_unused_files(directories, logfile, enc)
    # Flatten directories by moving files to parent directory and renaming them such that the new name is the concatenation of the parent directory and the original filename
    flatten_directories(directories)
    # Replace image directory with image directory + '_'
    replace_contents(directories, tex_files)
        
        
