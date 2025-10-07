
import socket
import threading
import json
from datetime import datetime
import uuid

HOST = '127.0.0.1'
PORT = 8888
LOG_FILE = 'denuncias.json'

file_lock = threading.Lock()

def carregar_denuncias():
    try:
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def salvar_denuncia(denuncia):
    with file_lock:
        denuncias = carregar_denuncias()
        denuncias.append(denuncia)
        with open(LOG_FILE, 'w', encoding='utf-8') as f:
            json.dump(denuncias, f, indent=4, ensure_ascii=False)

def handle_client(conn, addr):
    print(f"[NOVA CONEXÃO] {addr} conectado.")
    
    try:
        data = conn.recv(1024)
        if not data:
            return
        
        denuncia_cliente = json.loads(data.decode('utf-8'))
        print(f"[{addr}] Denúncia recebida: {denuncia_cliente['tipo']}")

        denuncia_completa = {
            "protocolo": str(uuid.uuid4()),
            "timestamp_recebimento": datetime.now().isoformat(),
            "tipo": denuncia_cliente.get("tipo", "Não especificado"),
            "local": denuncia_cliente.get("local", "Não especificado"),
            "descricao": denuncia_cliente.get("descricao", "")
        }

        salvar_denuncia(denuncia_completa)
        
        resposta = {
            "status": "sucesso",
            "mensagem": "Denúncia registrada com sucesso!",
            "protocolo": denuncia_completa["protocolo"]
        }
        conn.sendall(json.dumps(resposta).encode('utf-8'))

    except (json.JSONDecodeError, KeyError) as e:
        print(f"[ERRO] Erro ao processar dados de {addr}: {e}")
        resposta_erro = {"status": "erro", "mensagem": "Dados da denúncia inválidos."}
        conn.sendall(json.dumps(resposta_erro).encode('utf-8'))
    except Exception as e:
        print(f"[ERRO INESPERADO] {e}")
    finally:
        conn.close()
        print(f"[A CONEXÃO FOI ENCERRADA] {addr}")

def main():
    print("[INICIANDO] O Servidor de denúncias está sendo iniciado")
    
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