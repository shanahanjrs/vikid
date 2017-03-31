# Vikid

### Viki job automation platform daemon

## Features of Viki
- Simple to start up and use
- Small and lightweight
- Trigger a job run automatically via Webhook or manually with the command line tool
- Uses JSON instead of XML

## Installing
Pip installation:
```
pip install vikid
```

For development:
```
$ git clone https://github.com/shanahanjrs/vikid
$ cd vikid
$ pip3 install -e .
```

## FAQ

### How do I start the Viki daemon?
Simple, run `$ vikid` to start the daemon. Starting with Monit recommended.

### How do I use the command line tool?
Install [viki](https://github.com/shanahanjrs/vikid) and run `viki -h` to get started.

### Will there be Windows support any time soon?
At the moment there is no plan to support windows operating systems.

### License
Code released under the [Apache 2.0 License](https://github.com/shanahanjrs/viki/blob/master/LICENSE.md).
