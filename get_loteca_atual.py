import requests
from bs4 import BeautifulSoup
import json
import os

def scraping_loteca():
    # URL de exemplo (Sorte Online é estável para scraping de programação)
    url = "https://www.sorteonline.com.br/loteca/programacao"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Erro ao acessar site: {response.status_code}")
            return

        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Encontrar o número do concurso
        concurso_tag = soup.find("span", class_="header-resultados__concurso")
        concurso_num = concurso_tag.text.strip() if concurso_tag else "0"

        jogos = []
        # Localizar a tabela ou os cards de jogos (ajustar seletores conforme o site)
        lista_jogos = soup.find_all("div", class_="card-programacao")

        for i, item in enumerate(lista_jogos[:14]):
            try:
                # Extração dos nomes dos times
                times = item.find_all("span", class_="card-programacao__time")
                time_casa = times[0].text.strip()
                time_fora = times[1].text.strip()
                
                # Dia da semana/Data
                info_dia = item.find("div", class_="card-programacao__data").text.strip()

                jogos.append({
                    "posicao": i + 1,
                    "time_casa": time_casa,
                    "time_fora": time_fora,
                    "info": info_dia
                })
            except Exception as e:
                print(f"Erro no jogo {i+1}: {e}")

        dados_finais = {
            "concurso": concurso_num,
            "jogos": jogos
        }

        # Salva o JSON
        with open("dados_loterias/loteca_atual.json", "w", encoding="utf-8") as f:
            json.dump(dados_finais, f, ensure_ascii=False, indent=4)
        
        print(f"✅ Loteca Concurso {concurso_num} salvo com sucesso!")

    except Exception as e:
        print(f"Erro geral: {e}")

if __name__ == "__main__":
    # Garante que a pasta existe
    if not os.path.exists("dados_loterias"):
        os.makedirs("dados_loterias")
    scraping_loteca()
