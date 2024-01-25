import os

directories = ['cifar', 'mnist', 'cifar100']
logfile = 'output.log'
enc = 'Latin-1' # For Overleaf, try 'Latin-1' if issues encountered...

for directory in directories:
    print('Cleaning ' + directory + ' directory.')
    for filename in os.listdir(directory):
        if filename in open(logfile, encoding=enc).read():
            print(filename + ' in use.')
        else:
            if os.path.isfile(os.path.join(directory, filename)):
                print(filename + ' not in use - deleting.')
                os.remove(os.path.join(directory, filename))
            else:
                print(filename + ' is a directory.')