# Codigo principal para control de  maquina virtual 
import libvirt
import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - BMC_SIM - %(levelname)s - %(message)s',
    filename='bmc_operations.log'
)

class BMC_Simulator:
    def __init__(self, vm_name):
        self.vm_name = vm_name
        self.uri = "qemu:///system"
        self.conn = self._connect()

    def _connect(self):
        try:
            return libvirt.open(self.uri)
        except libvirt.libvirtError as e:
            logging.error(f"Error de conexión a libvirt: {e}")
            sys.exit(1)

    def _get_domain(self):
        try:
            return self.conn.lookupByName(self.vm_name)
        except libvirt.libvirtError:
            logging.error(f"La VM '{self.vm_name}' no existe.")
            return None

    def status(self):
        dom = self._get_domain()
        if dom:
            state, _ = dom.state()
            if state == libvirt.VIR_DOMAIN_RUNNING:
                print("Chassis Power is on")
                logging.info("Estado consultado: ON")
            else:
                print("Chassis Power is off")
                logging.info("Estado consultado: OFF")

    def power_on(self):
        dom = self._get_domain()
        if dom:
            try:
                dom.create()
                print(f"Comando IPMI: Power ON enviado a {self.vm_name}")
                logging.info("Operación: Encendido exitoso")
            except libvirt.libvirtError as e:
                print(f"Fallo al encender: {e}")

    def power_off(self):
        dom = self._get_domain()
        if dom:
            try:
                dom.destroy()
                print(f"Comando IPMI: Power OFF (forced) enviado a {self.vm_name}")
                logging.info("Operación: Apagado exitoso")
            except libvirt.libvirtError as e:
                print(f"Fallo al apagar: {e}")

if __name__ == "__main__":
    bmc = BMC_Simulator("rocky9")

    if len(sys.argv) < 2:
        print("Uso: python3 bmc_control.py [status|on|off]")
        sys.exit(1)

    cmd = sys.argv[1].lower()
    if cmd == "status": bmc.status()
    elif cmd == "on": bmc.power_on()
    elif cmd == "off": bmc.power_off()
    else: print("Comando no reconocido.")
