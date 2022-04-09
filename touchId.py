import binascii
import serial
import serial.tools.list_ports
import time
import led
import mqtt_x
# volatile unsigned char FPM10A_RECEICE_BUFFER[32];        //定义接收缓存区
# code unsigned char FPM10A_Pack_Head[6] = {0xEF,0x01,0xFF,0xFF,0xFF,0xFF};  //协议包头
# code unsigned char FPM10A_Get_Img[6] = {0x01,0x00,0x03,0x01,0x00,0x05};    //获得指纹图像
# code unsigned char FPM10A_Img_To_Buffer1[7]={0x01,0x00,0x04,0x02,0x01,0x00,0x08}; //将图像放入到BUFFER1
# code unsigned char FPM10A_Search[11]={0x01,0x00,0x08,0x04,0x01,0x00,0x00,0x00,0x64,0x00,0x72}; //搜索指纹搜索范围0 - 999,使用BUFFER1中的特征码搜索
serial = serial.Serial('/dev/ttyUSB0', 57600, timeout=0.5)
def recv(serial):
    while True:
        data = serial.read_all()
        if data == '':
            continue
        else:
            break
    return data

def detect():
    a = 'EF 01 FF FF FF FF 01 00 03 01 00 05'  # 探测手指
    d = bytes.fromhex(a)
    serial.write(d)
    time.sleep(1)
    data =recv(serial)
    if data != b'' :
        data_con = str(binascii.b2a_hex(data))[20:22]
        if(data_con == '02'):   # 02 表示 传感器上没有指纹
            print("未探测到指纹")
            return False
        elif(data_con == '00'):
            print("成功探测指纹")
            return True
        else:
            print("其他原因")
            return False

def character():
    buff = 'EF 01 FF FF FF FF 01 00 04 02 01 00 08'  # 生成特征码
    buff = bytes.fromhex(buff)
    serial.write(buff)
    time.sleep(1)
    buff_data = recv(serial)
    buff_con = str(binascii.b2a_hex(buff_data))[20:22]  
    if(buff_con == '00'): # 生成特征成功
        print("生成特征成功")
        return True
    else:
        print("特征生成失败")
        return False

def judge():
    serch = 'EF 01 FF FF FF FF 01 00 08 04 01 00 00 00 64 00 72'
    serch = bytes.fromhex(serch)
    serial.write(serch)
    time.sleep(1)
    serch_data = recv(serial)
    serch_con = str(binascii.b2a_hex(serch_data))[20:22]
    if (serch_con == '09'):
        print("指纹不匹配")
        mqtt_x.run()
        return False
    elif(serch_con == '00'):
        print("指纹匹配成功")
        return True
    elif (serch_con == '06'):# 图像乱，无法正常生成
        print("图像乱,重试")
        return False


if __name__ == '__main__':
    while True:
        if detect():
            if character() and judge():
                led.led()
            else:
                continue
        else:
            continue