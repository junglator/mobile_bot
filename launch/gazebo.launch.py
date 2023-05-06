import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='true') # each nodes will need the /use_sim_time parameter set to true
    robot_name = 'mobile_bot'
    world_file_name = 'supermarket.sdf'

    world = os.path.join(get_package_share_directory(
        robot_name), 'worlds', world_file_name)

    urdf = os.path.join(get_package_share_directory(
        robot_name), 'urdf', 'mobile.urdf')

    xml = open(urdf, 'r').read()

    xml = xml.replace('"', '\\"')

    swpan_args = '{name: \"mobile\", xml: \"' + xml + '\" }'

    # Open the URDF file
    with open(urdf, 'r') as infp:
        robot_desc = infp.read()

    return LaunchDescription([
        ExecuteProcess(
            cmd=['gazebo', '--verbose', world,
                 '-s', 'libgazebo_ros_factory.so'],
            output='screen'),

        ExecuteProcess(
            cmd=['ros2', 'param', 'set', '/gazebo',
                 'use_sim_time', use_sim_time],
            output='screen'),

        ExecuteProcess(
            cmd=['ros2', 'service', 'call', '/spawn_entity',
                 'gazebo_msgs/SpawnEntity', swpan_args],
            output='screen'),

        Node(package='robot_state_publisher',executable='robot_state_publisher',
            name='robot_state_publisher',output='screen',
            parameters=[{'use_sim_time': use_sim_time, 'robot_description': robot_desc}],
            arguments=[urdf]),
        
        Node(package='joint_state_publisher',executable='joint_state_publisher',
            name='joint_state_publisher',output='screen',
            parameters=[{'use_sim_time': use_sim_time, 'robot_description': robot_desc}],
            arguments=[urdf])
    ])