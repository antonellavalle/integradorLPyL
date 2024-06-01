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

    // Itera sobre cada canción y muestra su información en la consola
    data.canciones.forEach(cancion => {
      console.log('Título:', cancion.titulo);
      console.log('Artista:', cancion.artista);
      console.log('Álbum:', cancion.album);
      console.log('Imagen:', cancion.imagen);
      console.log('----------------------------------');
    });

    // Muestra las canciones en el DOM
    const listaCanciones = document.getElementById('lista-canciones'); // Obtiene el elemento <ul> donde se agregarán las canciones
    data.canciones.forEach(cancion => { // Itera sobre cada canción recibida
      const listItem = document.createElement('li'); // Crea un nuevo elemento <li> para cada canción
      listItem.innerHTML = `
        <img src="${cancion.imagen}" alt="${cancion.titulo}"> <!-- Agrega una imagen con la URL y el título de la canción como atributos -->
        <h2>${cancion.titulo}</h2> <!-- Agrega el título de la canción -->
        <p>Artista: ${cancion.artista}</p> <!-- Agrega el nombre del artista -->
        <p>Álbum: ${cancion.album}</p> <!-- Agrega el nombre del álbum -->
      `;
      listaCanciones.appendChild(listItem); // Agrega el elemento <li> a la lista de canciones
    });
  })
  .catch(error => {
    console.error('Error al obtener las canciones:', error.message); // Maneja cualquier error que ocurra durante el proceso
  });