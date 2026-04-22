import libvirt
import sys
import logging
from pyghmi.ipmi.events import EventLog 

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - BMC_SIM_PYGHMI - %(levelname)s - %(message)s',
    filename='bmc_operations.log'
)

class BMC_Simulator:
    def __init__(self, vm_name):
        self.vm_name = vm_name
        self.uri = "qemu:///system"
        self.conn = self._connect()
        self.event_log = EventLog()

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
                logging.info("IPMI Query: Power State ON")
            else:
                print("Chassis Power is off")
                logging.info("IPMI Query: Power State OFF")

    def power_on(self):
        dom = self._get_domain()
        if dom:
            try:
                dom.create()
                print(f"IPMI Command: [Chassis Control On] sent to {self.vm_name}")
                logging.info("IPMI Action: Power ON sequence initiated")
            except libvirt.libvirtError as e:
                print(f"Error: {e}")

    def power_off(self):
        dom = self._get_domain()
        if dom:
            try:
                dom.destroy()
                print(f"IPMI Command: [Chassis Control Off] sent to {self.vm_name}")
                logging.info("IPMI Action: Power OFF (Immediate/Forced)")
            except libvirt.libvirtError as e:
                print(f"Error: {e}")

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
