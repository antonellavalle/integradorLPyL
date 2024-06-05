// Realiza una solicitud HTTP GET para obtener los nuevos lanzamientos
fetch('/nuevos_lanzamientos_en_arg')
  .then(response => {
    // Verifica si la respuesta del servidor es exitosa
    if (!response.ok) {
      throw new Error('Hubo un problema al obtener los nuevos lanzamientos.'); // Lanza un error si la respuesta no es exitosa
    }
    return response.json(); // Parsea la respuesta como JSON y la devuelve
  })
  .then(data => {
    // Manipula los datos recibidos
    console.log('Datos de nuevos lanzamientos recibidos:', data); // Muestra los datos recibidos en la consola

    // Muestra los nuevos lanzamientos en el DOM
    const listaLanzamientos = document.getElementById('lista-lanzamientos'); // Obtiene el elemento <ul> donde se agregarán los lanzamientos
    listaLanzamientos.innerHTML = ''; // Borra cualquier contenido previo de la lista

    data.lanzamientos.forEach((cancion, index) => { // Itera sobre cada lanzamiento recibido
      const listItem = document.createElement('li'); // Crea un nuevo elemento <li> para cada lanzamiento
      listItem.className = 'cancion-pequeña m-1 ms-4 col-md-6 row align-items-center'; // Agrega las clases necesarias
      listItem.innerHTML = `
        <div class="col-1 h3">${index + 1}</div> <!-- Número del lanzamiento -->
        <div class="col d-flex">
          <img src="${cancion.imagen}" alt="${cancion.imagen}" class="cancion-pequeña-img rounded m-1"> <!-- Carátula del lanzamiento -->
          <div class="ms-1">
            <div>${cancion.titulo}</div> <!-- Título del lanzamiento -->
            <small>Artista: ${cancion.artista}</small> <!-- Artista del lanzamiento -->
          </div>
        </div>
        <div class="col-2">${cancion.duracion} <i class="bi bi-play-fill"></i></div> <!-- Duración del lanzamiento -->
      `;
      listaLanzamientos.appendChild(listItem); // Agrega el elemento <li> a la lista de lanzamientos
    });
  })
  .catch(error => {
    console.error('Error al obtener los nuevos lanzamientos:', error.message); // Maneja cualquier error que ocurra durante el proceso
  });