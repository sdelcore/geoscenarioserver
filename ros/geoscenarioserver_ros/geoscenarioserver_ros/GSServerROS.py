from dataclasses import dataclass
import os

import rclpy
from rclpy.node import Node
from rclpy.exceptions import ParameterNotDeclaredException
from rcl_interfaces.msg import ParameterType, ParameterDescriptor
from rclpy.logging import LoggingSeverity

from geoscenario_msgs.msg import Tick, Pedestrian, Vehicle

from geoscenarioserver.GSServer import GSServerBase
from geoscenarioserver.geoscenarioserver.mapping.LaneletMap import LaneletMap
from geoscenarioserver.geoscenarioserver.SimConfig import SimConfig
from geoscenarioserver.SimTraffic import SimTraffic
from geoscenarioserver.dash.Dashboard import *

@dataclass
class Parameter:
    name:str = ""
    type:ParameterType = ParameterType.PARAMETER_NOT_SET
    description:str = ""
    default_value = None

class GSServerROS(Node, GSServerBase):
    def __init__(self):
        super(Node, self).__init__('geoscenarioserver')
        super(GSServerBase, self).__init__()

        parameters = [
            Parameter(name='scenario_files', type=ParameterType.PARAMETER_STRING_ARRAY, description='GeoScenario file paths', default_value=[]),
            Parameter(name='quiet', type=ParameterType.PARAMETER_BOOL, description="don't print messages to stdout", default_value=True),
            Parameter(name='no_dashboard', type=ParameterType.PARAMETER_BOOL, description='run without the dashboard', default_value=False),
            Parameter(name='map_path', type=ParameterType.PARAMETER_STRING, description='Set the prefix to append to the value of the attribute `globalconfig->lanelet`', default_value=""),
            Parameter(name='btree_locations', type=ParameterType.PARAMETER_STRING, description='Add higher priority locations to search for btrees by agent btypes', default_value=""),
            Parameter(name='dashboard_position', type=ParameterType.PARAMETER_DOUBLE_ARRAY, description='Set the position of the dashboard window (x y width height)', default_value=[]),
            Parameter(name='file_log', type=ParameterType.PARAMETER_BOOL, description='Log to $GSS_OUTPUTS/GSServer.log instead of stdout', default_value=False)
        ]

        # Don't add args for log level and log location as those are handled by ROS2 (parameter log-level and env $ROS_HOME)

        for param in parameters:
            param_descriptor = ParameterDescriptor(type=param.type,
                                                    description=param.description)
            self.declare_parameter(param.name, param.default_value, param_descriptor)

        self.tick_pub = self.create_publisher(Tick, '/gs/tick', 10)
        self.tick_sub = self.create_subscription(Tick, '/gs/tick_from_client', self.tick_from_client, 10)

        self.get_logger().info('GeoScenarioServer ROS Node has been started.')

        self.lanelet_map = LaneletMap()
        self.sim_config = SimConfig()
        self.sim_config.show_dashboard = not self.get_parameter('no_dashboard').get_parameter_value().bool_value
        self.btree_locations = self.parse_btree_paths(self.get_parameter('btree_locations').get_parameter_value().string_value) # TODO: does it need to be retained?
        self.traffic = SimTraffic(self.lanelet_map, self.sim_config)

        gsfiles = self.get_parameter('scenario_files').get_parameter_value().string_array_value
        map_path = self.get_parameter('map_path').get_parameter_value().string_value

        if not self.construct_scenario(gsfiles, self.traffic, self.sim_config, self.lanelet_map, map_path, self.btree_locations):
            log.error("Failed to load scenario")
            raise RuntimeError("Failed to load scenario")

        self.traffic.start()

        #GUI / Debug screen
        if self.sim_config.show_dashboard:
            dashboard_position = self.get_parameter('dashboard_position').get_parameter_value().double_array_value
            screen_param = get_screen_parameters(dashboard_position)
            dashboard = Dashboard(self.traffic, self.sim_config, screen_param)
            dashboard.start()

    def tick_from_client(self, msg):
        self.get_logger().info(f"Received tick from client: {msg}")


def main(args=None):
    gs = GSServerBase()
    print('GSServerBase initialized with test value: "%s"' % gs.test)
    rclpy.init(args=args)
    gs_server_ros = GSServerROS()
    rclpy.spin(gs_server_ros)
    gs_server_ros.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()