from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
import psycopg2
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.properties import ListProperty
from kivy.uix.screenmanager import ScreenManager, Screen

class VirtesWindow(Screen, BoxLayout):
    datos_a_enviar = ListProperty(['','','',0,0])
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def consultar(self):
        """
        CONSULTARÁ LOS DATOS INGRESADOS PARA VERIFICAR LA 
        IDENTIDAD DE LA PERSONA QUE INTENTA ACCEDER A LA VOTACIÓN
        """
        sql=(f"""SELECT * FROM poblacion_capital_distrito WHERE dni = {int(self.datos_a_enviar[3])};""")
        conn = None
        try:
            conn = psycopg2.connect(
            host="localhost",
            port="5432",
            user="postgres",
            database="votosvir",
            password="zxmloop0198")

            with conn:
                with conn.cursor() as cur:
                    cur.execute(sql)
                    
                    if cur is not None:
                        fila = cur.fetchall()
                        self.fila1 = [fila[0][2],fila[0][3],fila[0][4],str(fila[0][0]),str(fila[0][1])]
                        if fila[0][6] != None:
                            print("Ya has votado")
                        elif fila[0][6] == None:
                            if self.fila1 != self.datos_a_enviar:
                                self.ids.frst_apellido.text= ''
                            else:
                                return True
            if conn is not None:
                conn.close()
        except (Exception, psycopg2.DatabaseError) as e:
            print(e)
        finally:
            if conn is not None:
                conn.close()
    
    def chng_preview(self, instance, identidad):
        """
        CAMBIARÁ LA VISTA PREVIA O VISUALIZACIÓN ESPEREADA DEL DNI
        DE LA PERSONA QUE INGRESA SUS DATOS
        """
        value=instance.text #contenido de la dirección(instance)

        # print(instance) es dirección de memoria
        # print(instance.text) es el contenido de la dirección
        # print(value) es el contenido, pero como variable
        # print(identidad) es el seg parámetro de la función

        try: 
            if identidad == 'primer_apellido':
                self.ids.frst_apellido.text = value.upper()
                self.datos_a_enviar[0] = value.upper()
            if identidad == "segundo_apellido":
                self.ids.scnd_apellido.text = value.upper()
                self.datos_a_enviar[1] = value.upper()
            if identidad == "nombres":
                self.ids.names.text = value.upper()
                self.datos_a_enviar[2] = value.upper()
            if identidad == "dni":
                self.ids.ind.text = value.upper()
                self.datos_a_enviar[3] = value.upper()
            if identidad == "cod_ver_dni":
                self.ids.dni_ver_cod.text = value.upper()
                self.datos_a_enviar[4] = value.upper()
        except:
            print("LOS DATOS NO FUERON INGRESADOS CORRECTAMENTE")
    
    def votar(self, voto):

        sql = (f"""UPDATE poblacion_capital_distrito SET voto = {int(voto)} WHERE dni = {int(self.datos_a_enviar[3])};""")
        conn = None

        try:
            conn = psycopg2.connect(
            host="localhost",
            port="5432",
            user="postgres",
            database="votosvir",
            password="zxmloop0198")
            with conn:
                with conn.cursor() as cur:
                    cur.execute(sql, (voto))
            if conn is not None:
                conn.close()

        except (Exception, psycopg2.DatabaseError) as e:
            print(e)

        finally:
            if conn is not None:
                conn.close()
class AnotherScreen(Screen):
    pass
class ScreenManagment(ScreenManager):
    pass

kv = Builder.load_file("PRUEBAS.kv")

class MainApp(App):
    def build(self):

        return kv

if __name__=='__main__':
    MainApp().run()