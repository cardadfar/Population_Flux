# Population_Flux

Population Flux is a typology machine that measures the different population trends of people in rooms and how people tend to move in and out of rooms (individual/group) in order for viewers to see how busy rooms are at certain times.

## Interface

![description](documentation/layout.png)

Layout of the data-transfer operations. Terminals need to be set up to listen from the serial port, transmit data over a web socket, and launch a localhost to view the visualization. The serial port terminal can be run independently to first capture the data, while the other two terminals can be run to parse and visualize the results.

## Setup

In a terminal at the home directory,
```bash
cd /dev/
ls
```
Look for a device named tty.usbmodem(#number). In urg/pyUrg.py, change the port variable default to the name of the tty modem

```python
 def connect(self, port = '/dev/tty.usbmodem(#number)', baudrate = 115200, timeout = 0.1):
```
