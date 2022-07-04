import scapy.all as scapy
import argparse
import re
from random import randrange
import logging

"""Script to emulate an inbound call for Caller ID device

Script generates a packet that Caller ID devices generate and send it to broadcast IP
"""

def setup_logging():
    logger = logging.getLogger('hello')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(levelname)-6s - %(message)s")
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    logger.addHandler(sh)

    return logger

logger = setup_logging()

class PhoneNumber:
    def __init__(self):
        self.phone_number = self.get_phone_number()
        logger.info("phone_number: " + self.phone_number)

    def __str__(self):
        return self.phone_number

    def get_phone_number(self):
        """Getting phone number from command line arguments or generating a random number
        Phone number is padded to 14 characters as per Caller ID packet structure

        Returns:
            str: packet-ready phone number
        """        
        self.parser = argparse.ArgumentParser(description="Caller ID inbound call emulator")
        self.parser.add_argument("phone_number", type=str, help="Caller's phone number", nargs="?")
        self.args = self.parser.parse_args()

        if self.args.phone_number:
            logger.info("phone_number is provided")
            self.args.phone_number = str(self.args.phone_number)
            if self.validate_phone_number(self.args.phone_number):
                logger.info("phone_number is valid")
                return self.args.phone_number.ljust(14, " ")# Padding phone number to 14 chars
            else: 
                logger.error("Invalid phone_number provided. phone_number must be 1-14 digits long")
                logger.info("Generating a random number")
                return self.generate_phone_number()
        else:
            logger.info("No phone_number provided")
            logger.info("Generating a random number")
            return self.generate_phone_number()

    def validate_phone_number(self, phone_number):
        """Validates phoner number

        Args:
            phone_number (str)

        Returns:
            bool: is phone_number valid
        """        
        pattern = re.compile("^\(?\d{1,3}\)?[\s.-]?\d{0,3}[\s.-]?\d{0,4}$")
        return bool(pattern.match(phone_number))

    def generate_phone_number(self):
        """Generate random phone number

        Returns:
            str: random phone_number
        """        
        return f"({randrange(100,999)})-{randrange(100,999)}-{randrange(1000,9999)}"


class UdpMessage:
    """Class for generating and sending broadcast message to emulate inbound call
    """
    
    def __init__(self, phone_number):
        self.dst = scapy.conf.route.get_if_bcast(scapy.conf.iface)[0] 
        self.ip = scapy.IP(src="0.0.0.0", dst=self.dst)
        self.proto = scapy.UDP(sport=3520, dport=3520) 
        self.content = scapy.Raw(load=f"^^<U>000001<S>123456$01 I S 0000 G A1 01/01 12:00 PM {phone_number} CallerIDTest")
        self.packet = self.ip / self.proto / self.content

        logger.info("Generated phone call message")

    def send(self):
        logger.info("Sending phone call message")
        scapy.send(self.packet)

def run():
    phone_number = PhoneNumber()
    message = UdpMessage(phone_number)
    message.send()

if __name__ == "__main__":
    run()