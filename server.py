from flask import Flask, render_template, request, redirect, url_for
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Configuração do Flask
app = Flask(__name__)

# Configuração do Google Sheets
def get_google_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("CorridaRio2025").sheet1  # Altere para o nome da sua planilha
    return sheet

# Rota principal (formulário)
@app.route('/')
def index():
    return render_template('index.html')

# Rota para processar o formulário
@app.route('/submit', methods=['POST'])
def submit():
    # Coletar dados do formulário
    team_name = request.form['team_name']
    athletes = request.form.getlist('athletes[]')  # Lista de atletas

    # Salvar dados no Google Sheets
    sheet = get_google_sheet()
    for athlete in athletes:
        sheet.append_row([team_name, athlete])  # Adicione mais campos conforme necessário

    return redirect(url_for('index'))

# Iniciar o servidor
if __name__ == '__main__':
    app.run(debug=True)