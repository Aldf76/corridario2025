document.addEventListener('DOMContentLoaded', function () {
  let athleteCount = 1;
  const addButton = document.getElementById('add-athlete');
  const form = document.querySelector('form');

  function cloneAthleteFields() {
      const originalAthlete = document.querySelector('.atleta');
      const newAthlete = originalAthlete.cloneNode(true);
      athleteCount++;

      // Atualiza o título e IDs
      newAthlete.querySelector('h3').textContent = `Atleta ${athleteCount}`;
      newAthlete.querySelectorAll('input, select').forEach(input => {
          const newId = input.id + '_' + athleteCount;
          input.id = newId;
          input.name = input.name.replace('[]', `_${athleteCount}[]`);
      });

      // Adiciona botão "Remover"
      const removeButton = document.createElement('button');
      removeButton.type = 'button';
      removeButton.textContent = 'Remover Atleta';
      removeButton.onclick = () => newAthlete.remove();
      newAthlete.appendChild(removeButton);

      // Insere antes do botão "Adicionar Atleta"
      addButton.parentNode.insertBefore(newAthlete, addButton);
  }

  addButton.addEventListener('click', cloneAthleteFields);

  // Validação básica
  form.addEventListener('submit', function (event) {
      let isValid = true;
      document.querySelectorAll('input[required], select[required]').forEach(input => {
          if (!input.value.trim()) {
              isValid = false;
              input.style.borderColor = 'red';
          } else {
              input.style.borderColor = '#ccc';
          }
      });

      if (!isValid) {
          event.preventDefault();
          alert('Preencha todos os campos obrigatórios!');
      }
  });
});