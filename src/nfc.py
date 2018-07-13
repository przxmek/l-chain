import serial.tools.list_ports
import asyncio
import serial_asyncio
import json


def init_nfc(socket_update_callback):
    #serial.tools.list_ports_windows
    ports = list(serial.tools.list_ports.comports())

    for item in ports:
        print(item.device)
        print(item.description)

    #con = serial.Serial()

    class Output(asyncio.Protocol):
        def connection_made(self, transport):
            self.transport = transport
            self.buf = bytes()
            print('port opened', transport)
            transport.serial.rts = False  # You can manipulate Serial object via transport
            transport.write(b'init')  # Write serial data via transport


        def data_received(self, data):
            #self.buf += data
            #print('data received', data)#repr(data))
            #if b'\n' in data:
                #self.transport.close()

            self.buf += data
            if b'\n' in self.buf:
                lines = self.buf.split(b'\n')
                self.buf = lines[-1]  # whatever was left over
                for line in lines[:-1]:
                    myData = json.loads(line.decode())
                    #print(f'Reader received: {line.decode()}')
                    # print('json :',myData['uid_device'])

                    #
                socket_update_callback(myData)

        def connection_lost(self, exc):
            print('port closed')
            self.transport.loop.stop()

        def pause_writing(self):
            print('pause writing')
            print(self.transport.get_write_buffer_size())

        def resume_writing(self):
            print(self.transport.get_write_buffer_size())
            print('resume writing')

    loop = asyncio.new_event_loop()#.get_event_loop()
    coro = serial_asyncio.create_serial_connection(loop, Output, '/dev/ttyUSB0', baudrate=115200)
    loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()