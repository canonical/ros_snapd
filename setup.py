from catkin_pkg.python_setup import generate_distutils_setup
from setuptools import setup

setup_args = generate_distutils_setup(
    package_dir={"": "src"},
    packages=["ros_snapd"],
)

setup(**setup_args)
