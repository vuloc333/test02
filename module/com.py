import snap7
from snap7.util import get_bool, get_int, set_bool, set_int

class plc_com:
    def __init__(self, ip, rack, slot, read_db, write_db):
        self.client = snap7.client.Client()
        self.params = {'ip': ip, 'rack': rack, 'slot': slot}
        self.db_ids = {'read': read_db, 'write': write_db}
        
        # Buffers thô
        self.read_buffer = bytearray(100)
        self.write_buffer = bytearray(100)

        # Định nghĩa ánh xạ: (Tên biến, Byte, Bit)
        # Nếu là Int thì Bit để None
        self.read_map = [
            ("i_bConnectStatus", 0, 0),
            ("i_bSensor_01", 0, 1),
            ("i_iActualPos", 2, None),
        ]
        
        self.write_map = [
            ("o_bMotor_Start", 0, 1),
            ("o_iTargetSpeed", 2, None),
        ]

    def connect(self):
        self.client.connect(self.params['ip'], self.params['rack'], self.params['slot'])

    def sync_read(self, data_obj):
        """Bước 1 & 2: Đọc DB và Unpack vào Struct"""
        self.read_buffer = self.client.db_read(self.db_ids['read'], 0, len(self.read_buffer))
        for name, byte, bit in self.read_map:
            if bit is not None:
                val = get_bool(self.read_buffer, byte, bit)
            else:
                val = get_int(self.read_buffer, byte)
            setattr(data_obj, name, val)

    def sync_write(self, data_obj):
        """Bước 4 & 5: Pack từ Struct và Ghi xuống DB"""
        for name, byte, bit in self.write_map:
            val = getattr(data_obj, name)
            if bit is not None:
                set_bool(self.write_buffer, byte, bit, val)
            else:
                set_int(self.write_buffer, byte, val)
        self.client.db_write(self.db_ids['write'], 0, self.write_buffer)