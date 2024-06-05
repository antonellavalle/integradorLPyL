// Realiza una solicitud HTTP GET para obtener las canciones en tendencia
fetch('/canciones_en_tendencia')
  .then(response => {
    // Verifica si la respuesta del servidor es exitosa
    if (!response.ok) {
      throw new Error('Hubo un problema al obtener las canciones.'); // Lanza un error si la respuesta no es exitosa
    }
    return response.json(); // Parsea la respuesta como JSON y la devuelve
  })
  .then(data => {
    // Manipula los datos recibidos
    console.log('Datos de canciones recibidos:', data); // Muestra los datos recibidos en la consola

    // Muestra las canciones en el DOM
    const listaCanciones = document.getElementById('lista-canciones'); // Obtiene el elemento <ul> donde se agregarán las canciones
    listaCanciones.innerHTML = ''; // Borra cualquier contenido previo de la lista

    data.canciones.forEach((cancion, index) => { // Itera sobre cada canción recibida
      const listItem = document.createElement('li'); // Crea un nuevo elemento <li> para cada canción
      listItem.className = 'cancion-pequeña m-1 ms-4 col-md-6 row align-items-center'; // Agrega las clases necesarias
      listItem.innerHTML = `
        <div class="col-1 h3">${index + 1}</div> <!-- Número de canción -->
        <div class="col d-flex">
          <img src="${cancion.imagen}" alt="${cancion.titulo}" class="cancion-pequeña-img rounded m-1"> <!-- Carátula de la canción -->
          <div class="ms-1">
            <div>${cancion.titulo}</div> <!-- Título de la canción -->
            <small>Artista: ${cancion.artista}</small> <!-- Artista de la canción -->
          </div>
        </div>
        <div class="col-2">${cancion.duracion} <i class="bi bi-play-fill"></i></div> <!-- Duración de la canción -->
      `;
      listaCanciones.appendChild(listItem); // Agrega el elemento <li> a la lista de canciones
    });
  })
  .catch(error => {
    console.error('Error al obtener las canciones:', error.message); // Maneja cualquier error que ocurra durante el proceso
  });

