from flask import Flask, render_template, request, redirect, url_for
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# Configuração do Flask
app = Flask(__name__)

# Escopos necessários
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Caminho para o arquivo de credenciais
CREDENTIALS_PATH = "./config/credentials.json"

# Função de validação de data
def validar_data(data_str):
    try:
        # Aceita tanto '/' quanto '-' como separadores
        data = datetime.strptime(data_str.replace('-', '/'), '%d/%m/%Y')
        
        # Verifica se a data é no futuro
        if data.date() > datetime.now().date():
            return None
            
        # Formata para o padrão do Sheets (DD/MM/YYYY como string)
        return data.strftime('%d/%m/%Y')
    except ValueError:
        return None

# Inicialização do cliente do Google Sheets
try:
    creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
    client = gspread.authorize(creds)
    print("✅ Autenticação com o Google Sheets bem-sucedida!")
except Exception as e:
    print(f"❌ Erro na autenticação: {str(e)}")
    client = None

# Rotas
@app.route('/')
def index():
    if not client:
        return "Erro de autenticação com o Google Sheets. Verifique as credenciais.", 500
    
    try:
        # Renderiza o formulário HTML
        return render_template('index.html')
    except Exception as e:
        return f"Erro ao carregar o formulário: {str(e)}", 500

@app.route('/test')
def test_sheets():
    if not client:
        return "Cliente do Google Sheets não inicializado.", 500
    
    try:
        # Acessa a planilha template
        template = client.open("Template_Corrida")
        worksheet = template.worksheet('Atletas')
        
        # Verifica os cabeçalhos
        headers = worksheet.row_values(1)
        if len(headers) != len(set(headers)):
            return "Erro: Cabeçalhos duplicados na aba 'Atletas'.", 400
        
        # Recupera todos os registros
        records = worksheet.get_all_records()
        
        # Exibe os dados
        return f"""
            <h1>Teste de Autenticação</h1>
            <p>✅ Conexão com o Google Sheets bem-sucedida!</p>
            <p>📊 Total de registros na aba 'Atletas': {len(records)}</p>
            <p>🔍 Cabeçalhos: {headers}</p>
            <h2>Dados:</h2>
            <pre>{records}</pre>
        """
    except gspread.SpreadsheetNotFound:
        return "Planilha 'Template_Corrida' não encontrada. Verifique o nome e as permissões.", 404
    except Exception as e:
        return f"Erro durante o teste: {str(e)}", 500

@app.route('/submit', methods=['POST'])
def salvar():
    if not client:
        return "Erro de autenticação com o Google Sheets. Verifique as credenciais.", 500
    
    try:
        # Coleta os dados do formulário
        team_name = request.form['team_name']
        athletes = request.form.getlist('athletes[]')
        birth_dates = request.form.getlist('birth_dates[]')
        shirt_sizes = request.form.getlist('shirt_sizes[]')

        # Validação de dados
        if not all([team_name, athletes, birth_dates, shirt_sizes]):
            return "Dados incompletos", 400

        # Prepara linhas para o Sheets
        linhas = []
        for i in range(len(athletes)):
            data_validada = validar_data(birth_dates[i])
            if not data_validada:
                return f"Data inválida para o atleta {i+1}", 400
            
            linhas.append([
                team_name,
                athletes[i],
                data_validada,
                shirt_sizes[i].upper()
            ])

        # Salva na planilha
        planilha = client.open("Template_Corrida")
        worksheet = planilha.worksheet('Atletas')
        worksheet.append_rows(linhas, value_input_option='USER_ENTERED')
        
        return redirect(url_for('index'))
    except Exception as e:
        return f"Erro ao salvar os dados: {str(e)}", 500

# Inicialização do servidor
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)