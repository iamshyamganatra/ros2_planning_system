# Copyright 2019 Intelligent Robotics Lab
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    # Get the launch directory
    domain_expert_dir = get_package_share_directory('plansys2_domain_expert')
    launch_dir = os.path.join(domain_expert_dir, 'launch')

    # Create the launch configuration variables
    model_file = LaunchConfiguration('model_file')

    stdout_linebuf_envvar = SetEnvironmentVariable(
        'RCUTILS_CONSOLE_STDOUT_LINE_BUFFERED', '1')

    declare_model_file_cmd = DeclareLaunchArgument(
        'model_file',
        default_value='src/ros2_planning_system/'
        'plansys2_domain_expert/test/pddl/domain_simple.pddl',
        description='PDDL Model file')

    # Specify the actions
    domain_expert_cmd = Node(
        package='plansys2_problem_expert',
        node_executable='problem_expert_node',
        node_name='problem_expert',
        output='screen',
        parameters=[{'model_file': model_file}])

    # Create the launch description and populate
    ld = LaunchDescription()

    # Set environment variables
    ld.add_action(stdout_linebuf_envvar)
    ld.add_action(declare_model_file_cmd)

    # Declare the launch options
    ld.add_action(domain_expert_cmd)

    return ld