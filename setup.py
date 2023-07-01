from setuptools import setup, find_packages
from typing import List

HYPHEN_E_DOT = '-e .'
def get_requirements(file_path:str)->List[str]:
    '''
        Desc: This function will responsible for reading modules from
        requirements.txt as well it going to ignore our -e . when all module or lib
        is going to install when we hit python setup.py
    '''
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace('\n', '') for req in requirements]
        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)
    return requirements

setup(
    name='Credit Card Fault Detection',
    version='0.0.1',
    author='Anirudhra rao',
    author_email='raorudhra16@gmail.com',
    packages=find_packages(),
    install_requires = get_requirements('requirements.txt')
)