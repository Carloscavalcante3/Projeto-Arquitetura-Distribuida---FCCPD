
import socket
import json

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8888

def exibir_menu():
    print("\n--- Portal de Denúncia Anônima ---")
    print("Selecione o tipo de ocorrência:")
    tipos = {
        "1": "Vandalismo",
        "2": "Roubo / Furto",
        "3": "Tráfico de Drogas",
        "4": "Poluição Sonora",
        "5": "Violência Doméstica",
        "0": "Outro"
    }
    for key, value in tipos.items():
        print(f"[{key}] - {value}")
    
    escolha = input("> ")
    return tipos.get(escolha, "Outro")

def main():
    tipo_denuncia = exibir_menu()
    
    print(f"\nTipo selecionado: {tipo_denuncia}")
    local = input("Digite o local da ocorrência (ex: Rua, Bairro, Ponto de Referência):\n> ")
    descricao = input("Descreva a ocorrência com o máximo de detalhes possível:\n> ")
    
    denuncia = {
        "tipo": tipo_denuncia,
        "local": local,
        "descricao": descricao
    }
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            print("\n[CONECTANDO] Conectando ao servidor...")
            client_socket.connect((SERVER_HOST, SERVER_PORT))
            print("[CONECTADO] Conexão estabelecida.")
            
            client_socket.sendall(json.dumps(denuncia).encode('utf-8'))
            
            resposta_bytes = client_socket.recv(1024)
            resposta = json.loads(resposta_bytes.decode('utf-8'))
            
            if resposta.get("status") == "sucesso":
                print("\n--- CONFIRMAÇÃO ---")
                print(f"Status: {resposta.get('mensagem')}")
                print(f"Seu número de protocolo é: {resposta.get('protocolo')}")
                print("---------------------")
            else:
                print(f"[ERRO] Falha ao registrar denúncia: {resposta.get('mensagem')}")

    except ConnectionRefusedError:
        print("\n[ERRO] Não foi possível conectar ao servidor. Verifique se o servidor está online.")
    except Exception as e:
        print(f"\n[ERRO INESPERADO] Ocorreu um erro: {e}")

if __name__ == "__main__":
    main()