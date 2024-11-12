const ruta = window.location.pathname;
const ruta_seleccionada = ruta.split("/")[2];

const protocolo = window.location.protocol === "https:" ? "wss" : "ws";

// Conexión con el WS Creado
const ws = new WebSocket(
  `${protocolo}://${window.location.host}/ws/chat/${ruta_seleccionada}/`
);
//

ws.onopen = (e) => {
  console.log("Conexión establecida");
};

ws.onclose = (e) => {
  console.log("Conexión cerrada");
};

ws.onerror = (e) => {
  console.log("Error en la conexión");
};

const boton = document.querySelector("#boton");
const texto = document.querySelector("#texto");

const mensajes = document.querySelector("#mensajes");

boton.addEventListener("click", () => {
  const mensaje = texto.value;

  let data = {
    type: "message",
    message: mensaje,
  };
  // Parse en python es equivalemte a JSON.stringify en JS
  // Loads en python es equivalente a JSON.parse en JS
  data = JSON.stringify(data);

  ws.send(data);

  texto.value = "";
});

function nuevo_mensaje(data) {
  mensajes.innerHTML += `
    <article class="message">
        <img src="https://i.blogs.es/d1e3df/tanjiro-kamado/840_560.jpeg" alt="Avatar de Ana" class="avatar">
        <div class="message-content">
            <div class="message-header">
                <span class="username">Ana</span>
                <span class="timestamp">${data.timestamp}</span>
            </div>
            <p class="text">${data.message}</p>
        </div>
    </article>
    `;
}

const alerta = document.querySelector("#alerta");

alerta.addEventListener("click", () => { 
    let mensaje = texto.value;
    let data = {
        type: "alert",
        message: mensaje,
    }
    data = JSON.stringify(data);
    texto.value = "";
    ws.send(data);
});

ws.onmessage = (e) => {
  const data = JSON.parse(e.data);
  console.log(data);
  if (data.type === "message") {
    nuevo_mensaje(data);
  }
  else if (data.type === "alert") {
    alert(data.message);
  }
};
