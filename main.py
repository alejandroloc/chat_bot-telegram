#!/usr/bin/env python
# pyright:reportUnusedVariable=false, reportGeneralTypeIssues=false
"""
Hit RUN to execute the program.

You can also deploy a stable, public version of your project, unaffected by the changes you make in the workspace.

This proof-of-concept Telegram bot takes a user's text messages and turns them into stylish images. Utilizing Python, the `python-telegram-bot` library, and PIL for image manipulation, it offers a quick and interactive way to generate content.

Read the README.md file for more information on how to get and deploy Telegram bots.
"""
import logging
from base_de_datos import imprimir_datos, imprimir_datos1234
from telegram import __version__ as TG_VER
from telegram._utils.types import ReplyMarkup

try:
  from telegram import __version_info__
except ImportError:
  __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
  raise RuntimeError(
      f"This example is not compatible with your current PTB version {TG_VER}.To view the"
      f"{TG_VER} version of this example,"
      f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html")

from base_de_datos import imprimir_datos
from telegram import Update, ForceReply, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackContext, CallbackQueryHandler
import os

my_bot_token = '7195493988:AAE1ouhp-4Gh2ib6nUnnUuiW3X-J35wQyy4'
# Base de datos ficticia de libros
libros = [{
    "titulo": "Algorithms: Sequential, Parallel, and Distributed",
    "autor": "BERMAN, Kenneth, PAUL, Jerome",
    "ubicacion": "Biblioteca FI \"Ing. Antonio Dovalí Jaime\"",
    "ejemplares": 5,
    "editorial": "Thomson",
    "año_publicacion": 2005
}, {
    "titulo": "Discrete mathematics with applications",
    "autor": "EPP, Susanna S.",
    "ubicacion": "Biblioteca \"Mtro. Enrique Rivero Borrell\"",
    "ejemplares": 5,
    "editorial": "Boston Brooks",
    "año_publicacion": 2011
}, {
    "titulo":
    "Matemática discreta y lógica: Una perspectiva desde la Ciencia de la Computación",
    "autor": "GRASSMANN, Winfried, TREMBLAY, Jean-paul",
    "ubicacion": "Biblioteca FI \"Ing. Antonio Dovalí Jaime\"",
    "ejemplares": 8,
    "editorial": "Madrid Prentice Hall",
    "año_publicacion": 2003
}, {
    "titulo": "Discrete Mathematics",
    "autor": "JOHNSONBAUGH, Richard",
    "ubicacion":
    "Biblioteca \"Ing. Antonio Dovalí Jaime\", Biblioteca \"Mtro. Enrique Rivero Borrell\", Biblioteca de Posgrado \"Dr. Enzo Levi”",
    "ejemplares": 26,
    "editorial": "London Pearson",
    "año_publicacion": 2008
}, {
    "titulo": "Discrete Mathematical Structures",
    "autor": "KOLMAN, Bernard",
    "ubicacion": "Biblioteca \"Mtro. Enrique Rivero Borrell\"",
    "ejemplares": 15,
    "editorial": "Pearson",
    "año_publicacion": 2008
}, {
    "titulo": "Elementos de matemáticas discretas",
    "autor": "KLIU, C. L.",
    "ubicacion": "Biblioteca de Posgrado \"Dr. Enzo Levi”",
    "ejemplares": 20,
    "editorial": "México McGraw-Hill",
    "año_publicacion": 1995
}, {
    "titulo": "Matemáticas discretas y sus aplicaciones",
    "autor": "ROSEN, Kenneth",
    "ubicacion": "Biblioteca de Posgrado \"Dr. Enzo Levi”",
    "ejemplares": 3,
    "editorial": "España Mc Graw Hill",
    "año_publicacion": 2004
}, {
    "titulo":
    "Matemáticas discretas con aplicación a las ciencias de la computación",
    "autor": "TREMBLAY, Jean-paul, MANOHAR, Ram, RANGEL, Raymundo (TRAD.)",
    "ubicacion": "Biblioteca \"Mtro. Enrique Rivero Borrell\"",
    "ejemplares": 30,
    "editorial": "México CECSA",
    "año_publicacion": 2000
}, {
    "titulo": "Matemáticas discretas con teoría de gráficas y combinatoria",
    "autor": "VEERARAJAN, T.",
    "ubicacion":
    "Biblioteca \"Mtro. Enrique Rivero Borrell\", Biblioteca \"Ing. Antonio Dovalí Jaime\"",
    "ejemplares": 15,
    "editorial": "México McGraw-Hill Interamericana",
    "año_publicacion": 2008
}]

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Definicion del handlers start. These usually take the two arguments update and
# context.
async def help_command(update: Update,
                       context: ContextTypes.DEFAULT_TYPE) -> None:
  """Send a message when the command /help is issued."""
  await update.message.reply_text(
      "¡Bienvenido! al reservo de libros de estructuras discretas. Puedes usar los siguientes comandos:\n"
      "/buscar_autor [nombre del autor] - Buscar libros por autor.\n"
      "/buscar_titulo [título del libro] - Buscar libros por título.\n"
      "/start - Iniciar el bot.\n"
      "/help - Mostrar esta ayuda.")


# Función start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  """Dar la bienvenida al usuario."""
  keyboard = InlineKeyboardMarkup([
      [InlineKeyboardButton(text="Libros Digitales", callback_data="digital")],
      [
          InlineKeyboardButton(text="Sitios/Páginas web", callback_data="web")
      ],
      [InlineKeyboardButton(text="Libros en Bibliotecas",
                            callback_data="fisico")]
  ])

  if update.message and update.effective_user is not None:
    user = update.effective_user
    await update.message.reply_html(
        rf"¡Hola {user.mention_html()}! Bienvenido a la biblioteca de Estructuras Discretas",
        reply_markup=ForceReply(selective=True))
    await update.message.reply_text(
        "Selecciona una opción:", reply_markup=keyboard)


#funcion que controla los botones
async def mostrar_teclado_libros_digitales(update):
  """Mostrar teclado para libros digitales"""
  keyboard = InlineKeyboardMarkup([
      [
          InlineKeyboardButton(
              text="A Guide to Graph Algorithms",
              url="https://link.springer.com/book/10.1007/978-981-16-6350-5")
      ],
      [
          InlineKeyboardButton(
              text="Elementos de matemáticas discretas",
              url=
              "https://gc.scalahed.com/recursos/files/r161r/w25470w/Elementosdematematicasdiscretas.pdf"
          )
      ],
      [
          InlineKeyboardButton(
              text="Elementary Methods of Graph Ramsey Theory",
              url=
              "https://drive.google.com/file/d/1b554QWn7FLWOpGWLVmILzw5hg4dFOpK5/view?usp=sharing"
          )
      ],
      [
          InlineKeyboardButton(
              text="Guide to Discrete Mathematics",
              url=
              "https://drive.google.com/file/d/1aZ20pHP57otlo3eMPPDdLQaJj0kuq2yo/view?usp=sharing"
          )
      ],
      [
          InlineKeyboardButton(
              text="Matemática Discreta.",
              url=
              "https://riuma.uma.es/xmlui/bitstream/handle/10630/25954/Discreta22.pdf?sequence=1"
          )
      ],
      [
          InlineKeyboardButton(
              text="Matemáticas Discretas",
              url=
              "https://catedras.facet.unt.edu.ar/lad/wp-content/uploads/sites/93/2018/04/Matem%C3%A1ticas-Discretas-6edi-Johnsonbaugh.pdf"
          )
      ],
      [
          InlineKeyboardButton(
              text="Matemáticas Discretas con Aplicaciones",
              url=
              "https://bibliotecavirtual8denovpinas.files.wordpress.com/2020/08/matematicas-discretas-con-aplicaciones-epp-4ta-edicion-2.pdf"
          )
      ],
      [
          InlineKeyboardButton(
              text="Notas de Matemáticas Discretas",
              url=
              "https://drive.google.com/file/d/1aCq3a57apKH7lNmoIx6sNpYjkd57vxye/view?usp=sharing"
          )
      ],
      [
          InlineKeyboardButton(
              text="Propedéutico: Matemáticas Discretas",
              url=
              "https://posgrados.inaoep.mx/archivos/PosCsComputacionales/Curso_Propedeutico/Matematicas_Discretas/Capitulo_4_Grafos.pdf"
          )
      ], [InlineKeyboardButton(text="Atrás", callback_data="atras")]
  ])
  await update.callback_query.message.edit_text("Selecciona el libro que deseas consultar:",
                                                reply_markup=keyboard)


# Función de imprimir
async def mostrar_teclado_libros_fisicos(update):
  """Mostrar teclado para libros físicos"""
  keyboard = InlineKeyboardMarkup(
      [[InlineKeyboardButton(text="Todos los temas", callback_data="todos")],
       [InlineKeyboardButton(text="Tema 1", callback_data="tema1")],
       [InlineKeyboardButton(text="Tema 2", callback_data="tema2")],
       [InlineKeyboardButton(text="Tema 3", callback_data="tema3")],
       [InlineKeyboardButton(text="Tema 4", callback_data="tema4")],
       [InlineKeyboardButton(text="Atrás", callback_data="atras")]])
  await update.callback_query.message.edit_text(
      "Selecciona una opción para ver los libros que se encuentran en la Facultad de Ingeniería:",
      reply_markup=keyboard)


async def mostrar_teclado_paginas_web(update):
  """Mostrar teclado para páginas web"""
  keyboard = InlineKeyboardMarkup([
      [
          InlineKeyboardButton(
              text="Conjuntos y Relaciones",
              url=
              "https://conjuntos-y-relaciones.blogspot.com/2017/10/conjuntos-y-relaciones.html"
          )
      ],
      [
          InlineKeyboardButton(
              text="Estructuras de matemática discreta para computación",
              url=
              "https://jcastrom.jimdofree.com/matematica/matem%C3%A1tica-discreta/"
          )
      ],
      [
          InlineKeyboardButton(
              text="Estructuras Discretas Aplicadas (Doerr y Levasseur)",
              url=
              "https://espanol.libretexts.org/Matematicas/Combinatoria_y_Matematicas_Discretas/Estructuras_Discretas_Aplicadas_(Doerr_y_Levasseur)"
          )
      ],
      [
          InlineKeyboardButton(
              text="Estructuras Discretas y Ciencias de la Computación",
              url=
              "https://docplayer.es/77030955-Estructuras-discretas-y-ciencias-de-la-computacion.html"
          )
      ],
      [
          InlineKeyboardButton(
              text="Grafos Conexos",
              url=
              "https://teoriadegrafos.blogspot.com/2007/03/grafos-conexos.html"
          )
      ],
      [
          InlineKeyboardButton(
              text="Grafos y Árboles",
              url=
              "https://clubmateparacompu.blogspot.com/2016/11/grafos-y-arboles.html"
          )
      ],
      [
          InlineKeyboardButton(
              text="Matemáticas Discretas",
              url=
              "https://eldiscretini.wordpress.com/aplicacion-de-arboles-y-redes/"
          )
      ],
      [
          InlineKeyboardButton(
              text="Teoría de Conjuntos",
              url="https://roa.cedia.edu.ec/webappscode/19/index.html")
      ],
      [
          InlineKeyboardButton(text="Teoría de Grafos",
                               url="https://rpubs.com/Yelky99/Tgrafos_pmai")
      ],
      [
          InlineKeyboardButton(
              text="Teoría de la Computabilidad",
              url=
              "https://academia-lab.com/enciclopedia/teoria-de-la-computabilidad/"
          )
      ],
      [InlineKeyboardButton(text="Atrás", callback_data="atras")]
  ])
  await update.callback_query.message.edit_text(
      "Selecciona la página que deseas visitar:", reply_markup=keyboard)


async def controlador_callback(update: Update, context: CallbackContext):
  """Controlar los callbacks"""
  opcion = update.callback_query.data
  if opcion == "digital":
    await update.callback_query.edit_message_text(
        "Seleccionaste libros digitales")
    await mostrar_teclado_libros_digitales(update)

  elif opcion == "fisico":
    await update.callback_query.edit_message_text(
        "Seleccionaste libros en bibliotecas")
    await mostrar_teclado_libros_fisicos(update)

  elif opcion == "web":
    await update.callback_query.edit_message_text("Seleccionaste sitios web")
    await mostrar_teclado_paginas_web(update)

  elif opcion == "todos":
    await imprimir_datos(update)
  elif opcion == "tema1":
    await imprimir_datos1234(update)
  elif opcion == "tema2":
    await imprimir_datos1234(update)
  elif opcion == "tema3":
    await imprimir_datos1234(update)
  elif opcion == "tema4":
    await imprimir_datos1234(update)

  elif opcion == "atras":
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton(text="Libros Digitales", callback_data="digital")],
         [
             InlineKeyboardButton(text="Sitios/Páginas web", callback_data="web")
         ],
         [InlineKeyboardButton(text="Libros en Bibliotecas",
                               callback_data="fisico")]])
    await update.callback_query.message.edit_text("Volver al menú principal:",
                                                  reply_markup=keyboard)


async def lista(titulo, apellido, nombre):
  lista = []
  lista.append({"titulo": titulo, "apellido": apellido, "nombre": nombre})
  for lista in lista:
    print(lista)


# Función para el comando /buscar_titulo
async def buscar_por_titulo(update: Update, context):
  # Verificar si se proporcionó el título después del comando
  if len(context.args) == 0:
    await update.message.reply_text(
        "Por favor, proporciona el título del libro después del comando.")
    return

  # Obtener el título proporcionado por el usuario
  titulo = ' '.join(context.args)

  # Inicializar una lista para almacenar los resultados de búsqueda
  resultados = []

  # Buscar libros que coincidan con el título proporcionado
  for libro in libros:
    if titulo.lower() in libro['titulo'].lower():
      resultados.append(libro)

  # Construir la respuesta
  if resultados:
    respuesta = "Resultados de búsqueda para el título '{}':\n\n".format(
        titulo)
    for libro in resultados:
      respuesta += f"Título: {libro['titulo']}\n"
      respuesta += f"Autor: {libro['autor']}\n"
      respuesta += f"Ubicación: {libro['ubicacion']}\n\n"
  else:
    respuesta = f"No se encontraron resultados para el título '{titulo}'."

  # Responder al usuario con los resultados
  await update.message.reply_text(respuesta)


# Función de busqueda
async def buscar_por_autor(update: Update, context):
  # Verificar si se proporcionó el nombre del autor después del comando
  if len(context.args) == 0:
    await update.message.reply_text(
        "Por favor, proporciona el nombre del autor después del comando.")
    return
  # Obtener el autor proporcionado por el usuario
  autor = ' '.join(context.args)
  # Inicializar una lista para almacenar los resultados de búsqueda
  resultados = []
  # Buscar libros que coincidan con el autor proporcionado
  for libro in libros:
    if autor.lower() in libro['autor'].lower():
      resultados.append(libro)
  # Construir la respuesta
  if resultados:
    respuesta = "Resultados de búsqueda para el autor '{}':\n\n".format(autor)
    for libro in resultados:
      respuesta += f"Título: {libro['titulo']}\n"
      respuesta += f"Autor: {libro['autor']}\n"
      respuesta += f"Ubicación: {libro['ubicacion']}\n\n"
  else:
    respuesta = f"No se encontraron resultados para el autor '{autor}'."
  # Responder al usuario con los resultados
  await update.message.reply_text(respuesta)


def main() -> None:
  """Bot en ejecucion"""

  # iniciacion de la aplicacion/bot con el token de telegram.
  application = ApplicationBuilder().token(my_bot_token).build()

  # Comandos del bot
  application.add_handler(CommandHandler("start", start))
  application.add_handler(CallbackQueryHandler(controlador_callback))
  # application.add_handler(CommandHandler("list", imprimir_libro))

  application.add_handler(CommandHandler("help", help_command))
  application.add_handler(CommandHandler("buscar_autor", buscar_por_autor))
  application.add_handler(CommandHandler("buscar_titulo", buscar_por_titulo))

  # on non command i.e message - echo the message on Telegram

  # Run the bot until the user presses Ctrl-C
  application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
  main()
