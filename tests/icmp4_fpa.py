#!/usr/bin/env python3


############################################################################
#                                                                          #
#  PyTCP - Python TCP/IP stack                                             #
#  Copyright (C) 2020-2021  Sebastian Majewski                             #
#                                                                          #
#  This program is free software: you can redistribute it and/or modify    #
#  it under the terms of the GNU General Public License as published by    #
#  the Free Software Foundation, either version 3 of the License, or       #
#  (at your option) any later version.                                     #
#                                                                          #
#  This program is distributed in the hope that it will be useful,         #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of          #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           #
#  GNU General Public License for more details.                            #
#                                                                          #
#  You should have received a copy of the GNU General Public License       #
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.  #
#                                                                          #
#  Author's email: ccie18643@gmail.com                                     #
#  Github repository: https://github.com/ccie18643/PyTCP                   #
#                                                                          #
############################################################################


#
# tests/icmp4_fpa.py -  tests specific for ICMPv4 fpa module
#

from testslide import TestCase

from pytcp.lib.tracker import Tracker
from pytcp.protocols.icmp4.fpa import Icmp4Assembler
from pytcp.protocols.icmp4.ps import (
    ICMP4_ECHO_REPLY,
    ICMP4_ECHO_REPLY_LEN,
    ICMP4_ECHO_REQUEST,
    ICMP4_ECHO_REQUEST_LEN,
    ICMP4_UNREACHABLE,
    ICMP4_UNREACHABLE__PORT,
    ICMP4_UNREACHABLE_LEN,
)
from pytcp.protocols.ip4.ps import IP4_PROTO_ICMP4


class TestIcmp4Assembler(TestCase):
    def test_icmp4_fpa__ip4_proto_icmp4(self):
        """Test the ip4_proto property of Icmp4Assembler class"""

        self.assertEqual(Icmp4Assembler.ip4_proto, IP4_PROTO_ICMP4)

    def test_icmp4_fpa__assert_ec_id(self):
        """Test assertion for the ec_id"""

        Icmp4Assembler(ec_id=12345)

    def test_icmp4_fpa__assert_ec_id__bellow(self):
        """Test assertion for the ec_id"""

        with self.assertRaises(AssertionError):
            Icmp4Assembler(ec_id=-1)

    def test_icmp4_fpa__assert_ec_id__above(self):
        """Test assertion for the ec_id"""

        with self.assertRaises(AssertionError):
            Icmp4Assembler(ec_id=0x10000)

    def test_icmp4_fpa__assert_ec_seq(self):
        """Test assertion for the ec_seq"""

        Icmp4Assembler(ec_seq=54321)

    def test_icmp4_fpa__assert_ec_seq__bellow(self):
        """Test assertion for the ec_id"""

        with self.assertRaises(AssertionError):
            Icmp4Assembler(ec_seq=-1)

    def test_icmp4_fpa__assert_ec_seq__above(self):
        """Test assertion for the ec_seq"""

        with self.assertRaises(AssertionError):
            Icmp4Assembler(ec_seq=0x10000)

    def test_icmp4_fpa__assert_unknown_type_code(self):
        """Test assertion for the unknown type/code combination"""

        with self.assertRaises(AssertionError):
            Icmp4Assembler(type=255, code=255)

    def test_icmp4_fpa__constructor__echo_request(self):
        """Test class constructor for Echo Request message"""

        packet = Icmp4Assembler(
            type=ICMP4_ECHO_REQUEST,
            code=0,
            ec_id=12345,
            ec_seq=54321,
            ec_data=b"0123456789ABCDEF",
            echo_tracker=Tracker(prefix="TX"),
        )

        self.assertEqual(packet._ec_id, 12345)
        self.assertEqual(packet._ec_seq, 54321)
        self.assertEqual(packet._ec_data, b"0123456789ABCDEF")
        self.assertTrue(repr(packet.tracker._echo_tracker).startswith("Tracker(serial='<lr>TX"))

    def test_icmp4_fpa__constructor__echo_request__assert_code_under(self):
        """Test class constructor for Echo Request message"""

        with self.assertRaises(AssertionError):
            Icmp4Assembler(
                type=ICMP4_ECHO_REQUEST,
                code=-1,
            )

    def test_icmp4_fpa__constructor__echo_request__assert_code_above(self):
        """Test class constructor for Echo Request message"""

        with self.assertRaises(AssertionError):
            Icmp4Assembler(
                type=ICMP4_ECHO_REQUEST,
                code=1,
            )

    def test_icmp4_fpa__constructor__unreachable_port(self):
        """Test class constructor for Unreachable Port message"""

        packet = Icmp4Assembler(
            type=ICMP4_UNREACHABLE,
            code=ICMP4_UNREACHABLE__PORT,
            un_data=b"0123456789ABCDEF" * 50,
            echo_tracker=Tracker(prefix="TX"),
        )

        self.assertEqual(packet._un_data, (b"0123456789ABCDEF" * 50)[:520])
        self.assertTrue(repr(packet.tracker._echo_tracker).startswith("Tracker(serial='<lr>TX"))

    def test_icmp4_fpa__constructor__unreachable_port__assert_code_bellow(self):
        """Test class constructor for Unreachable Port message"""

        with self.assertRaises(AssertionError):
            Icmp4Assembler(
                type=ICMP4_ECHO_REQUEST,
                code=ICMP4_UNREACHABLE__PORT - 1,
            )

    def test_icmp4_fpa__constructor__unreachable_port__assert_code_above(self):
        """Test class constructor for Unreachable Port message"""

        with self.assertRaises(AssertionError):
            Icmp4Assembler(
                type=ICMP4_ECHO_REQUEST,
                code=ICMP4_UNREACHABLE__PORT + 1,
            )

    def test_icmp4_fpa__constructor__echo_reply(self):
        """Test class constructor for Echo Reply message"""

        packet = Icmp4Assembler(
            type=ICMP4_ECHO_REPLY,
            code=0,
            ec_id=12345,
            ec_seq=54321,
            ec_data=b"0123456789ABCDEF",
            echo_tracker=Tracker(prefix="TX"),
        )

        self.assertEqual(packet._ec_id, 12345)
        self.assertEqual(packet._ec_seq, 54321)
        self.assertEqual(packet._ec_data, b"0123456789ABCDEF")
        self.assertTrue(repr(packet.tracker._echo_tracker).startswith("Tracker(serial='<lr>TX"))

    def test_icmp4_fpa__constructor__echo_reply__assert_code_under(self):
        """Test class constructor for Echo Reply message"""

        with self.assertRaises(AssertionError):
            Icmp4Assembler(
                type=ICMP4_ECHO_REPLY,
                code=-1,
            )

    def test_icmp4_fpa__constructor__echo_reply__assert_code_above(self):
        """Test class constructor for Echo Reply message"""

        with self.assertRaises(AssertionError):
            Icmp4Assembler(
                type=ICMP4_ECHO_REPLY,
                code=1,
            )

    def test_icmp4_fpa__constructor__unknown(self):
        """Test class constructor for message with unknown type"""

        with self.assertRaises(AssertionError):
            Icmp4Assembler(
                type=255,
            )

    def test_icmp4_fpa____len____echo_reply(self):
        """Test class __len__ operator"""

        packet = Icmp4Assembler(
            type=ICMP4_ECHO_REPLY,
            code=0,
            ec_data=b"0123456789ABCDEF",
        )

        self.assertEqual(len(packet), ICMP4_ECHO_REPLY_LEN + 16)

    def test_icmp4_fpa____len____unreachable_port(self):
        """Test class __len__ operator"""

        packet = Icmp4Assembler(
            type=ICMP4_UNREACHABLE,
            code=ICMP4_UNREACHABLE__PORT,
            un_data=b"0123456789ABCDEF",
        )

        self.assertEqual(len(packet), ICMP4_UNREACHABLE_LEN + 16)

    def test_icmp4_fpa____len____echo_request(self):
        """Test class __len__ operator"""

        packet = Icmp4Assembler(
            type=ICMP4_ECHO_REQUEST,
            code=0,
            ec_data=b"0123456789ABCDEF",
        )

        self.assertEqual(len(packet), ICMP4_ECHO_REQUEST_LEN + 16)

    def test_icmp4_fpa____str____echo_reply(self):
        """Test class __str__ operator"""

        packet = Icmp4Assembler(
            type=ICMP4_ECHO_REPLY,
            code=0,
            ec_id=12345,
            ec_seq=54321,
            ec_data=b"0123456789ABCDEF",
        )
        self.assertEqual(str(packet), "ICMPv4 0/0 (echo_reply), id 12345, seq 54321, dlen 16")

    def test_icmp4_fpa____str____unreachable_port(self):
        """Test class __str__ operator"""

        packet = Icmp4Assembler(
            type=ICMP4_UNREACHABLE,
            code=ICMP4_UNREACHABLE__PORT,
            un_data=b"0123456789ABCDEF",
        )
        self.assertEqual(str(packet), "ICMPv4 3/3 (unreachable_port), dlen 16")

    def test_icmp4_fpa____str____echo_request(self):
        """Test class __str__ operator"""

        packet = Icmp4Assembler(
            type=ICMP4_ECHO_REQUEST,
            code=0,
            ec_id=12345,
            ec_seq=54321,
            ec_data=b"0123456789ABCDEF",
        )
        self.assertEqual(str(packet), "ICMPv4 8/0 (echo_request), id 12345, seq 54321, dlen 16")

    def test_icmp4_fpa__tracker_getter(self):
        """Test tracker getter"""

        packet = Icmp4Assembler()
        self.assertTrue(repr(packet.tracker).startswith("Tracker(serial='<lr>TX"))

    def test_icmp4_fpa__assemble__echo_reply(self):
        """Test assemble method"""

        packet = Icmp4Assembler(
            type=ICMP4_ECHO_REPLY,
            code=0,
            ec_id=12345,
            ec_seq=54321,
            ec_data=b"0123456789ABCDEF",
        )

        frame = memoryview(bytearray(ICMP4_ECHO_REPLY_LEN + 16))
        packet.assemble(frame)
        self.assertEqual(bytes(frame), b"\x00\x00,\xbe09\xd410123456789ABCDEF")

    def test_icmp4_fpa__asssemble__unreachable_port(self):
        """Test assemble method"""

        packet = Icmp4Assembler(
            type=ICMP4_UNREACHABLE,
            code=ICMP4_UNREACHABLE__PORT,
            un_data=b"0123456789ABCDEF",
        )

        frame = memoryview(bytearray(ICMP4_ECHO_REPLY_LEN + 16))
        packet.assemble(frame)
        self.assertEqual(bytes(frame), b"\x03\x03.&\x00\x00\x00\x000123456789ABCDEF")

    def test_icmp4_fpa__assemble__echo_request(self):
        """Test assemble method"""

        packet = Icmp4Assembler(
            type=ICMP4_ECHO_REQUEST,
            code=0,
            ec_id=12345,
            ec_seq=54321,
            ec_data=b"0123456789ABCDEF",
        )

        frame = memoryview(bytearray(ICMP4_ECHO_REQUEST_LEN + 16))
        packet.assemble(frame)
        self.assertEqual(bytes(frame), b"\x08\x00$\xbe09\xd410123456789ABCDEF")