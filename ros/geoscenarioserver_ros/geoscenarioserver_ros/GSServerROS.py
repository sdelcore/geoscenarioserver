import rclpy
from rclpy.node import Node

from std_msgs.msg import String  # remove after testing

from geoscenarioserver.GSServer import GSServerBase

class GSServerROS(Node):
    def __init__(self):
        super().__init__('geoscenarioserver')
        self.get_logger().info('GeoScenarioServer ROS Node has been started.')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello, ROS 2! %d' % self.i
        self.publisher_.publish(msg)
        self.i += 1
        self.get_logger().info('Publishing: "%s"' % msg.data)


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