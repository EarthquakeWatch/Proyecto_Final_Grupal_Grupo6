# BOT TELEGRAM  
 
# Descripción 
 
En este proyecto, hemos creado un bot de Telegram que proporciona alertas de sismos, incluyendo su magnitud y localización. El bot es capaz de enviar actualizaciones periódicas sobre sismos a los usuarios que inicien una conversación con él. 
 
# Configuración inicial 
 
Lo primero que hicimos fue configurar el bot en la plataforma de Telegram. Le asignamos un nombre descriptivo, características relevantes y una foto representativa. 

# Caracteristicas  

- Alerta de sismos con su magnitud y localizacion 
- Información de peligrosidad 
- información de localización  
- Envío periódico de actualizaciones sobre sismos. 
 
# Requisitos 
 
- Python 3.x 
 
- Biblioteca python-telegram-bot  
  
# Uso 
 
1. Ejecuta el achivo bot-telegram.py para iniciar el bot  

2. Abre Telegram y busca AlertSismosBot  

3. Inicia la conversacion con el bot simplemente al dar inicio  

4. El bot enviara una alerta de sismo, que incluye su magnitud y su localizacion. La localizacion tambien cuenta con un mapa donde esta ocurriendo.  

5. Ademas, el bot enviará actualizaciones periódicas sobre sismos cada 3000 segundos.  
 
# Descripción del código 

1. Importación de bibliotecas: El código comienza importando las bibliotecas necesarias, como telegram y telegram.ext. Estas bibliotecas proporcionan funcionalidades para interactuar con la API de Telegram
 
2. Declaración de variables: Se inicia la variable chat_state, este es un diccionario utilizado para almacenar el estado de la conversación con cada usuario.
 
3. Funciones: A continuación, se definen varias funciones. La función start se ejecuta cuando un usuario envía el comando /start al bot. Esta función envía una alerta de sismos al usuario, configura un trabajo en el job_queue y llama a las funciones peligrosidad y localizacion para enviar información adicional.

La función send_sismo es el trabajo programado en el job_queue. Se encarga de enviar la alerta de sismo al usuario y llamar a las funciones peligrosidad y localizacion. 

4. Función principal: La función main es la entrada principal del programa. Inicializa el Updater con el token del bot de Telegram y configura los controladores de comandos. Luego, inicia la recepción de actualizaciones del bot y entra en un bucle de espera. 
 
5. Finalmente, el código verifica si se está ejecutando directamente y, en ese caso, llama a la función main.  
 
# Aclaracion 

En este proyecto, utilizamos un dataframe para extraer la información sobre los sismos. Actualmente, estamos almacenando los datos en un archivo CSV local, lo cual cumple con los requisitos de funcionamiento del bot. Sin embargo, a medida que obtengamos los fondos necesarios, tenemos previsto migrar a un entorno en la nube, como AWS, para trabajar con datos en tiempo real. 
La migración a un entorno en la nube nos permitirá acceder a una mayor cantidad de datos actualizados y procesarlos de manera más eficiente.

 
