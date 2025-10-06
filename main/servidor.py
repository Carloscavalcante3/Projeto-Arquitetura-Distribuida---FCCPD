import socket
import threading

HOST = '127.0.0.1'
PORT = 8888

def handle_client(conn, addr):
    print(f"[NOVA CONEXÃO] {addr} conectado.")
    
    try:
        data = conn.recv(1024)
        if data:
            print(f"[{addr}]: {data.decode('utf-8')}")
            
            # Resposta simples para o cliente
            conn.sendall(b"Mensagem recebida pelo servidor!")

    except Exception as e:
        print(f"[ERRO] {e}")
    finally:
        conn.close()
        print(f"[CONEXÃO ENCERRADA] {addr}")

def main():
    print("[INICIANDO] Servidor está iniciando...")
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    
    print(f"[ESCUTANDO] Servidor escutando em {HOST}:{PORT}")
    
    while True:
        conn, addr = server.accept()
        
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        
        print(f"[CONEXÕES ATIVAS] {threading.active_count() - 1}")

if __name__ == "__main__":
    main()