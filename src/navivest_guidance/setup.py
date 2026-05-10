from setuptools import find_packages, setup

package_name = 'navivest_guidance'

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
    maintainer='macho',
    maintainer_email='macho@todo.todo',
    description='TODO: Package description',
    license='MIT',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'goal_to_plan = navivest_guidance.goal_to_plan:main',
            'zed_topdown_astar = navivest_guidance.zed_topdown_astar:main',
            'scan_guardrails = navivest_guidance.scan_guardrails:main',
        ],
    },
)
