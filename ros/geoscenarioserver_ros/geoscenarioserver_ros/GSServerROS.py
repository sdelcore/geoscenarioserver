from dataclasses import dataclass

import rclpy
from rclpy.node import Node
from rclpy.exceptions import ParameterNotDeclaredException
from rcl_interfaces.msg import ParameterType, ParameterDescriptor

from geoscenarioserver.GSServer import GSServerBase
from geoscenarioserver.geoscenarioserver.mapping.LaneletMap import LaneletMap

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
            Parameter(name='debug', type=ParameterType.PARAMETER_BOOL, description='Set the logging level to DEBUG instead of INFO', default_value=False),
            Parameter(name='file_log', type=ParameterType.PARAMETER_BOOL, description='Log to $GSS_OUTPUTS/GSServer.log instead of stdout', default_value=False)
        ]

        for param in parameters:
            param_descriptor = ParameterDescriptor(type=param.type,
                                                    description=param.description)
            self.declare_parameter(param.name, param.default_value, param_descriptor)

        self.get_logger().info('GeoScenarioServer ROS Node has been started.')

        #self.lanelet_map = LaneletMap()
        #self.sim_config = self.construct_sim_config
        #tree_locations = self.parse_btree_paths(args.btree_locations)

        # use sim_config after all modifications
        #traffic = SimTraffic(lanelet_map, sim_config)


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