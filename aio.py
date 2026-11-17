import cv2
import os
import time

# Configuración
CLASE_ACTUAL = "lata"  # Cambia esto a "botella" o "otros" según corresponda
URL_CAMARA = "http://192.168.4.1"
CARPETA = f"dataset_propio/{CLASE_ACTUAL}"

# Crear carpeta si no existe
os.makedirs(CARPETA, exist_ok=True)
contador = len(os.listdir(CARPETA)) + 1

print(f"--- Iniciando Sistema de Captura ---")
print(f"Guardando en la carpeta: '{CARPETA}/'")
print("Instrucciones en la ventana flotante:")
print(" - Presiona 'c' para CAPTURAR la foto")
print(" - Presiona 'q' para SALIR")

while True:
    # 1. Solicita la imagen a la cámara
    cap = cv2.VideoCapture(URL_CAMARA)
    ret, frame = cap.read()
    cap.release() # Cierra inmediatamente para no sobrecargar el servidor
    
    if not ret:
        print(" -> La cámara no respondió. Esperando...")
        cv2.waitKey(250)
        continue
        
    # 2. Genera la vista previa
    # Amplía el fotograma a 640x480 para facilitar el enfoque
    fotograma_ampliado = cv2.resize(frame, (640, 480))
    
    # Agrega un texto de ayuda sobre la imagen
    cv2.putText(fotograma_ampliado, f"Clase: {CLASE_ACTUAL} | Foto #{contador}", (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(fotograma_ampliado, "Presiona 'c' para Capturar | 'q' para Salir", (10, 460), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
    
    cv2.imshow("Preview ESP32-CAM", fotograma_ampliado)
    
    # 3. Espera la acción del teclado en la ventana (con pausa para no saturar la placa)
    tecla = cv2.waitKey(250) & 0xFF
    
    # Si presionas 'c', guarda la foto usando los píxeles originales
    if tecla == ord('c'):
        ruta_archivo = f"{CARPETA}/{CLASE_ACTUAL}_{contador:03d}_{int(time.time())}.jpg"
        cv2.imwrite(ruta_archivo, frame) # Guarda el 'frame' original sin textos ni redimensionamiento
        print(f" -> Guardada exitosamente: {ruta_archivo}")
        contador += 1
        
    # Si presionas 'q', cierra el programa
    elif tecla == ord('q'):
        break

# Limpieza final
cv2.destroyAllWindows()
print("Proceso finalizado.")