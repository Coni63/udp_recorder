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
record_udp -p 1234 -s 127.0.0.1 -f myfile.bin -b 1024 -c 9999 -s 3600
replay_udp -p 1234 -s 127.0.0.1 -f myfile.bin
```

|    |          | description                  | required | type | default    |
|----|----------|------------------------------|----------|------|------------|
| -p | --port   | Port to listen/replay to     | False    | int  | 1234       |
| -s | --server | Host to listen/replay to     | False    | str  | 127.0.0.1  |
| -f | --file   | File to save/read the stream | False    | str  | udp.bin    |
| -b | --buffer | Buffer size limit            | False    | int  | 65536      |
| -c | --count  | number of message to read    | False    | int  | 1000000000 |
| -t | --time   | time limit to record         | False    | int  | 1000000000 |

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

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. A list of future changes is available just below. Feel free to contribute on those points.

Please make sure to update tests as appropriate.

## Future updates

- Add parameter to adjust the replay speed
- better handling of errors
- Add pipeline for tests / pre-commits
- Add badges on the readme based on build
- Add tox to tests multiples environments

## License

[MIT](https://choosealicense.com/licenses/mit/)
