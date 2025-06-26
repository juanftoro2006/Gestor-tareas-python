document.addEventListener('DOMContentLoaded', () => {
  const taskList = document.getElementById('task-list');

  // Cargar tareas desde el backend
  fetch('http://127.0.0.1:8000/tareas')  // Ajusta la URL si usas otro puerto o dominio
    .then(response => response.json())
    .then(tareas => {
      if (tareas.length === 0) {
        taskList.innerHTML = '<p>No hay tareas disponibles.</p>';
        return;
      }

      tareas.forEach((tarea, index) => {
        const taskCard = document.createElement('div');
        taskCard.className = 'task-card';

        const completada = tarea.completada ? "✅ Completada" : "❌ Pendiente";

        taskCard.innerHTML = `
          <h3>${index + 1}. ${tarea.titulo}</h3>
          <p><strong>Descripción:</strong> ${tarea.descripcion}</p>
          <p><strong>Estado:</strong> ${completada}</p>
          <p><strong>Fecha Límite:</strong> ${tarea.fecha_limite}</p>
          <p><strong>Creada:</strong> ${tarea.creada_en}</p>
          <p><strong>Completada en:</strong> ${tarea.completada_en || "No completada"}</p>
        `;

        taskList.appendChild(taskCard);
      });
    })
    .catch(error => {
      console.error('❌ Error al cargar tareas:', error);
      taskList.innerHTML = '<p>Error al cargar las tareas.</p>';
    });
});
