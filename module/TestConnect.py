import snap7
from snap7.util import *

class PlcData:
    def __init__(self, ip, rack, slot, read_db, read_maxbyte, write_db):
        self.plc = snap7.client.Client()
        self.read_db = read_db
        self.read_maxbyte = read_maxbyte
        self.write_db = write_db
        
        try:
            self.plc.connect(ip, rack, slot)
        except:
            pass
            
        self.ConnectStatus = self.plc.get_connected()
        # Khởi tạo mảng rỗng để tránh lỗi nếu chưa đọc được ngay
        self.arReadData = bytearray(read_maxbyte) 

    def update_read_buffer(self):
        return self.plc.db_read(self.read_db, 0, self.read_maxbyte)
    
    def update_write_buffer(self, arWriteData):
        self.plc.db_write(self.write_db, 0, arWriteData)

