import os
from pathlib import Path
directories = ['cifar', 'mnist', 'cifar100']
logfile = 'output.log'
enc = 'Latin-1' # For Overleaf, try 'Latin-1' if issues encountered...

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
                
                
# Uncomment to prepare for ArXiv submission
# Remove .git subdirectories
# git_directories = ['.git', '.github', '.gitignore', '.gitattributes']
# for filename in git_directories:
#     if os.path.isfile(filename):
#         print(filename + ' not in use - deleting.')
#         os.remove(filename)
#     else:
# print('Removed git Repo')
# Remove .py file
# if os.path.isfile('clean.py'):
#     print('clean.py not in use - deleting.')

# Move all image files to root directory, replacing ${image_directory}/ with ${image_directory}_ in .tex file

for directory in directories:
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            new_name = str(Path(Path(directory).parent, Path(directory).name + '_' + filename).resolve())   
            # move file
            os.rename(os.path.join(directory, filename), new_name)
        else:
            print(filename + ' is a directory.')

# List all .tex files
tex_files = Path('.').glob('*.tex')

# Replace image directory with image directory + '_'
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

# Delete all image directories
for directory in directories:
    if Path(directory).exists():
        print('Removing ' + directory + ' directory.')
