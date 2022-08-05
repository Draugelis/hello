Hello?
=============
Basic [Caller ID](https://callerid.com) inbound call emulator.

Setup
-------------
1. Clone repository

`git clone https://github.com/Draugelis/hello.git`

2. Change directory to `hello/`

`cd hello/`

3. Run `hello.py` 

`python3 hello.py 555-555-5555`

Arguments
-------------
Positional arguments:
* `phone_number`  Caller's phone number - optional

If `phone_number` is missing, a random number will be generated in `(555)-555-5555` format

Allowed `phone_number` formats:
* (555)-555-5555
    * note: `python3 hello.py \(555\)-555-5555`
* 555-555-5555
* 555.555.5555
* 5555555555


