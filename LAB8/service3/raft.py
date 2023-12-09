import socket
import json


class RAFTFactory:
    """Functionality for the initial election in RAFT."""

    def __init__(self, service_info : dict,
                 udp_host : str = "127.0.0.1",
                 udp_port : int = 4444,
                 udp_buffer_size : int = 1024,
                 num_followers : int = 2):
        self.udp_host = udp_host
        self.udp_port = udp_port
        self.udp_buffer_size = udp_buffer_size
        self.udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.service_info = service_info
        self.num_followers = num_followers
        self.followers = []


    def election(self):
        """
            Determines the leader and the followers. 
            The first one connected to the UDP connection
            will be the leader the rest will be the followers.
        """

        # The election ends when all the expected number of followers
        # connected and each sent 2 messages: accept and credentials.
        self.min_num_msgs = self.num_followers * 2

        # All services try to connect using the UDP connection
        # and try bind to the connection.
        try:
            # Only one will succeed in this, and this service will become the Leader.
            self.udp_socket.bind((self.udp_host, self.udp_port))
            self.role = "leader"

            # Starting to gather the information about the followers as they connect using UDP.
            count_of_msgs = 0
            while True:
                # Reading the message and the address from connection.
                message, address = self.udp_socket.recvfrom(self.udp_buffer_size)

                if message.decode() == "Accept":
                    # The Leader should responde back with it's HTTP credentials 
                    # (ip, port, token for writes) to inform the followers about it's location.
                    # if the follower accepted him.
                    data = json.dumps(self.service_info)
                    count_of_msgs += 1
                    self.udp_socket.sendto(str.encode(data), address)
                else:
                    # After getting the Leader's information the 
                    # Followers should send back their HTTP credentials.
                    message = message.decode()
                    count_of_msgs += 1
                    follower_data = json.loads(message)
                    self.followers.append(follower_data)
                if count_of_msgs >= self.min_num_msgs:
                    break
        except:
            # The rest of services will become Followers.
            self.role = "follower"

            # After becoming a Follower the services should send to 
            # the leader an accept message informing they accept him being a leader.
            self.leader_data = self.send_data("Accept")

            # Sending back to the leader the follower's credentials.
            self.send_data(self.service_info)
        self.udp_socket.close()


    def send_data(self, msg):
        """Data send by the followers."""

        if type(msg) is str:
            # Send the accept message to the leader.
            bytes_to_send = str.encode(msg)
            self.udp_socket.sendto(bytes_to_send, (self.udp_host, self.udp_port))
            msg_from_server = self.udp_socket.recvfrom(self.udp_buffer_size)[0]
            return json.loads(msg_from_server.decode())
        else:
            # Send the followers credentials to the leader.
            str_dict = json.dumps(msg)
            bytes_to_send = str.encode(str_dict)
            self.udp_socket.sendto(bytes_to_send, (self.udp_host, self.udp_port))