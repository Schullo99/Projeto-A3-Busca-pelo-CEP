import requests
from geopy.geocoders import Nominatim

# 1. Defina o CEP
cep_rio_bonito = "85345-000" 

# --- ETAPA 1: CEP para Endereço (Usando ViaCEP) ---

print(f"Buscando endereço para o CEP: {cep_rio_bonito}...")

url_viacep = f"https://viacep.com.br/ws/{cep_rio_bonito}/json/"
try:
    response = requests.get(url_viacep)
    response.raise_for_status() # Lança exceção para códigos de status ruins (4xx ou 5xx)
    dados_endereco = response.json()
except requests.exceptions.RequestException as e:
    print(f"Erro ao consultar a API ViaCEP: {e}")
    dados_endereco = None

if dados_endereco and 'erro' not in dados_endereco:
    # A base de dados dos Correios para este CEP principal retorna apenas
    # a Cidade e Estado, pois é um CEP de uso geral (único para toda a cidade).
    cidade = dados_endereco.get('localidade', '')
    uf = dados_endereco.get('uf', '')
    
    # Monta a string de endereço para geocodificação
    endereco_completo = f"{cidade}, {uf}, Brasil"
    print(f"Endereço encontrado: {endereco_completo}")

    # --- ETAPA 2: Endereço para Coordenadas (Usando Geopy/Nominatim) ---
    
    # Inicializa o geocodificador do Nominatim (OpenStreetMap)
    # É necessário definir um 'user_agent'
    geolocator = Nominatim(user_agent="geocodificador_personalizado")
    print("Buscando coordenadas...")
    
    try:
        # Busca as coordenadas
        location = geolocator.geocode(endereco_completo, timeout=10)

        if location:
            print("-" * 30)
            print("✨ LOCALIZAÇÃO ENCONTRADA ✨")
            print(f"Cidade/Estado: {endereco_completo}")
            print(f"Latitude: **{location.latitude}**")
            print(f"Longitude: **{location.longitude}**")
            print("-" * 30)
        else:
            print("Não foi possível encontrar as coordenadas para este endereço.")
    
    except Exception as e:
        print(f"Erro ao geocodificar com Nominatim: {e}")

else:
    print("CEP não encontrado ou erro na resposta da API.")