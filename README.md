# UDPRecorder

UDPRecorder is a Python library for recording and replaying UDP steams. It is made to ease the development of applications based on UDP streams. It is originally used to replay telemetry data from sim racing games such as *Assetto Corsa Competizione* or *F1 20XX* games.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install UDPRecorder.

```bash
pip install udprecorder
```

## Usage

### Commandline

```bash
python
```

### In scripts

```python
import udprecorder

# To record a stream
udprecorder.record(
    file_name = 'my_record.bin', # path to the saved replay
    addr = ('127.0.0.1', 1234)   # (host, port) to listen to
    buffer_size = 65536     # size of buffer used for the socket
    max_num_packets = 1200  # stop the record after 1200 event received
    max_seconds = 3600      # stop the record after 1 hour
)

# To replay a stream
udprecorder.replay(
    file_name = 'my_record.bin', # path to the saved replay
    addr = ('127.0.0.1', 1234)   # (host, port) to emit to
)
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
