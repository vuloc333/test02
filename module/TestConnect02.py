from TestConnect import PlcData

class Plc:
    def __init__(self):
        self.plc = PlcData('192.168.2.43', 0, 1, 98, 20, 99)
        self.ConnectStatus = self.plc.ConnectStatus
        if self.ConnectStatus:
            print("Connected to PLC SIM successfully!")
        else:
            print("Connection failed!")
    
    def MoveByte(self, arWriteData, byte_index, value):
        # Chuyển int thành 2 byte (big-endian)
        byte_value = value.to_bytes(2, byteorder='big', signed=True)
        # Gán vào mảng write_buffer tại vị trí byte_index
        arWriteData[byte_index:byte_index+2] = byte_value
    
    def Getbyte(self, iByte):
        return int.from_bytes(self.arReadData[iByte:iByte+2], byteorder='big', signed=True)

    def UpdateData(self, i_bits, i_ints, o_bits, o_ints):

        self.arReadData = self.plc.update_read_buffer()
    #Read Data
        for i in range(8):
            i_bits[i] = bool(self.arReadData[0] & (1 << i))
            i_bits[i + 8] = bool(self.arReadData[1] & (1 << i))

        for i in range(10):
            i_ints[i] = self.Getbyte(2 + i * 2)

    # Write Data
        arWriteData = bytearray(22)  # Tạo mảng byte để ghi dữ liệu
        for i in range(8):
            arWriteData[0] |= o_bits[i] << i
            arWriteData[1] |= o_bits[i + 8] << i

        for i in range(10):
            self.MoveByte(arWriteData, 2 + i * 2, o_ints[i])  # Ghi các giá trị int vào các byte tương ứng

        self.plc.update_write_buffer(arWriteData)