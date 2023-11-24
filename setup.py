from setuptools import find_packages, setup

setup(
    name='flaskr',
    version='1.0.0',
    #'packages' tells Python what package directories to include.
    packages=find_packages(),
    #find_packages() finds these directories automatically so you don't have to type them out.
    include_package_data=True,
    #include_package_data is set to include other files, such as the static and templates directories.
    install_requires=[
        'flask',
    ],
)

#Python needs another file named MANIFEST.in to tell what this other data is.

#>pip install -e .
#This command tells pip to find setup.py in the current directory and install it in
# editable or development mode. Editable mode means that you make changes to your local code,
# you'll only need to re-install if you change the metadata about the project, such as its dependencies

#Can observe the packages this project have with 
# >'pip list'

#Nothing changed from how the project is running. --app is still set to flaskr
# and flask run still runs on the application, but you can call it from anywhere,
# not just the flask_project directory.

