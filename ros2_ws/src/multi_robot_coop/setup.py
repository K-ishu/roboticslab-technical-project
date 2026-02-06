from setuptools import find_packages, setup

package_name = 'multi_robot_coop'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='kishu',
    maintainer_email='mkhodashenas78@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
    'console_scripts': [
        'tb3_coordinator = multi_robot_coop.tb3_coordinator:main',
        'arm_coordinator = multi_robot_coop.arm_coordinator:main',
    ],
},

)
