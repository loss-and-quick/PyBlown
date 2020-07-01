try:
    import wget
    import json
    import pymem.process
    import os
    import time
    import keyboard
    import threading
    import re
    import math
    import configparser
    import random
except:
    print("Error couldnt find modules.Downloading....")
    time.sleep(5)
    os.system('pip3 install wget pymem keyboard ')


class settings():
    glow = list()
    glowlegit = list()
    rankkey = str
    triggerkey = str
    triggerdelay = int
    trggerenable = 0


def createConfig():
    config = configparser.ConfigParser()
    config.add_section("Settings-Glow")
    config.set("Settings-Glow", "enable", '1')
    config.set("Settings-Glow", "r", '255')
    config.set("Settings-Glow", "g", '0')
    config.set("Settings-Glow", "b", '0')
    config.set("Settings-Glow", "alpha", "0.25")
    config.add_section("Settings-Glow legit")
    config.set("Settings-Glow legit", "enable", '0')
    config.set("Settings-Glow legit", "r", '255')
    config.set("Settings-Glow legit", "g", '0')
    config.set("Settings-Glow legit", "b", '0')
    config.set("Settings-Glow legit", "alpha", "0.25")
    config.add_section("Settings-Trigger")
    config.set("Settings-Trigger", "enable", '0')
    config.set("Settings-Trigger", "key", '0')
    config.set("Settings-Trigger", "delay", '0')
    config.add_section("Settings-Rank reaval")
    config.set("Settings-Rank reaval", 'key', 'insert')
    with open('config.cfg', "w") as config_file:
        config.write(config_file)


def readConfig():
    config = configparser.ConfigParser()
    config.read('config.cfg')
    settings.glow.append(float(config.get("Settings-Glow", "r")))
    settings.glow.append(float(config.get("Settings-Glow", "g")))
    settings.glow.append(float(config.get("Settings-Glow", "b")))
    settings.glow.append(float(config.get("Settings-Glow", "alpha")))
    settings.glow.append(int(config.get("Settings-Glow", "enable")))
    settings.trggerenable = int(config.get("Settings-Trigger", 'enable'))
    settings.triggerkey = str(config.get("Settings-Trigger", 'key'))
    settings.triggerdelay = int(config.get("Settings-Trigger", 'delay'))
    settings.rankkey = config.get("Settings-Rank reaval", 'key')


def radarhack():
    clientModule = pm.read_bytes(client.lpBaseOfDll, client.SizeOfImage)
    address = client.lpBaseOfDll + re.search(rb'\x80\xB9.{5}\x74\x12\x8B\x41\x08', clientModule).start() + 6
    pm.write_char(address, chr(0 if ord(pm.read_char(address)) else 1))


def moneyhack():
    clientModule = pm.read_bytes(client.lpBaseOfDll, client.SizeOfImage)
    address = client.lpBaseOfDll + re.search(rb'.\x0C\x5B\x5F\xB8\xFB\xFF\xFF\xFF',
                                             clientModule).start()
    pm.write_uchar(address, 0xEB if pm.read_uchar(address) == 0x75 else 0x75)


def glow():
    glow_manager = pm.read_int(client.lpBaseOfDll + dwGlowObjectManager)
    map = pm.read_string((pm.read_int(engine.lpBaseOfDll + dwClientState)) + dwClientState_Map)[0:2]

    for i in range(0, 32):
        entity = pm.read_int(client.lpBaseOfDll + dwEntityList + i * 0x10)
        if entity:
            entity_team_id = pm.read_int(entity + m_iTeamNum)
            entity_glow = pm.read_int(entity + m_iGlowIndex)
            entity_i = pm.read_int(client.lpBaseOfDll + dwLocalPlayer)

            if map == 'dz':
                if entity_team_id == pm.read_int(entity_i + m_iTeamNum):
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x4, float(settings.glow[0]))  # R
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(settings.glow[1]))  # G
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(settings.glow[2]))  # B
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(settings.glow[3]))  # Alpha
                    pm.write_int(glow_manager + entity_glow * 0x38 + 0x24, settings.glow[4])
                else:
                    pm.write_int(glow_manager + entity_glow * 0x38 + 0x24, 0)
            else:
                if entity_team_id != pm.read_int(entity_i + m_iTeamNum):
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x4,
                                   float(settings.glow[0]))  # R
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x8,
                                   float(settings.glow[1]))  # G
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0xC,
                                   float(settings.glow[2]))  # B
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x10,
                                   float(settings.glow[3]))  # Alpha
                    pm.write_int(glow_manager + entity_glow * 0x38 + 0x24, settings.glow[4])

                else:
                    pm.write_int(glow_manager + entity_glow * 0x38 + 0x24, 0)


def rankreaval():
    if keyboard.is_pressed(settings.rankkey):
        ranks = ["Unranked",
                 "Silver I",
                 "Silver II",
                 "Silver III",
                 "Silver IV",
                 "Silver Elite",
                 "Silver Elite Master",
                 "Gold Nova I",
                 "Gold Nova II",
                 "Gold Nova III",
                 "Gold Nova Master",
                 "Master Guardian I",
                 "Master Guardian II",
                 "Master Guardian Elite",
                 "Distinguished Master Guardian",
                 "Legendary Eagle",
                 "Legendary Eagle Master",
                 "Supreme Master First Class",
                 "The Global Elite"]
        print('\n' * 300)
        for i in range(0, 32):
            entity = pm.read_int(client.lpBaseOfDll + dwEntityList + i * 0x10)

            if entity:
                entity_team_id = pm.read_int(entity + m_iTeamNum)
                entity_i = pm.read_int(client.lpBaseOfDll + dwLocalPlayer)
                if entity_team_id != pm.read_int(entity_i + m_iTeamNum):
                    player_info = pm.read_int(
                        (pm.read_int(engine.lpBaseOfDll + dwClientState)) + dwClientState_PlayerInfo)
                    player_info_items = pm.read_int(pm.read_int(player_info + 0x40) + 0xC)
                    info = pm.read_int(player_info_items + 0x28 + (i * 0x34))
                    playerres = pm.read_int(client.lpBaseOfDll + dwPlayerResource)
                    rank = pm.read_int(playerres + m_iCompetitiveRanking + i * 4)

                    if pm.read_string(info + 0x10) != 'GOTV':
                        print(pm.read_string(info + 0x10), ranks[rank])

def resendpackers():
    time.sleep(0.1)
    pm.write_uchar(engine + dwbSendPackets, 1)
def bhop():
    if keyboard.is_pressed("space") or (keyboard.is_pressed("space") and keyboard.is_pressed("shift")):
        force_jump = client.lpBaseOfDll + dwForceJump
        player = pm.read_int(client.lpBaseOfDll + dwLocalPlayer)
        if player:
            on_ground = pm.read_int(player + m_fFlags)
        if on_ground and on_ground == 257:
            pm.write_int(force_jump, 5)
            time.sleep(0.08)
            pm.write_int(force_jump, 4)
    time.sleep(0.002)


def Trigger():
    player = pm.read_int(client.lpBaseOfDll + dwLocalPlayer)
    if player:
        flags = pm.read_int(player + m_fFlags)
        crossHairID = pm.read_int(player + m_iCrosshairId)
        if crossHairID != 0:
            crossEntity = pm.read_int(client.lpBaseOfDll + dwEntityList + ((crossHairID - 1) * 0x10))
            if crossEntity:
                crossEntityTeam = pm.read_int(crossEntity + m_iTeamNum)
                dormant = pm.read_int(crossEntity + m_bDormant)
                spotted = pm.read_int(crossEntity + m_bSpotted)
                if crossEntityTeam != pm.read_int(player + m_iTeamNum) and (dormant > 0 or spotted != 0):

                    speed = pm.read_float(player + m_vecVelocity)
                    time.sleep(settings.triggerdelay)
                    while crossHairID != 0 and flags & (1 << 0) and speed == 0:
                        crossHairID = pm.read_int(player + m_iCrosshairId)
                        pm.write_int(client.lpBaseOfDll + dwForceAttack, 5)
                        time.sleep(0.1)
                        pm.write_int(client.lpBaseOfDll + dwForceAttack, 4)


def get_sig(modname, pattern, extra=0, offset=0, relative=True):  # pasted
    module = pymem.process.module_from_name(pm.process_handle, modname)
    bytes = pm.read_bytes(module.lpBaseOfDll, module.SizeOfImage)
    match = re.search(pattern, bytes).start()
    non_relative = pm.read_int(module.lpBaseOfDll + match + offset) + extra
    yes_relative = pm.read_int(module.lpBaseOfDll + match + offset) + extra - module.lpBaseOfDll
    return "0x{:X}".format(yes_relative) if relative else "0x{:X}".format(non_relative)


if __name__ == "__main__":
    try:
        pm = pymem.Pymem("csgo.exe")
    except:
        print("u dont open csgo.exe")
        time.sleep(10)
        exit(1)

    ####
    # https://github.com/frk1/hazedumper/blob/master/csgo.json
    # https://github.com/guided-hacking/GH-Offset-Dumper/blob/master/config.json
    ###Signature
    dwForceAttack = int(get_sig('client.dll', rb'\x89\x0D....\x8B\x0D....\x8B\xF2\x8B\xC1\x83\xCE\x04', 0, 2), 0)
    dwGlowObjectManager = int(get_sig('client.dll', rb'\xA1....\xA8\x01\x75\x4B', 4, 1), 0)
    dwClientState = int(get_sig('engine.dll', rb'\xA1....\x33\xD2\x6A\x00\x6A\x00\x33\xC9\x89\xB0', 0, 1), 0)
    dwClientState_Map = int(get_sig('engine.dll', rb'\x05....\xC3\xCC\xCC\xCC\xCC\xCC\xCC\xCC\xA1', 0, 1, False), 0)
    dwEntityList = int(get_sig('client.dll', rb'\xBB....\x83\xFF\x01\x0F\x8C....\x3B\xF8', 0, 1), 0)
    dwLocalPlayer = int(
        get_sig('client.dll', rb'\x8D\x34\x85....\x89\x15....\x8B\x41\x08\x8B\x48\x04\x83\xF9\xFF', 4, 3), 0)
    dwClientState_PlayerInfo = int(get_sig('engine.dll', rb'\x8B\x89....\x85\xC9\x0F\x84....\x8B\x01', 0, 2, False), 0)
    dwPlayerResource = int(get_sig('client.dll', rb'\x8B\x3D....\x85\xFF\x0F\x84....\x81\xC7', 0, 2), 0)
    m_bDormant = int(get_sig('client.dll', rb'\x8A\x81....\xC3\x32\xC0', 8, 2, False), 0)
    dwForceJump = int(get_sig('client.dll', rb'\x8B\x0D....\x8B\xD6\x8B\xC1\x83\xCA\x02', 0, 2), 0)
    dwbSendPackets=int(get_sig('engine.dll',rb'\xB3\x01\x8B\x01\x8B\x40\x10\xFF\xD0\x84\xC0\x74\x0F\x80\xBF....\x0F\x84',1),0)
    ###
    ###NetVars
    m_iTeamNum = 244
    m_iGlowIndex = 42040
    m_iCompetitiveRanking = 6788
    m_fFlags = 260
    m_iCrosshairId = 46052
    m_bSpotted = 2365
    m_vecVelocity = 276
    ####i dont know hot to dump netvars using (https://github.com/guided-hacking/GH-Offset-Dumper/blob/master/config.json)

    client = pymem.process.module_from_name(pm.process_handle, "client.dll")
    engine = pymem.process.module_from_name(pm.process_handle, "engine.dll")

    print('\n' * 300)
    print('updating Offsets')
    # for bomjey
    # wget.download("https://raw.githubusercontent.com/frk1/hazedumper/master/csgo.json")
    # with open('csgo.json') as file:
    #    Offsets = json.load(file)
    # if os.path.exists(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'csgo.json')) == 1:
    #    os.remove(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'csgo.json'))
    # for i in Offsets["signatures"]:
    #    exec('%s = %d' % (i, Offsets["signatures"][i]))
    # for i in Offsets["netvars"]:
    #    exec('%s = %d' % (i, Offsets["netvars"][i]))
    # del (Offsets)
    print("done...Running cheat")
    miscstatus = False
    if os.path.exists('config.cfg'):
        readConfig()
    else:
        createConfig()
    while True:
        if pm.read_int(client.lpBaseOfDll + dwLocalPlayer):
            if miscstatus == False and pm.read_int(client.lpBaseOfDll + dwLocalPlayer):
                miscstatus = True
                radarhack()
                moneyhack()
                resendpackers()
            if not pm.read_int(client.lpBaseOfDll + dwLocalPlayer):
                miscstatus = False
            if settings.trggerenable == 1 and keyboard.is_pressed(settings.triggerkey):
                threading.Thread(target=Trigger())
            if settings.glow[4] == 1:
                threading.Thread(target=glow())
            threading.Thread(target=bhop())
            threading.Thread(target=rankreaval())
