import socket
import threading

print("-------------[DS.hack Team]-------------")
print("-------------{Do not perform illegal activities}------------")

# Use a thread-safe dictionary or protect access to a regular dictionary with a lock
# Since Python's built-in dict is not thread-safe, we need to use a lock to ensure thread safety
lock = threading.Lock()
# Instead of using a global variable as the output container, we return it as the output of the scan_port function

def Tcp_connect(ip, port_number, delay, shared_dict, shared_lock):
    TCPsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCPsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TCPsock.settimeout(delay)

    # Before attempting to connect, check and set the port status to 'closed' (use lock to ensure thread safety)
    with shared_lock:
        if port_number not in shared_dict:
            shared_dict[port_number] = 'closed'

    try:
        TCPsock.connect((ip, port_number))
        # After successful connection, update the port status to 'open' (use lock to ensure thread safety)
        with shared_lock:
            shared_dict[port_number] = 'open'
    except Exception as e:
        # You can log the exception information, but for now, we'll ignore it
        pass
    finally:
        TCPsock.close()

def scan_port(host_ip, delay):
    threads = []
    # Use a dictionary to store port scan results and protect access to it with a lock
    port_status = {}

    for i in range(1, 10001):  # Note that port numbers start from 1 to 10000
        t = threading.Thread(target=Tcp_connect, args=(host_ip, i, delay, port_status, lock))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # Print the open ports
    for port, status in port_status.items():
        if status == 'open':
            print(f"Port {port}: {status}")

    return port_status  # If needed, you can return the port status dictionary for subsequent use

def main():
    host_ip = input("Enter the specified IP: ")
    delay = int(input("Enter the timeout duration in seconds: "))
    # Call the scan_port function and wait for the scan to complete
    scan_port(host_ip, delay)
    input("Scan completed, press any key to exit...")

if __name__ == '__main__':
    main()
