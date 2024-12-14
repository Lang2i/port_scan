import socket
import threading

print("-------------[DS.hack团队]-------------")
print("-------------{请勿做违法行为}------------")

# 使用一个线程安全的字典，或者通过锁来保护对普通字典的访问
# 由于Python的内置dict不是线程安全的，我们需要使用锁来确保线程安全
lock = threading.Lock()
# 这里不再使用全局变量作为输出容器，而是将其作为scan_port函数的返回值

def Tcp_connect(ip, port_number, delay, shared_dict, shared_lock):
    TCPsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCPsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TCPsock.settimeout(delay)

    # 尝试连接前，先检查并设置端口状态为'closed'（使用锁确保线程安全）
    with shared_lock:
        if port_number not in shared_dict:
            shared_dict[port_number] = 'closed'

    try:
        TCPsock.connect((ip, port_number))
        # 连接成功后，更新端口状态为'open'（使用锁确保线程安全）
        with shared_lock:
            shared_dict[port_number] = 'open'
    except Exception as e:
        # 可以记录异常信息，这里暂时忽略
        pass
    finally:
        TCPsock.close()

def scan_port(host_ip, delay):
    threads = []
    # 使用一个字典来存储端口扫描结果，并通过锁来保护对它的访问
    port_status = {}

    for i in range(1, 10001):  # 注意端口号从1开始到10000
        t = threading.Thread(target=Tcp_connect, args=(host_ip, i, delay, port_status, lock))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # 打印打开的端口
    for port, status in port_status.items():
        if status == 'open':
            print(f"Port {port}: {status}")

    return port_status  # 如果需要，可以返回端口状态字典供后续使用

def main():
    host_ip = input("输入指定IP: ")
    delay = int(input("输入多少秒后抛出异常（超时时间）: "))
    # 调用scan_port函数并等待扫描完成
    scan_port(host_ip, delay)
    input("扫描完成，按下任意键退出...")

if __name__ == '__main__':
    main()