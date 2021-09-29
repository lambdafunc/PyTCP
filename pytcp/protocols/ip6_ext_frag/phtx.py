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
# ip6_ext_frag/phtx.py - packet handler for outbound IPv6 fragment extension header
#


from __future__ import annotations  # Required by Python ver < 3.10

from typing import TYPE_CHECKING

import config
from lib.logger import log
from misc.tx_status import TxStatus
from protocols.ip6.ps import IP6_HEADER_LEN
from protocols.ip6_ext_frag.fpa import Ip6ExtFragAssembler
from protocols.ip6_ext_frag.ps import IP6_EXT_FRAG_HEADER_LEN

if TYPE_CHECKING:
    from protocols.ip6.fpa import Ip6Assembler


def _phtx_ip6_ext_frag(self, ip6_packet_tx: Ip6Assembler) -> TxStatus:
    """Handle outbound IPv6 fagment extension header"""

    data = memoryview(bytearray(ip6_packet_tx.dlen))
    ip6_packet_tx._carried_packet.assemble(data, ip6_packet_tx.pshdr_sum)
    data_mtu = (config.TAP_MTU - IP6_HEADER_LEN - IP6_EXT_FRAG_HEADER_LEN) & 0b1111111111111000
    data_frags = [data[_ : data_mtu + _] for _ in range(0, len(data), data_mtu)]
    offset = 0
    self.ip6_id += 1
    ip6_tx_status: set[TxStatus] = set()
    for data_frag in data_frags:
        ip6_ext_frag_tx = Ip6ExtFragAssembler(next=ip6_packet_tx.next, offset=offset, flag_mf=data_frag is not data_frags[-1], id=self.ip6_id, data=data_frag)
        if __debug__:
            log("ip6", f"{ip6_ext_frag_tx.tracker} - {ip6_ext_frag_tx}")
        ip6_tx_status.add(self._phtx_ip6(ip6_src=ip6_packet_tx.src, ip6_dst=ip6_packet_tx.dst, carried_packet=ip6_ext_frag_tx))
        offset += len(data_frag)

    # Return the most severe code
    for tx_status in [
        TxStatus.DROPED_ETHER_RESOLUTION_FAIL,
        TxStatus.DROPED_ETHER_NO_GATEWAY,
        TxStatus.DROPED_ETHER_CACHE_FAIL,
        TxStatus.DROPED_ETHER_GATEWAY_CACHE_FAIL,
        TxStatus.PASSED_TO_TX_RING,
    ]:
        if tx_status in ip6_tx_status:
            return tx_status

    return TxStatus.DROPED_IP6_EXT_FRAG_UNKNOWN