// Espera a que el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', () => {
  const taskList = document.getElementById('task-list');
  const form = document.getElementById('task-form');

  // ========================
  // 1. Cargar tareas existentes desde el backend
  // ========================
  fetch('http://127.0.0.1:8000/tareas')
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

        // Pintar tarea
        taskCard.innerHTML = `
          <h3>${index + 1}. ${tarea.titulo}</h3>
          <p><strong>Descripción:</strong> ${tarea.descripcion}</p>
          <p><strong>Estado:</strong> ${completada}</p>
          <p><strong>Fecha Límite:</strong> ${tarea.fecha_limite}</p>
          <p><strong>Creada:</strong> ${tarea.creada_en}</p>
          <p><strong>Completada en:</strong> ${tarea.completada_en || "No completada"}</p>
          <button class="btn-eliminar" data-id="${tarea.id}">❌ Eliminar</button>
        `;

        // ✅ Agregar evento al botón de eliminar
        const btnEliminar = taskCard.querySelector('.btn-eliminar');
        btnEliminar.addEventListener('click', () => {
          const id = btnEliminar.dataset.id;

          // Enviar DELETE al backend
          fetch(`http://127.0.0.1:8000/tareas/${id}`, {
            method: 'DELETE'
          })
            .then(res => {
              if (!res.ok) {
                throw new Error('No se pudo eliminar la tarea');
              }
              // Eliminar visualmente del DOM
              taskCard.remove();
            })
            .catch(error => {
              console.error('❌ Error al eliminar la tarea:', error);
              alert("Error al eliminar la tarea.");
            });
        });

        // Agregar la tarjeta de tarea al contenedor
        taskList.appendChild(taskCard);
      });
    })
    .catch(error => {
      console.error('❌ Error al cargar tareas:', error);
      taskList.innerHTML = '<p>Error al cargar las tareas.</p>';
    });

  // ========================
  // 2. Crear nueva tarea (enviar al backend)
  // ========================
  form.addEventListener('submit', (e) => {
    e.preventDefault(); // Evita que el formulario recargue la página

    const nuevaTarea = {
      titulo: document.getElementById('titulo').value,
      descripcion: document.getElementById('descripcion').value,
      fecha_limite: document.getElementById('fecha_limite').value
    };

    fetch('http://127.0.0.1:8000/tareas', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(nuevaTarea)
    })
      .then(res => {
        if (!res.ok) {
          throw new Error('No se pudo crear la tarea');
        }
        return res.json();
      })
      .then(() => {
        form.reset();         // Limpiar el formulario
        location.reload();    // Recargar para ver la nueva tarea
      })
      .catch(error => {
        console.error('❌ Error al crear tarea:', error);
        alert("No se pudo crear la tarea.");
      });
  });
});
