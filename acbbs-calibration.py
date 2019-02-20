#!/usr/bin/python2.7
# coding=UTF-8

from acbbs.drivers.ate.PwrMeter import PwrMeter
from acbbs.drivers.ate.RFSigGen import RFSigGen
from acbbs.drivers.ate.Swtch import Swtch
import argparse
import time
import json
import os.path


CONF_PATH = "/etc/acbbs/swtch_cal.json"

LIST_PATH = {
    "Jx-J2":{
        "port":"J2",
        "min":5,
        "max":15,
        "sw3":2,
        "sw4":1
    },
    "Jx-J3":{
        "port":"J3",
        "min":70,
        "max":80,
        "sw3":3,
        "sw4":1
    },
    "Jx-J5":{
        "port":"J5",
        "min":20,
        "max":28,
        "sw3":4,
        "sw4":1
    },
    "Jx-J4":{
        "port":"J4",
        "min":0,
        "max":5,
        "sw3":3,
        "sw4":1
    },
    "Jx-J4_20dB":{
        "port":"J4",
        "min":30,
        "max":40,
        "sw3":4,
        "sw4":2
    },
    "Jx-J18":{
        "port":"J18",
        "min":0,
        "max":5,
        "sw3":2,
        "sw4":1
    }
}

class read_write(object):
    def __init__(self, file):
        self.file = file
        with open(self.file, "r") as json_file:
            self.data = json.load(json_file)

    def write_date(self):
        self.data["calibration-date"] = time.strftime("%Y-%m-%d %H:%M:%S")

    def read_date(self):
        return self.data["calibration-date"]

    def write_cal(self, path, value):
        self.data["loss"][path] = value

    def read_cal(self, path):
        return self.data["loss"][path]

    def __del__(self):
        with open(self.file, "w") as json_file:
            json.dump(self.data, json_file, indent=2, sort_keys=True)


def main(args):
    print("Not yet checked. Come back later ;)")
    exit(0)
    ###################################################################################
    ################### args check
    ###################################################################################
    if args.conf is None:
        conf_path = CONF_PATH
    else:
        conf_path = args.conf

    if not os.path.isfile(conf_path):
        print("configuration.json not found at location {0}. Please use arg -c to set it correctly".format(conf_path))
        exit(0)

    try:
        dut_channel = args.channel.split(",")
        for i in range(0, len(dut_channel)):
            dut_channel[i] = int(dut_channel[i])
    except:
        print("Error parsing DUT channel")
        exit(0)

    OUTPUT_FREQ_CALIBRATION = int(args.frequency)
    OUTPUT_POWER_CALIBRATION = int(args.power)
    if args.simulate:
        SIMULATE = True
    else:
        SIMULATE = False

    ###################################################################################
    ################### class instantiation
    ###################################################################################    
    rw = read_write(conf_path)
    rfsiggen = RFSigGen(simulate=SIMULATE)
    pwrmeter = PwrMeter(simulate=SIMULATE)
    swtch = Swtch(simulate=SIMULATE)

    rfsiggen.status = 0
    rfsiggen.freq = OUTPUT_FREQ_CALIBRATION
    rfsiggen.power = OUTPUT_POWER_CALIBRATION

    pwrmeter.freq = OUTPUT_FREQ_CALIBRATION

    print("Previous calibration date : {0}\n".format(rw.read_date()))

    ###################################################################################
    ################### get calibration cable loss
    ###################################################################################
    print("Connect power meter on generator without any cable.")
    raw_input("Press Enter key to start measure...")
    rfsiggen.status = 1
    time.sleep(1)
    gen_loss = OUTPUT_POWER_CALIBRATION - pwrmeter.power
    print("generator loss is : {0}dB".format(gen_loss))
    rfsiggen.status = 0

    print("Connect calibration cable between generator and power meter.")
    raw_input("Press Enter key to start measure...")
    rfsiggen.status = 1
    time.sleep(1)
    calibration_cable_loss = OUTPUT_POWER_CALIBRATION - pwrmeter.power
    total_loss = calibration_cable_loss + gen_loss
    print("Calibration cable loss is : {0}dB".format(calibration_cable_loss))
    print("Total generator plus calibration cable loss is : {0}dB".format(total_loss))
    rfsiggen.status = 0


    ###################################################################################
    ################### calibration
    ###################################################################################
    for channel in dut_channel:
        print("\nConnect generator on channel {0}".format(channel))
        for key, value in LIST_PATH.items():
            t_key = key.replace("x", str(channel+8))
            retry = True
            while(retry):
                print("\nConnect power meter on output {0}".format(value["port"]))
                raw_input("Press Enter key to start measure...")
                swtch.setSwitch(sw1 = channel, sw3=value["sw3"], sw4=value["sw4"])
                rfsiggen.status = 1
                time.sleep(1)
                loss = OUTPUT_POWER_CALIBRATION - pwrmeter.power - total_loss
                if value["port"] == "J4":
                    loss += gen_loss                            #Add generator loss only for generator output
                rfsiggen.status = 0

                print("\n{0}\t previous loss : {1}dB\t actual loss : {2}dB\t Delta : {3}".format(
                    t_key, rw.read_cal(path=t_key), loss, abs(rw.read_cal(path=t_key)-loss)))

                if loss < value["min"] or loss > value["max"]:
                    print("Error. Loss should be between {0}dB and {1}dB.".format(value["min"], value["max"]))
                    c = 0
                    while c != 'r' and c != 'k' and c!= 'p':
                        c = raw_input("Retry (r), keep this value (k) or pass and keep previous value (p)\n")
                        if c == 'r':
                            pass
                        elif c == 'k':
                            rw.write_cal(path=t_key, value=loss)
                            retry = False
                        elif c == 'p':
                            retry = False
                else:
                    rw.write_cal(path=t_key, value=loss)
                    retry = False

    rw.write_date()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description = "Calibration script for Hardware caracterisation bench",
        fromfile_prefix_chars = '@' )
    parser.add_argument(
        "-c",
        "--conf",
        help="set configuration path (default is {0})".format(CONF_PATH),
        required = False)
    parser.add_argument(
        "--channel",
        help="select channel to calibrate (1,2,3,4,5,6,7,8)",
        required = True)
    parser.add_argument(
        "-f",
        "--frequency",
        help="set generator frequency for calibration (in Hz)",
        required = True)
    parser.add_argument(
        "-p",
        "--power",
        help="set generator output power for calibration (in dBm)",
        required = True)
    parser.add_argument(
        "--simulate",
        help="start calibration in simulation for test",
        required = False,
        action="store_true")
    args = parser.parse_args()
    main(args)
