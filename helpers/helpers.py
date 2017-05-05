
def disable_paging(channel):
    """
    set terminal len 0 on ssh session and clear recv buffer
    :param channel: paramiko.channel.Channel
    :return: None
    """
    channel.send("terminal length 0\n")
    # Clear the buffer
    channel.recv(1000)


def remove_whitespace(list_of_strings):
    """
    remove all whitespace from a list of strings
    :param list_of_strings: list e.g ["  foo   ", "   bar "]
    :return: list ["foo","bar]
    """
    return [i.replace(" ", "") for i in list_of_strings]


def dict_from_row(row):
    """

    this function will structure a row of output into a dictionary,

    :param row:  str e.g '|Eth1/1|---|---|---|---|---|---|---|'
    :return: dict e.g   {'interface': 'Eth1/1',
                         'mm_rx_crc': 0,
                         'fi_rx_crc': 0,
                         'mm_tx_crc': 0,
                         'fi_tx_stomp': 0,
                         'fi_tx_crc': 0,
                         'mm_rx_stomp': 0,
                         'fi_rx_stomp': 0
                         }

    """
    columns = row.split('|')

    # replace any --- with a 0
    columns = [c.replace("---", "0") for c in columns]

    # create a dictionary for each interface
    return {
        columns[1]: dict(
            mm_rx_crc=int(columns[2]),
            mm_rx_stomp=int(columns[3]),
            fi_rx_crc=int(columns[4]),
            fi_rx_stomp=int(columns[5]),
            fi_tx_crc=int(columns[6]),
            fi_tx_stomp=int(columns[7]),
            mm_tx_crc=int(columns[8])
        )
    }



def carmel_output_parser(output):
    """
        structures data from the output of "show hardware internal carmel crc"
    :param output: str output from show hardware internal carmel crc
    :return: list of interface dictionaries with k,v pairs for carmel CRC errors
    """
    structured_data = []

    # create a list of rows
    ints = [line for line in output.split("\r\n") if line.startswith('| Eth')]

    # eliminate whitespace from all indexes
    ints = remove_whitespace(ints)

    for i in ints:
        structured_data.append(dict_from_row(i))

    return structured_data
