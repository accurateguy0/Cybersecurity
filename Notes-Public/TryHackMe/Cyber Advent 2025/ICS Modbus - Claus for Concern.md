The snow falls heavily over Wareville as chaos erupts at TBFC headquarters. What should be the busiest shipping day of the season has turned into a disaster.

**"Another chocolate egg?!"** shouts a frustrated warehouse worker, holding up yet another Easter-themed package.**"We're supposed to be shipping Christmas presents!"**

The delivery drones buzz overhead, their mechanical hums sounding almost... mocking. Each one returns from its route empty, having successfully delivered its cargo. But the cargo is all wrong.

You're called into the command centre, where screens flicker with delivery statistics. Everything looks normal on the surface—1,000 presents in stock, 98% success rate, and all systems are operational. But the phones won't stop ringing with confused citizens asking why they're receiving chocolate eggs instead of the toys and gifts they ordered.

The logistics manager pulls up a delivery manifest. **"Look at this",** she says, pointing at the screen.**"The system indicates that we delivered a teddy bear to the Miller family, but they received a chocolate bunny instead. It's the same weight, exact dimensions, but completely different items."**

Then, on one of the monitoring screens, a message flashes for just a second before disappearing:

🐰 EGGSPLOIT v6.66 - Property of HopSec Island 🐰  
"Why should Christmas have all the fun?" - King Malhare

Someone has compromised the drone fleet's control systems. The attack is sophisticated, falsifying sensor data, manipulating inventory selection, and erasing all traces. This isn't just a prank—it's a calculated assault on Christmas itself.

Your mission is clear: investigate the TBFC Drone Delivery System, uncover how King Malhare's Eggsploit team has compromised it, and restore Christmas deliveries before SOC-mas is ruined.

**But be warned:** King Malhare doesn't leave systems undefended. Traps are waiting for the careless investigator. One wrong move and you might make things much worse.

## A Mysterious Discovery

As you walk through the warehouse control room, something catches your eye—a crumpled piece of paper on the floor near the PLC terminal. It looks like someone dropped it in a hurry.

You pick it up and unfold it. The handwriting is hurried, almost frantic:

TBFC DRONE CONTROL - REGISTER MAP
(For maintenance use only)

HOLDING REGISTERS:
HR0: Package Type Selection
     0 = Christmas Gifts
     1 = Chocolate Eggs
     2 = Easter Baskets

HR1: Delivery Zone (1-9 normal, 10 = ocean dump!)

HR4: System Signature/Version
     Default: 100
     Current: ??? (check this!)

COILS (Boolean Flags):
C10: Inventory Verification
     True = System checks actual stock
     False = Blind operation

C11: Protection/Override
     True = Changes locked/monitored
     False = Normal operation

C12: Emergency Dump Protocol
     True = DUMP ALL INVENTORY
     False = Normal

C13: Audit Logging
     True = All changes logged
     False = No logging

C14: Christmas Restored Flag
     (Auto-set when system correct)

C15: Self-Destruct Status
     (Auto-armed on breach)

CRITICAL: Never change HR0 while C11=True!
Will trigger countdown!

- Maintenance Tech, Dec 19
You stare at the note, confusion washing over you. _"Register map? Coils? What is all this?"_

The terminology is foreign—HR0, C11, "Modbus" scribbled in the margin. But something about it feels important, like a key you don't yet know how to use.

You pocket the note carefully. **"I'll figure out what this means later"**, you think. For now, you need to understand the systems you're dealing with.

_Little do you know, this crumpled note will be exactly what saves Christmas..._

## Learning Objectives

- How **SCADA (Supervisory Control and Data Acquisition)** systems monitor industrial processes
- What **PLCs (Programmable Logic Controllers)** do in automation
- How the **Modbus protocol** enables communication between industrial devices
- How to identify compromised system configurations in industrial systems
- Techniques for safely remediating compromised control systems
- Understanding protection mechanisms and trap logic in ICS environments
## What is SCADA?

SCADA systems are the "command centres" of industrial operations. They act as the bridge between human operators and the machines doing the work. Think of SCADA as the nervous system of a factory—it senses what's happening, processes that information, and sends commands to make things happen.

TBFC uses a SCADA system to oversee its entire drone delivery operation. Without it, operators would have no way to monitor hundreds of drones, manage inventory, or ensure packages reach the right destinations. It's the invisible orchestrator of Christmas logistics.

## Components of a SCADA System

A SCADA system typically consists of four key components:

1. **Sensors & actuators:** These are the eyes and hands of the system. Sensors measure real-world conditions, such as temperature, pressure, position, and weight. Actuators perform physical actions—motors turn, valves open, robotic arms move.
2. **PLCs (Programmable Logic Controllers):** These are the brains that execute automation logic. They read sensor data, make decisions based on programmed rules, and send commands to actuators
3. **Monitoring systems:** Visual interfaces like CCTV cameras, dashboards, and alarm panels where operators observe physical processes.
4. **Historians:** Databases that store operational data for later analysis.
## Why SCADA Systems Are Targeted

Industrial control systems, such as SCADA, have become increasingly attractive targets for cybercriminals and nation-state actors. Here's why:

- They often run **legacy software** with known vulnerabilities. Many SCADA systems were installed decades ago and never updated. Security patches that exist for modern software don't exist for these ageing systems.
- **Default credentials** are commonly left unchanged. Administrators prioritise keeping systems running over changing passwords. In industrial environments, the mentality is often "if it works, don't touch it"—a recipe for security disasters.
- They're designed for **reliability, not security**. Most SCADA systems were built before cyber security was a significant concern. They were intended for closed networks that were presumed safe. Authentication, encryption, and access controls were afterthoughts at best.
- They control **physical processes**. Unlike attacking a website or stealing data, compromising SCADA systems has real-world consequences. Attackers can cause blackouts, contaminate water supplies, or—in our case—sabotage Christmas deliveries.
- They're often **connected to corporate networks**. The myth of "air-gapped" industrial systems is largely fiction. Most SCADA systems connect to business networks for reporting, remote management, and data integration. This connectivity provides attackers with entry points.
- Protocols like **Modbus lack authentication**. Many industrial protocols were designed for trusted environments. Anyone who can reach the Modbus port (502) can read and write values without proving their identity
## **What is a PLC?**

A PLC (Programmable Logic Controller) is an industrial computer designed to control machinery and processes in real-world environments. Unlike your laptop or smartphone, PLCs are purpose-built machines engineered for extreme reliability and harsh conditions.
PLCs are designed to:
- Survive harsh environments, like extreme temperatures, dust, moisture, constant vibrations and electromagnetic interference
- Run continuously 24/7, they operate for years, often without rebooting. Industries can't afford to restart.
- Executing control in real time, for example a package reaching the end of conveyor belt and PLC activating a robotic arm to catch it.
- Direct interface with physical hardware, like actuators and sensors

# Modbus
Modbus is a protocol for communication between industrial devices. Its popularity is due to its simplicity, but because of that there's no security in place.
## Modbus Data Types

Modbus organises data into four distinct types, each serving a specific purpose in industrial automation:

| Type                  | Purpose                    | Values  | Example Use Cases                                 |
| --------------------- | -------------------------- | ------- | ------------------------------------------------- |
| **Coils**             | Digital outputs (on/off)   | 0 or 1  | Motor running? Valve open? Alarm active?          |
| **Discrete Inputs**   | Digital inputs (on/off)    | 0 or 1  | Button pressed? Door closed? Sensor triggered?    |
| **Holding Registers** | Analogue outputs (numbers) | 0-65535 | Temperature setpoint, motor speed, zone selection |
| **Input Registers**   | Analogue inputs (numbers)  | 0-65535 | Current temperature, pressure reading, flow rate  |
The difference between input and output is that the input can be writable and output can be only readable.

In TBFC's drone control system, you'll find:

- **Holding Registers** storing configuration values:
    - HR0: Package type selection (0=Gifts, 1=Eggs, 2=Baskets)
    - HR1: Delivery zone (1-9 for normal zones, 10 for emergency disposal)
    - HR4: System signature (a version identifier or, in this case, an attacker's calling card)
- **Coils** controlling system behaviour:
    - C10: Inventory verification enabled/disabled
    - C11: Protection mechanism enabled/disabled
    - C12: Emergency dump protocol active/inactive
    - C13: Audit logging enabled/disabled
    - C14: Christmas restoration status flag
    - C15: Self-destruct mechanism armed/disarmed
# Modbus Addressing
In each data point in Modbus you have unique data points. To read or write a specific value you need to referenmce its address number. Modbus addresses start at 0.

In TBFC's drone control system, you'll find:

- **Holding Registers** storing configuration values:
    - HR0: Package type selection (0=Gifts, 1=Eggs, 2=Baskets)
    - HR1: Delivery zone (1-9 for normal zones, 10 for emergency disposal)
    - HR4: System signature (a version identifier or, in this case, an attacker's calling card)
- **Coils** controlling system behaviour:
    - C10: Inventory verification enabled/disabled
    - C11: Protection mechanism enabled/disabled
    - C12: Emergency dump protocol active/inactive
    - C13: Audit logging enabled/disabled
    - C14: Christmas restoration status flag
    - C15: Self-destruct mechanism armed/disarmed
Originally Modbus operated over serial connections using RS-232 or RS-485 cables. Now they use TCP Modbus protocol on port 408 to achieve the same thing with remote control, easier integration and centralised management. But these network systems also now is being exposed to network attacks.

nmap -sV -T4 -p- -vv 10.65.173.137

pip3 install pymodbus== 3.6.8

nano reconnaissance.py
Copy and paste the following code:

reconnaissance.py

```python
#!/usr/bin/env python3
from pymodbus.client import ModbusTcpClient

PLC_IP = "10.65.173.137"
PORT = 502
UNIT_ID = 1

# Connect to PLC
client = ModbusTcpClient(PLC_IP, port=PORT)

if not client.connect():
    print("Failed to connect to PLC")
    exit(1)

print("=" * 60)
print("TBFC Drone System - Reconnaissance Report")
print("=" * 60)
print()

# Read holding registers
print("HOLDING REGISTERS:")
print("-" * 60)

registers = client.read_holding_registers(address=0, count=5, slave=UNIT_ID)
if not registers.isError():
    hr0, hr1, hr2, hr3, hr4 = registers.registers
    
    print(f"HR0 (Package Type): {hr0}")
    print(f"  0=Christmas, 1=Eggs, 2=Baskets")
    print()
    
    print(f"HR1 (Delivery Zone): {hr1}")
    print(f"  1-9=Normal zones, 10=Ocean dump")
    print()
    
    print(f"HR4 (System Signature): {hr4}")
    if hr4 == 666:
        print(f"  WARNING: Eggsploit signature detected")
    print()

# Read coils
print("COILS (Boolean Flags):")
print("-" * 60)

coils = client.read_coils(address=10, count=6, slave=UNIT_ID)
if not coils.isError():
    c10, c11, c12, c13, c14, c15 = coils.bits[:6]
    
    print(f"C10 (Inventory Verification): {c10}")
    print(f"  Should be True")
    print()
    
    print(f"C11 (Protection/Override): {c11}")
    if c11:
        print(f"  ACTIVE - System monitoring for changes")
    print()
    
    print(f"C12 (Emergency Dump): {c12}")
    if c12:
        print(f"  CRITICAL: Dump protocol active")
    print()
    
    print(f"C13 (Audit Logging): {c13}")
    print(f"  Should be True")
    print()
    
    print(f"C14 (Christmas Restored): {c14}")
    print(f"  Auto-set when system is fixed")
    print()
    
    print(f"C15 (Self-Destruct Armed): {c15}")
    if c15:
        print(f"  DANGER: Countdown active")
    print()

print("=" * 60)
print("THREAT ASSESSMENT:")
print("=" * 60)

if hr4 == 666:
    print("Eggsploit framework detected")
if c11:
    print("Protection mechanism active - trap is set")
if hr0 == 1:
    print("Package type forced to eggs")
if not c10:
    print("Inventory verification disabled")
if not c13:
    print("Audit logging disabled")

print()
print("REMEDIATION REQUIRED")
print("=" * 60)

client.close()
```
nano restore_christmas.py
Enter the following code:

restore_christmas.py

```python
#!/usr/bin/env python3
from pymodbus.client import ModbusTcpClient
import time

PLC_IP = "10.65.173.137"
PORT = 502
UNIT_ID = 1

def read_coil(client, address):
    result = client.read_coils(address=address, count=1, slave=UNIT_ID)
    if not result.isError():
        return result.bits[0]
    return None

def read_register(client, address):
    result = client.read_holding_registers(address=address, count=1, slave=UNIT_ID)
    if not result.isError():
        return result.registers[0]
    return None

# Connect to PLC
client = ModbusTcpClient(PLC_IP, port=PORT)

if not client.connect():
    print("Failed to connect to PLC")
    exit(1)

print("=" * 60)
print("TBFC Drone System - Christmas Restoration")
print("=" * 60)
print()

# Step 1: Check current state
print("Step 1: Verifying current system state...")
time.sleep(1)

package_type = read_register(client, 0)
protection = read_coil(client, 11)
armed = read_coil(client, 15)

print(f"  Package Type: {package_type} (1 = Eggs)")
print(f"  Protection Active: {protection}")
print(f"  Self-Destruct Armed: {armed}")
print()

# Step 2: Disable protection
print("Step 2: Disabling protection mechanism...")
time.sleep(1)

result = client.write_coil(11, False, slave=UNIT_ID)
if not result.isError():
    print("  Protection DISABLED")
    print("  Safe to proceed with changes")
else:
    print("  FAILED to disable protection")
    client.close()
    exit(1)

print()
time.sleep(1)

# Step 3: Change package type to Christmas
print("Step 3: Setting package type to Christmas presents...")
time.sleep(1)

result = client.write_register(0, 0, slave=UNIT_ID)
if not result.isError():
    print("  Package type changed to: Christmas Presents")
else:
    print("  FAILED to change package type")

print()
time.sleep(1)

# Step 4: Enable inventory verification
print("Step 4: Enabling inventory verification...")
time.sleep(1)

result = client.write_coil(10, True, slave=UNIT_ID)
if not result.isError():
    print("  Inventory verification ENABLED")
else:
    print("  FAILED to enable verification")

print()
time.sleep(1)

# Step 5: Enable audit logging
print("Step 5: Enabling audit logging...")
time.sleep(1)

result = client.write_coil(13, True, slave=UNIT_ID)
if not result.isError():
    print("  Audit logging ENABLED")
    print("  Future changes will be logged")
else:
    print("  FAILED to enable logging")

print()
time.sleep(2)

# Step 6: Verify restoration
print("Step 6: Verifying system restoration...")
time.sleep(1)

christmas_restored = read_coil(client, 14)
new_package_type = read_register(client, 0)
emergency_dump = read_coil(client, 12)
self_destruct = read_coil(client, 15)

print(f"  Package Type: {new_package_type} (0 = Christmas)")
print(f"  Christmas Restored: {christmas_restored}")
print(f"  Emergency Dump: {emergency_dump}")
print(f"  Self-Destruct Armed: {self_destruct}")
print()

if christmas_restored and new_package_type == 0 and not emergency_dump and not self_destruct:
    print("=" * 60)
    print("SUCCESS - CHRISTMAS IS SAVED")
    print("=" * 60)
    print()
    print("Christmas deliveries have been restored")
    print("The drones will now deliver presents, not eggs")
    print("Check the CCTV feed to see the results")
    print()
    
    # Read the flag from registers
    flag_result = client.read_holding_registers(address=20, count=12, slave=UNIT_ID)
    if not flag_result.isError():
        flag_bytes = []
        for reg in flag_result.registers:
            flag_bytes.append(reg >> 8)
            flag_bytes.append(reg & 0xFF)
        flag = ''.join(chr(b) for b in flag_bytes if b != 0)
        print(f"Flag: {flag}")
    
    print()
    print("=" * 60)
else:
    print("Restoration incomplete - check system state")

client.close()
print()
print("Disconnected from PLC")
```