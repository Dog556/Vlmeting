from model import get_infos,send,abc,get_info,upload_file
from database import insert_unique_data,clear_db,create_db
from config import get_server
import time
import argparse


parser = argparse.ArgumentParser(description='\033[31m[+]Wecome Vlmeting! Vlmeting! 作者:by carrot!\033[0m')
parser.add_argument('-s', action='store_true', help='启动服务Service')
parser.add_argument('-c', action='store_true', help='清理数据,还原最初数据')
parser.add_argument('-t', metavar='--time', type=str, help='指定多少分钟运行一次，单位min')
parser.add_argument('-f', action='store_true', help='启用字典模式')
args,unknown = parser.parse_known_args()

def main():
    print("\033[32m[+]Wecome Vlmeting! 作者:by carrot!\033[0m")
    print("[*]仅提供学习与交流，请勿用于非法与商业用途，交流群:611149449")
    if args.s:
        if args.f:
            data_new = get_infos()
        else:
            data_new = get_info()
        if abc(data_new) == False:
            print("\033[32m[+]The data is new and the data has been updated!\033[0m")
            print("\033[32m[+]join......\033[0m")
            time.sleep(5)
            data = data_new
            print(data_new)
            new_data = insert_unique_data(data)
            print("\033[32m[+]Data insert Succeed\033[0m")
            upload_file("data.db")
            print("\033[32m[+]Web Update Succeed\033[0m")
            time.sleep(4)
            sentence = ' '.join(send(new_data))
            get_server(sentence)
            time.sleep(5)
            print("\033[32m[+]Succeed!\033[0m")
        else:
            data = data_new
            print(f"[+]{data}")
            print("\033[31m[-]The data is unchanged\033[0m")
    else:
        print("\033[31m[-]You haven't set the parameters yet! Pleases -s???\033[0m")


if __name__ == '__main__':
    create_db()#创建数据库
    if args.c:
        clear_db()  # 清除数据库
    if args.t or args.s:
        times = int(args.t)
        while True:
            print("\033[32m[+]Procedure runing......\033[0m")
            main()
            time.sleep(times * 60)
    else:
        print("\033[31m[-]You haven't specified the parameters yet  Pleases -t or-s???\033[0m")