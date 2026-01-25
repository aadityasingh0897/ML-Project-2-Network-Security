from typing import List

from setuptools import find_packages, setup

def get_requirements() -> List[str]:
    requirement_list: List[str] = []
    try:
        with open("requirements.txt", "r") as file:
            for line in file:
                requirement = line.strip()
                if requirement and requirement != "-e .":
                    requirement_list.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file not found.")
    
    return requirement_list

setup(
    name="NetworkSecurity",
    version="1.0.0",
    author="Aaditya Singh",
    author_email="aadityasingh0897@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements(),
)
# This function reads the requirements.txt file and returns a list of dependencies,