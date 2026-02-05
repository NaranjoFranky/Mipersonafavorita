import os
from flask import Flask, render_template_string, request
from datetime import datetime

app = Flask(__name__, static_folder="static")

FECHA_ESPECIAL = datetime(2025, 10, 20)

HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Juego Para Ti 💖</title>

<style>
* { box-sizing: border-box; }

body {
	margin: 0;
	font-family: 'Arial', sans-serif;
	background: linear-gradient(135deg, #ff758c, #ff7eb3);
	color: white;
	text-align: center;
	padding: 15px;
}

.card-box {
	background: rgba(0,0,0,0.35);
	padding: 20px;
	border-radius: 20px;
	max-width: 520px;
	margin: auto;
}

h2 { font-size: 1.6rem; }

button, input {
	width: 100%;
	padding: 14px;
	margin-top: 12px;
	border-radius: 12px;
	border: none;
	font-size: 1rem;
}

button {
	background: #ff4f81;
	color: white;
	cursor: pointer;
}

button:active { transform: scale(0.97); }

.grid {
	display: grid;
	grid-template-columns: repeat(auto-fit, minmax(70px, 1fr));
	gap: 12px;
	margin-top: 20px;
}

.card {
	aspect-ratio: 1/1.25;
	background: #ff4f81;
	border-radius: 14px;
	font-size: 1.4rem;
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	color: transparent;
	cursor: pointer;
	user-select: none;
}

.card span { font-size: 1.6rem; }

.card.open, .card.matched {
	background: white;
	color: #ff4f81;
}

.galeria {
	display: flex;
	gap: 8px;
	overflow-x: auto;
	margin-bottom: 15px;
}

.galeria img {
	height: 110px;
	border-radius: 14px;
	border: 2px solid white;
}

.mensaje-final { display: none; margin-top: 20px; }

audio { display: none; }

@media (min-width: 768px) {
	h2 { font-size: 2rem; }
	.galeria img { height: 140px; }
}
</style>
</head>

<body>

<audio id="musica" autoplay loop>
	<source src="/static/musica/musica.mp3" type="audio/mpeg">
</audio>

<button onclick="toggleMusic()">🎵 Música</button>

<div class="card-box">

<h2>💖 Un juego hecho para ti 💖</h2>

<div class="galeria">
	<img src="/static/1.jpg">
	<img src="/static/2.jpg">
	<img src="/static/3.jpg">
	<img src="/static/4.jpg">
	<img src="/static/5.jpg">
	<img src="/static/6.jpg">
	<img src="/static/7.jpg">
	
</div>

{% if not nombre %}
<form method="post">
	<p>Escribe tu nombre 💌</p>
	<input type="text" name="nombre" required>
	<button type="submit">Empezar</button>
</form>
{% else %}

<p>Hola <b>{{ nombre }}</b> 🥰</p>
<p>{{ mensaje_fecha }}</p>

<div class="grid" id="grid"></div>

<div class="mensaje-final" id="mensajeFinal">
	<h3 id="palabraFormada"></h3>
	<p>Cada letra es un recuerdo contigo 💕</p>
	<button onclick="reiniciar()">Jugar otra vez 🔁</button>
</div>

{% endif %}
</div>

{% if nombre %}
<script>
const adjetivos = ["AMOR","UNICO","HERMOSO","INCREIBLE","LINDO","MAGICO"];
const sustantivos = ["MI VIDA","MI TODO","CORAZON","ALMA","DESTINO"];
const emojis = ["❤️","💖","✨","🔥","🥰","💌"];

const palabras = [];
while (palabras.length < 1000) {
	const texto =
		adjetivos[Math.floor(Math.random()*adjetivos.length)] + " " +
		sustantivos[Math.floor(Math.random()*sustantivos.length)];
	const emoji = emojis[Math.floor(Math.random()*emojis.length)];
	palabras.push({texto, emoji});
}

let palabraActual="", emojiActual="", cartas=[], primera=null, bloqueo=false, aciertos=0;

function iniciarJuego() {
	grid.innerHTML="";
	mensajeFinal.style.display="none";
	primera=null; bloqueo=false; aciertos=0;

	const sel = palabras[Math.floor(Math.random()*palabras.length)];
	palabraActual = sel.texto;
	emojiActual = sel.emoji;

	cartas=[];
	palabraActual.replace(/ /g,"").split("").forEach(l=>{
		cartas.push({l,emojiActual});
		cartas.push({l,emojiActual});
	});

	cartas.sort(()=>0.5-Math.random());

	cartas.forEach(c=>{
		const d=document.createElement("div");
		d.className="card";
		d.dataset.l=c.l;
		d.innerHTML=`<span>${emojiActual}</span>${c.l}`;
		d.onclick=()=>clickCarta(d);
		grid.appendChild(d);
	});
}

function clickCarta(c){
	if(bloqueo||c.classList.contains("open"))return;
	c.classList.add("open");
	if(!primera){primera=c;}
	else{
		bloqueo=true;
		if(primera.dataset.l===c.dataset.l){
			primera.classList.add("matched");
			c.classList.add("matched");
			aciertos++;
			primera=null; bloqueo=false;
			if(aciertos===cartas.length/2) mostrarFinal();
		} else {
			setTimeout(()=>{
				primera.classList.remove("open");
				c.classList.remove("open");
				primera=null; bloqueo=false;
			},700);
		}
	}
}

function mostrarFinal(){
	palabraFormada.textContent = palabraActual + " " + emojiActual;
	mensajeFinal.style.display="block";
}

function reiniciar(){ iniciarJuego(); }

function toggleMusic(){
	const m=document.getElementById("musica");
	m.paused ? m.play() : m.pause();
}

iniciarJuego();
</script>
{% endif %}

</body>
</html>
"""

@app.route("/", methods=["GET","POST"])
def juego():
	nombre = request.form.get("nombre")
	hoy = datetime.now()

	if hoy.date() < FECHA_ESPECIAL.date():
		mensaje = "Cada dia nos acerca mas a algo bonito 💕"
	elif hoy.date() > FECHA_ESPECIAL.date():
		mensaje = "Algunas cosas pasan, pero lo que se siente de verdad nunca se va💖"
	else:
		mensaje = "Hoy es un dia muy especial para nosotros 💘"

	return render_template_string(HTML, nombre=nombre, mensaje_fecha=mensaje)

if __name__ == "__main__":
	import os
	port = int(os.environ.get("PORT", 10000))
	app.run(host="0.0.0.0", port=port)
