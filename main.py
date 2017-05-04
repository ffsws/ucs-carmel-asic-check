import paramiko
import time
import yaml
from lib.helpers import carmel_output_parser, disable_paging
from lib.spark import send_spark_message

# Helper functions


def get_carmel_crc_errors(ip, username, password):
    """
    Main routine which will get and structure the output of a
    "show hardware internal carmel crc"

    :param ip: str IP address of FI
    :param username: str username
    :param password: str password
    :return: list of interface dictionaries
    """

    # Create instance of SSHClient object
    client_pre = paramiko.SSHClient()

    # Automatically add untrusted hosts (make sure okay for security policy in your environment)
    client_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # initiate SSH connection
    client_pre.connect(ip, username=username, password=password, look_for_keys=False, allow_agent=False)
    # print "SSH connection established to %s" % ip

    # Use invoke_shell to establish an 'interactive session'
    client = client_pre.invoke_shell()
    # Turn off paging
    disable_paging(client)

    # send the commands here

    client.send("\n")
    client.send("connect nxos \n")
    client.send("show hardware internal carmel crc\n")
    # Wait for the command to complete
    time.sleep(5)

    output = client.recv(30000)
    return carmel_output_parser(output)


if __name__ == '__main__':

    # Gather configuration
    with open('config.yaml') as fh:
        config = yaml.safe_load(fh)

    myusername = config['username']
    mypassword = config['password']
    fabric_interconnects = config['fabric_interconnects']

    results = dict()
    has_errors = list()

    # Gather all the data from the fabric interconnects
    for fi in fabric_interconnects:
        result = get_carmel_crc_errors(fi, myusername, mypassword)

        for interface in result:
            for k in interface.keys():
                # check if we get any errors
                if not all(value == 0 for value in interface[k].values()):
                    has_errors.append("Interface {} on Fabric Interconnect {} is reporting CRC errors!!".format(k, fi))

        results[fi] = result

    # Notification via Spark/Console
    if len(has_errors) == 0:
        cleanmsg = "No CRC errors were reported on any of the monitored Fabric Interconnects"
        if config['spark_notifications']:
            print "Sending Spark Notifications... "
            send_spark_message(config['spark_token'], config['spark_room_id'], cleanmsg)
        else:
            print cleanmsg
    else:
        for msg in has_errors:
            if config['spark_notifications']:
                print "Sending Spark Notifications... "
                send_spark_message(config['spark_token'], config['spark_room_id'], msg)
            else:
                print msg
