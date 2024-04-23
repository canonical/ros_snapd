from setuptools import find_packages, setup

package_name = "ros2_snapd"

setup(
    name=package_name,
    version="0.0.1",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages",
            ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    author="Jeremie Deray",
    author_email="jeremie.deray@canonical.com",
    maintainer="Jeremie Deray",
    maintainer_email="jeremie.deray@canonical.com",
    keywords=["ROS"],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python",
        "Topic :: Software Development",
    ],
    description="This package allows to start/stop snap services from ROS 2 services.",
    license="GNU General Public License v3",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": ["ros2_snapd = scripts.ros2_snapd:main"],
    },
)
