// Função para adicionar um novo atleta ao formulário
document.getElementById('add-athlete').addEventListener('click', function() {
    // 1. Seleciona o container de atletas
    const container = document.getElementById('atletas-container');
    
    // 2. Seleciona o template do primeiro atleta
    const template = document.querySelector('.atleta');
    
    // 3. Clona o template
    const clone = template.cloneNode(true);
    
    // 4. Atualiza o número do atleta
    const count = container.children.length + 1;
    clone.querySelector('h3').textContent = `Atleta ${count}`;
    
    // 5. Limpa os valores dos campos clonados
    clone.querySelectorAll('input').forEach(input => {
        input.value = '';
        // Aplica a máscara de data nos novos campos
        if (input.name === 'birth_dates[]') {
            aplicarMascaraData(input);
        }
    });
    clone.querySelector('select').selectedIndex = 0;
    
    // 6. Adiciona o novo atleta ao container
    container.appendChild(clone);
});

// Função para aplicar máscara de data
function aplicarMascaraData(input) {
    input.addEventListener('input', function(e) {
        // 1. Remove caracteres não numéricos
        let value = e.target.value.replace(/[^0-9]/g, '');
        
        // 2. Aplica a máscara DD/MM/AAAA
        if (value.length > 2) value = value.slice(0, 2) + '/' + value.slice(2);
        if (value.length > 5) value = value.slice(0, 5) + '/' + value.slice(5, 9);
        
        // 3. Limita o comprimento máximo
        e.target.value = value.slice(0, 10);
    });
}

// Aplica a máscara de data a todos os campos existentes
document.querySelectorAll('input[name="birth_dates[]"]').forEach(aplicarMascaraData);

// Função para validar o formulário antes do envio
document.querySelector('form').addEventListener('submit', function(event) {
    // 1. Seleciona todos os campos de data
    const dates = document.querySelectorAll('input[name="birth_dates[]"]');
    
    // 2. Verifica cada campo de data
    for (let date of dates) {
        const value = date.value.trim();
        
        // 3. Valida o formato DD/MM/AAAA
        if (!/^\d{2}\/\d{2}\/\d{4}$/.test(value)) {
            alert(`Data inválida: ${value}. Use o formato DD/MM/AAAA.`);
            event.preventDefault(); // Impede o envio do formulário
            return;
        }
    }
    
    // 4. Se tudo estiver certo, o formulário é enviado
    alert('Formulário enviado com sucesso!');
});