from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# Configurar Selenium con Chrome
driver = webdriver.Chrome()
driver.get("aqui_va_la_url_para_logearse") #Cambiar la url

# Escribir usuario y contraseña
usuario = driver.find_element(By.NAME, "_username") #cambiar si es necesario por el nombre del campo Usuario
usuario.send_keys("nombre_usuario") #cambiar por el usuario

clave = driver.find_element(By.NAME, "_password") #cambiar si es necesario por la contraseña
clave.send_keys("contraseña" + Keys.ENTER) #cambiar la contraseña de ingreso

time.sleep(5)
# Ir a la página de creación de cuentas de email
driver.get("aqui_va_la_otra_dirección_que_accede_a_la_creación_de_los_usuarios") #cambiar la url de donde se va a mostrar el formulario de alta de usuarios

# Cargar archivo Excel
archivo_excel = "Users.xlsx" #este es el nombre del archivo donde está la lista completa de los usuarios y contraseñas
df = pd.read_excel(archivo_excel)

# Iterar sobre cada usuario en el Excel
for index, row in df.iterrows():
    nombre = row["Nombre"]
    password = row["Contraseña"]

    print(f"Cargando usuario: {nombre}")

    # Esperar a que la notificación desaparezca si existe
    try:
        WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.ID, "notifications"))) #ver si hay notificaiones y cambiar el ID
    except:
        pass  # Si la notificación no está, continuar

    # Abrir el modal de creación de cuenta
    boton_modal = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@title='Crear nueva cuenta de email (Alt + N )']")) #cambiar de ser necesario por el botón de crear usuario
    )
    boton_modal.click()

    # Esperar a que los campos del modal estén visibles
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "prefix"))) #cambiar el ID de la caja de texto de usuario

    # Rellenar el formulario
    campo_nombre = driver.find_element(By.ID, "prefix")
    campo_nombre.clear()
    campo_nombre.send_keys(nombre)

    campo_password = driver.find_element(By.ID, "fieldPass1") #cambiar el nombre de la caja de texto de la contraseña
    campo_password.clear()
    campo_password.send_keys(password)

    time.sleep(5)

    # Esperar y hacer clic en "Crear ahora"
    boton_crear = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Crear ahora']")) #cambiar el nombre del botón que puede tener ID, NAME ó solo el texto
    )
    boton_crear.click()

    # Esperar a que el proceso termine
    time.sleep(18)

# Cerrar el navegador
driver.quit()

print("Carga de usuarios completada.")
