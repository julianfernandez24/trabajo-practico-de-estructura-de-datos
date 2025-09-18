#Clase Carpeta
class Carpeta:
 #Carpeta que contiene mensajes (implementada con lista)
    def __init__(self, nombre:str):
        self.__nombre = nombre
        self.__mensaje = list[mnsaje] = []
  @propery
  def nombre(self) - str:
      return self_.nombre
        

 def agregar_mensaje(self, mensaje:Mensaje):
    self.__mensaje.append(mensaje)

def eliminar_mensaje_por_id(self, msg_id:int) - bool:
    for i; m in enumerate(self._mensajes):
    if m.id == msg_id:
       def self._mensajes[i]
        return True
      return False

def listar_mensajes(self) -> List[Mensaje]:
        return list(self._mensajes) # retorno copia para evitar modificación externa

    def buscar_por_asunto(self, term: str) -> List[Mensaje]:
        term_low = term.lower()
        return [m for m in self._mensajes if term_low in m.asunto.lower()]

    def __len__(self):
        return len(self._mensajes)

    def __repr__(self):
        return f"<Carpeta '{self._nombre}' mensajes={len(self._mensajes)}>"

class Mensaje:
    """Modelo de un mensaje de correo."""
    _next_id = 1

    def __init__(self, remitente: str, destinatario: str, asunto: str, cuerpo: str, fecha: Optional[datetime]=None):
        self._id = Mensaje._next_id
        Mensaje._next_id += 1

        self._remitente = remitente
        self._destinatario = destinatario
        self._asunto = asunto
        self._cuerpo = cuerpo
        self._fecha = fecha or datetime.now()
        self._leido = False

    # propiedades de solo lectura
    @property
    def id(self) -> int:
        return self._id

    @property
    def remitente(self) -> str:
        return self._remitente

    @property
    def destinatario(self) -> str:
        return self._destinatario

    @property
    def asunto(self) -> str:
        return self._asunto

    @property
    def cuerpo(self) -> str:
        return self._cuerpo

    @property
    def fecha(self) -> datetime:
        return self._fecha

    @property
    def leido(self) -> bool:
        return self._leido

    # --- Métodos ---
    def marcar_leido(self):
        self._leido = True

    def resumen(self, max_len: int = 60) -> str:
        texto = f"[{self._id}] {self._asunto} - de {self._remitente} ({self._fecha.strftime('%Y-%m-%d %H:%M')})"
        return texto if len(texto) <= max_len else texto[:max_len-3] + "..."

    def __repr__(self):
        return f"<Mensaje id={self._id} from={self._remitente} to={self._destinatario} asunto='{self._asunto}'>"

       


class Usuario:
    """Modelo de usuario con carpetas básicas (INBOX, Enviados, Borradores, Papelera)."""
    def __init__(self, nombre: str, email: str):
        self._nombre = nombre
        self._email = email.lower()
        # carpetas indexadas por nombre
        self._carpetas: Dict[str, Carpeta] = {
            "INBOX": Carpeta("INBOX"),
            "Enviados": Carpeta("Enviados"),
            "Borradores": Carpeta("Borradores"),
            "Papelera": Carpeta("Papelera"),
        }

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def email(self) -> str:
        return self._email

    def crear_carpeta(self, nombre: str):
        if nombre in self._carpetas:
            raise ValueError(f"Carpeta '{nombre}' ya existe.")
        self._carpetas[nombre] = Carpeta(nombre)

    def recibir_mensaje(self, mensaje: Mensaje):
        """Recibe un mensaje y lo guarda en INBOX."""
        self._carpetas["INBOX"].agregar_mensaje(mensaje)

    def almacenar_en_enviados(self, mensaje: Mensaje):
        self._carpetas["Enviados"].agregar_mensaje(mensaje)

    def listar_carpetas(self) -> List[str]:
        return list(self._carpetas.keys())

    def listar_mensajes_carpeta(self, nombre_carpeta: str) -> List[Mensaje]:
        carpeta = self._carpetas.get(nombre_carpeta)
        if not carpeta:
            raise ValueError(f"Carpeta '{nombre_carpeta}' no existe para el usuario {self._email}.")
        return carpeta.listar_mensajes()

    def mover_mensaje(self, origen: str, destino: str, msg_id: int) -> bool:
        """Mover un mensaje entre carpetas (simple: busca y mueve)."""
        carp_origen = self._carpetas.get(origen)
        carp_destino = self._carpetas.get(destino)
        if not carp_origen or not carp_destino:
            raise ValueError("Carpeta origen o destino no existe.")
        for i, m in enumerate(carp_origen._mensajes):
            if m.id == msg_id:
                carp_destino.agregar_mensaje(m)
                del carp_origen._mensajes[i]
                return True
        return False

    def enviar(self, destinatario_email: str, asunto: str, cuerpo: str, servidor: "ServidorCorreo") -> bool:
        """Interfaz de usuario para enviar; delega en ServidorCorreo."""
        return servidor.enviar_mensaje(self._email, destinatario_email, asunto, cuerpo)

    def __repr__(self):
        return f"<Usuario {self._nombre} ({self._email})>"

class ServidorCorreo:
    """Servidor simple que registra usuarios y enruta mensajes localmente."""
    def __init__(self):
        # Mapeo email -> Usuario para búsquedas
        self._usuarios: Dict[str, Usuario] = {}

    def registrar_usuario(self, usuario: Usuario):
        email = usuario.email
        if email in self._usuarios:
            raise ValueError(f"Usuario con email '{email}' ya registrado.")
        self._usuarios[email] = usuario

    def registrar_usuarios_desde_lista(self, lista: List[tuple]):
        """
        Recibe lista de tuplas (nombre, email) y registra usuarios.
        Esto sigue la idea de tu compañero: crear usuarios desde una lista.
        """
        for nombre, email in lista:
            u = Usuario(nombre, email)
            try:
                self.registrar_usuario(u)
            except ValueError:
                
                pass

    def buscar_usuario(self, email: str) -> Optional[Usuario]:
        return self._usuarios.get(email.lower())

    def autenticar(self, email: str) -> Optional[Usuario]:
        """Simulación simplificada de 'login' (devuelve Usuario si existe)."""
        return self.buscar_usuario(email)

    def enviar_mensaje(self, remitente_email: str, destinatario_email: str, asunto: str, cuerpo: str) -> bool:
        remitente = self.buscar_usuario(remitente_email)
        destinatario = self.buscar_usuario(destinatario_email)
        if remitente is None:
            raise ValueError(f"Remitente '{remitente_email}' no registrado en el servidor.")
        if destinatario is None:
            
            raise ValueError(f"Destinatario '{destinatario_email}' no registrado en el servidor.")

        msg = Mensaje(remitente=remitente.email, destinatario=destinatario.email, asunto=asunto, cuerpo=cuerpo)
       
        destinatario.recibir_mensaje(msg)
        
        remitente.almacenar_en_enviados(msg)
        return True

    def listar_usuarios(self) -> List[str]:
        return list(self._usuarios.keys())

    def __repr__(self):
        return f"<ServidorCorreo usuarios={len(self._usuarios)}>"


# ejemplo de uso

if __name__ == "__main__":
    servidor = ServidorCorreo()

    # crear usuarios desde una lista
    lista_de_usuarios = [
        ("Alice", "alice@unal.edu.ar"),
        ("Bob", "bob@unal.edu.ar"),
        ("Carol", "carol@unal.edu.ar"),
    ]
    servidor.registrar_usuarios_desde_lista(lista_de_usuarios)

    # autenticar 
    alice = servidor.autenticar("alice@unal.edu.ar")
    bob = servidor.autenticar("bob@unal.edu.ar")

    print("Usuarios registrados:", servidor.listar_usuarios())

    # Alice envía un mensaje a Bob
    if alice and bob:
        alice.enviar("bob@unal.edu.ar", "Prueba Entrega1", "Hola Bob, este es un mensaje de prueba.", servidor)

    # Listar INBOX de Bob
    inbox_bob = bob.listar_mensajes_carpeta("INBOX")
    print(f"\nINBOX de {bob.email}: ({len(inbox_bob)} mensajes)")
    for m in inbox_bob:
        print(" -", m.resumen())

    # Listar Enviados de Alice
    enviados_alice = alice.listar_mensajes_carpeta("Enviados")
    print(f"\nEnviados de {alice.email}: ({len(enviados_alice)} mensajes)")
    for m in enviados_alice:
        print(" -", m.resumen())
Respuesta de IA

    



        
    























