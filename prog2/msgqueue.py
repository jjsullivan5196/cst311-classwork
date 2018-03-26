# Format for broadcast message
cast_fmt = '{} {}: {}'

# Format for debug message
debug_fmt = '{{ {} received before {} }}'

# These classes handle queuing up and formatting messages from clients.
# I used these to give the server configurable behavior, without
# having to hardcode it in. Most use was for debugging purposes.
class MsgQueue:
    def __init__(self):
        self.queue = []
        self.__server_msg = ''

    def __set_server_msg__(self, msg):
        self.__server_msg = msg

    def __mark__(self):
        self.queue = [[True, msg] for sent, msg in self.queue]
        
    def __unreads__(self):
        return [msg for msg in self.queue if not msg[0]]

    def __len__(self):
        return len(self.__unreads__())

    def __dequeue__(self):
        self.queue = self.__unreads__()

    def append(self, msg):
        self.queue.append([False, msg])

    def read_server(self):
        oldmsg = self.__server_msg
        self.__server_msg = ''
        return oldmsg
    
    def read(self):
        messages = [msg[1] for msg in self.__unreads__()]
        self.__mark__()
        self.__dequeue__()
        return '\n'.join([cast_fmt.format(*msg) for msg in messages])

class DebugQueue(MsgQueue):
    def read(self):
        messages = [msg[1] for msg in self.__unreads__()]
        self.__mark__()
        formatted = '\n'.join([cast_fmt.format(*msg) for msg in messages])

        if len(self.queue) > 1:
            clients = [str(msg[1][1]) for msg in self.queue]
            formatted += '\n' + debug_fmt.format(clients[0], ','.join(clients[1:]))
            self.__set_server_msg__('Sent acknowledgement to {} and {}'.format(clients[0], ','.join(clients[1:])))
            self.__dequeue__()

        return formatted
