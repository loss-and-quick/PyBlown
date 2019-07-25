#verion 0.9
import pymem
import pymem.process
import re
import time
from threading import Thread
class Offsets():
    m_iTeamNum = 0xF4
    dwEntityList = 0x4D05B14
    pm = pymem.Pymem("csgo.exe")
    clRender = 0x70
    client = pymem.process.module_from_name(pm.process_handle, "client_panorama.dll")
    dwGlowObjectManager = (0x5245F60)
    m_iGlowIndex = (0xA40C)
    dwLocalPlayer = 0xCF3A3C
def error():
    print(pymem.logger)
def radar():
    clientModule = Offsets.pm.read_bytes(Offsets.client.lpBaseOfDll, Offsets.client.SizeOfImage)
    address = Offsets.client.lpBaseOfDll + re.search(rb'\x80\xB9.{5}\x74\x12\x8B\x41\x08', clientModule).start() + 6

    Offsets.pm.write_char(address, chr(0 if ord(Offsets.pm.read_char(address)) else 1))
def main():
    print("Py project has launched.")
    print("Made this cheat:Minicx")
    Thread(target=glow_esp()).start()
    Thread(target=Chams_esp()).start()
    Thread(target=radar()).start()

def glow_esp():
    while True:
        glow_manager = Offsets.pm.read_int(Offsets.client.lpBaseOfDll + Offsets.dwGlowObjectManager)

        for i in range(1, 32):  # Entities 1-32 are reserved for players.
            entity = Offsets.pm.read_int(Offsets.client.lpBaseOfDll + Offsets.dwEntityList + i * 0x10)

            if entity:
                entity_team_id = Offsets.pm.read_int(entity + Offsets.m_iTeamNum)
                entity_glow = Offsets.pm.read_int(entity + Offsets.m_iGlowIndex)
                entity_i = Offsets.pm.read_int(Offsets.client.lpBaseOfDll + Offsets.dwLocalPlayer)
                if entity_team_id != Offsets.pm.read_int(entity_i+Offsets.m_iTeamNum):
                    Offsets.pm.write_float(glow_manager + entity_glow * 0x38 + 0x4, float(255))   # R
                    Offsets.pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(1))   # G
                    Offsets.pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(1))   # B
                    Offsets.pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(1))  # Alpha
                    Offsets.pm.write_int(glow_manager + entity_glow * 0x38 + 0x24, 1)           # Enable glow
def Chams_esp():
    while True:
        for i in range(1, 32):
            entity = Offsets.pm.read_int(Offsets.client.lpBaseOfDll + Offsets.dwEntityList + i * 16)
            if entity:
                entity_team_id = Offsets.pm.read_int(entity + Offsets.m_iTeamNum)
                entity_i = Offsets.pm.read_int(Offsets.client.lpBaseOfDll + Offsets.dwLocalPlayer)
                if entity_team_id != Offsets.pm.read_int(entity_i+Offsets.m_iTeamNum):
                    Offsets.pm.write_int(entity + Offsets.clRender, 0)  # // Red
                    Offsets.pm.write_int(entity + Offsets.clRender + 1, 255)  # // Green
                    Offsets.pm.write_int(entity + Offsets.clRender + 2, 0)  # // Blue
                    Offsets.pm.write_int(entity + Offsets.clRender + 3, 0)  # // Alpha
while True:
    main()
time.sleep(4)
error()

