class Decoder:
    @staticmethod
    def convertToUTF(byte_list: bytearray) -> str:
        return byte_list.decode("utf-8")