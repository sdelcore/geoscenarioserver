from rclpy.node import Node

class GSServerROS(Node, GSServer):
    def __init__(self):
        super().__init__('geoscenarioserver_ros_node')
        self.get_logger().info('GeoScenarioServer ROS Node has been started.')
