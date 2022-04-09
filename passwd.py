import requests
import led
import mqtt_x
def get_passwd():
    data = {
        'passwd': 'password'
    }
    r = requests.post("http://192.168.1.146:8888/api",data=data)
    print("r.text = ",r.text)
    return r.text
    

def main():
    while True:
        passwd = input("请输入密码:")
        print("pwd",passwd)
        if passwd == get_passwd():
            led.led()
        else:
            mqtt_x.run()





if __name__ == '__main__':
    main()