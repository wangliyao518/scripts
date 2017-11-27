# -*- coding: utf-8 -*-
"""
:author: leo
:contact: leo wang
"""
import prophy
import sys


EMonitorMode_All = 1
EMonitorType_ApiHeader = 1


# class EMonitorMode(prophy.enum):
#     __metaclass__ = prophy.enum_generator
#     _enumerators = [('EMonitorMode_None', 0),
#                     ('EMonitorMode_All', 1),
#                     ('EMonitorMode_TxOnly', 2),
#                     ('EMonitorMode_RxOnly', 3)]
# 
# 
# class EMonitorType(prophy.enum):
#     __metaclass__ = prophy.enum_generator
#     _enumerators = [('EMonitorType_None', 0),
#                     ('EMonitorType_ApiHeader', 1),
#                     ('EMonitorType_DscBus', 2),
#                     ('EMonitorType_CdBus', 3),
#                     ('EMonitorType_PciBus', 4),
#                     ('EMonitorType_AtmVc', 5),
#                     ('EMonitorType_AtmAal2', 6),
#                     ('EMonitorType_AtmAal5', 7),
#                     ('EMonitorType_BtsFp', 8),
#                     ('EMonitorType_Ethernet', 9),
#                     ('EMonitorType_Ip', 10),
#                     ('EMonitorType_SwBus', 11),
#                     ('EMonitorType_UdpPort', 12),
#                     ('EMonitorType_Raw', 99)]
# 
# 
# class SAaTraceMsgIdHeavyLoadFilter(prophy.struct):
#     __metaclass__ = prophy.struct_generator
#     _descriptor = [('msgId2', prophy.array(prophy.u32, size=8)),
#                    ('extraFilter', prophy.array(prophy.u32, size=8))]
# 
# 
# class SAaTraceMsgIdFilter(prophy.struct):
#     __metaclass__ = prophy.struct_generator
#     _descriptor = [('msgId', prophy.array(prophy.u32, size=128)),
#                    ('msgIdRange', prophy.array(prophy.u8, size=64))]
# 
# 
# 
# class SAaTraceMonCtrlParams(prophy.struct):
#     __metaclass__ = prophy.struct_generator
#     _descriptor = [('mode', EMonitorMode),
#                    ('type', EMonitorType),
#                    ('sAaTraceMsgIdFilter', SAaTraceMsgIdFilter),
#                    ('sAaTraceMsgIdHeavyLoadFilter', SAaTraceMsgIdHeavyLoadFilter),
#                    ('routingTarget', SMessageAddress),
#                    ('ifFormat', prophy.u32)]
# 
# 
# class AaTraceMonCtrlReqMsg(prophy.struct):
#     __metaclass__ = prophy.struct_generator
#     _descriptor = [('sAaTraceMonCtrlParams', SAaTraceMonCtrlParams)]
# 
# 
# class AaTraceMonCtrlRespMsg(prophy.struct):
#     __metaclass__ = prophy.struct_generator
#     _descriptor = [('successCode', prophy.u32)]
# 
# 
# class AaTraceMonIndMsg(prophy.struct):
#     __metaclass__ = prophy.struct_generator
#     _descriptor = [('type', EMonitorType),
#                    ('mode', EMonitorMode),
#                    ('sequence', prophy.u32),
#                    ('extra', prophy.array(prophy.u32, size=4)),
#                    ('dataLen', prophy.u32),
#                    ('data', prophy.bytes(bound='dataLen'))]


class ECarrierBandwidth(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators = [('ECarrierBandwidth_NotDefined', 0),
                    ('ECarrierBandwidth_1_4MHz', 6),
                    ('ECarrierBandwidth_3MHz', 15),
                    ('ECarrierBandwidth_5MHz', 25),
                    ('ECarrierBandwidth_10MHz', 50),
                    ('ECarrierBandwidth_15MHz', 75),
                    ('ECarrierBandwidth_20MHz', 100),
                    ('ECarrierBandwidth_05_05MHz', 2525),
                    ('ECarrierBandwidth_05_10MHz', 2550),
                    ('ECarrierBandwidth_10_05MHz', 5025),
                    ('ECarrierBandwidth_10_10MHz', 5050)]

class SMessageAddress(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('TBoard', prophy.u8),
                   ('TCpu', prophy.u8),
                   ('TTask', prophy.u16)]

    
class flags(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('system', prophy.u8),
                   ('user', prophy.u8)]

class MsgHeader(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('id', prophy.u32),
                   ('receiver', SMessageAddress),
                   ('sender', SMessageAddress),
                   ('length', prophy.u16),
                   ('flags', flags)]


class LoglevelQueryRequest(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('MsgHeader', MsgHeader),
                   ('numOfCarrierBw', prophy.u32),
                   ('ECarrierBandwidth', prophy.u32)]


class APF(object):

    APFSTR2NUM = {
        'EAaSysComMsgApf_32Big': (0, ">"),
        'EAaSysComMsgApf_32Little': (1, "<"),
        'EAaSysComMsgApf_8Big': (2, ">"),
        'EAaSysComMsgApf_8Little': (3, "<"),
    }

    NUM2STRAPF = {
        0: ('EAaSysComMsgApf_32Big', ">"),
        1: ('EAaSysComMsgApf_32Little', "<"),
        2: ('EAaSysComMsgApf_8Big', ">"),
        3: ('EAaSysComMsgApf_8Little', "<"),
    }

    def __init__(self, mode):
        self._mode = mode
        self._apf = self.get_default(mode)

    @property
    def apf(self):
        """Returns APF."""
        return self._apf

    @property
    def bracket(self):
        """Returns APF bracket."""
        return self.APFSTR2NUM[self._apf][1]

    @property
    def msg_flag(self):
        """Returns APF message flag."""
        return self.APFSTR2NUM[self._apf][0] << 2

    @property
    def version(self):
        """Returns APF type."""
        return self._apf.replace("EAaSysComMsgApf_", "")

    @property
    def endianness(self):
        """Returns APF endianness."""
        return "big" if "Big" in self._apf else "little"

    def get_default(self, mode):
        """Get default APF based on provided mode."""
        return 'EAaSysComMsgApf_32Big'
        if mode == "word":
            if self.is_little_endian():
                return 'EAaSysComMsgApf_32Little'
            return 'EAaSysComMsgApf_32Big'
        else:
            if self.is_little_endian():
                return 'EAaSysComMsgApf_8Little'
            return 'EAaSysComMsgApf_8Big'

    def set_apf(self, num):
        """Set APF based on provided number."""
        self._apf = self.NUM2STRAPF[num][0]

    def is_same_apf(self, apf):
        """Check if provided APF is the same APF."""
        return self._apf == apf

    def is_8bit(self):
        """Check if APF is set to 8 bit."""
        return '8' in self._apf

    def is_32bit(self):
        """Check if APF is set to 32 bit."""
        return '32' in self._apf

    def is_little_endian(self):
        """Check if system bit order is set to little endian."""
        return True if sys.byteorder == "little" else False

# apf = APF()
# size = 16 + len(data)
# req = MsgHeader()
# req.id = 0x27e1
# req.receiver.TBoard=0x12
# req.receiver.TCpu=0x32
# req.receiver.TTask=0x2121
# req.sender.TBoard=0x00
# req.sender.TCpu=0x00
# req.sender.TTask=0x0000
# req.length =0x0014
# req.flags.system =0x00
# req.flags.user =0x00

# print req
# request.MsgHeader = req
request = LoglevelQueryRequest()

request.MsgHeader.id = 0x27e1
request.MsgHeader.receiver.TBoard=0x12
request.MsgHeader.receiver.TCpu=0x32
request.MsgHeader.receiver.TTask=0x2121
request.MsgHeader.sender.TBoard=0x00
request.MsgHeader.sender.TCpu=0x00
request.MsgHeader.sender.TTask=0x0000
request.MsgHeader.length =0x0014
request.MsgHeader.flags.system =0x00
request.MsgHeader.flags.user =0x00

request.numOfCarrierBw = 0x00
request.ECarrierBandwidth =0x00

print request
a=request.encode('>')
# print a




