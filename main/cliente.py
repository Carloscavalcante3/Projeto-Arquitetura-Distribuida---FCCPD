import socket

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8888

def main():
    print("--- Cliente de Teste ---")
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            print("\n[CONECTANDO] Conectando ao servidor...")
            client_socket.connect((SERVER_HOST, SERVER_PORT))
            print("[CONECTADO] Conexão estabelecida.")
            
            mensagem_simples = "Testando conexão"
            client_socket.sendall(mensagem_simples.encode('utf-8'))
            
            resposta = client_socket.recv(1024)
            print(f"[SERVIDOR]: {resposta.decode('utf-8')}")

    except ConnectionRefusedError:
        print("\n[ERRO] Não foi possível conectar ao servidor.")
    except Exception as e:
        print(f"\n[ERRO INESPERADO] {e}")

if __name__ == "__main__":
    main()