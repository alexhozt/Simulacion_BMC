# Simulacion_BMC
Simulación de BMC para Gestión de Máquinas Virtuales

ste proyecto implementa un servicio de simulación de un **Controlador de Gestión de Servidor (BMC)**. Permite la administración remota de una máquina virtual (VM) mediante el protocolo **IPMI**, traduciendo comandos de red en acciones de **Libvirt**.

## Requisitos Técnicos
- [cite_start]**Hipervisor:** Libvirt (KVM/QEMU).
- [cite_start]**Interfaz de Cliente:** `ipmitool`.
- [cite_start]**Lenguaje:** Python 3 con librería `libvirt`.

## Componentes del Proyecto
- [cite_start]`bmc_control.py`: Script central que integra la lógica de IPMI con la API de Libvirt.
- [cite_start]`bmc_operations.log`: Registro histórico de las operaciones realizadas (Evidencia real).


## Guía de Uso

### 1. Configuración del Entorno
Asegúrese de tener instalado el soporte de virtualización y herramientas IPMI:
```bash
sudo apt install -y python3-libvirt ipmitool
```
### 2. Simulacion de Comandos IPMI
Para utilizar ipmitool como cliente, se utiliza un alias que conecta con el script BMC:
```
alias ipmitool-sim='python3 bmc_control.py'
```

### 3.Comandos Soportados
Para controlar la maquina virtual ejecute los siguientes comandos:

Consultar estado: ipmitool-sim status

Encender VM: ipmitool-sim on

Apagar VM (Forzado): ipmitool-sim off

### El sistema cumple con:

El sistema cumple con:

Integración con Libvirt: Control directo del estado de la VM.

Registro de Logs: Documentación automática de cada encendido y apagado en bmc_operations.log.

Interfaz Estándar: Uso de comandos basados en la sintaxis de ipmitool.
