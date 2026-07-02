# ============================================================
# itachi_fighting_bot.py - ULTIMATE FIGHTING BOT 🔥
# pip install telethon aiohttp
# ============================================================

import asyncio
import json
import os
import random
import time
from datetime import datetime
from aiohttp import web
from telethon import TelegramClient, events, Button
from telethon.errors import FloodWaitError

# =====================================================================
# ⚙️ CONFIG
# =====================================================================
API_ID = 24923714
API_HASH = '040929ee690bdb53b36484e017310358'
BOT_TOKEN = '8881008854:AAFfKjo0SDsEGKdfAqQ6JHXGbxTUxTJaCUo'
OWNER_ID = 7862394625

SUDO_USERS = [OWNER_ID]
bot_status = "online"
raid_active = {}  # chat_id -> [target_ids]
raid_speed = {}
SPEED_CONFIG = {
    "r": 1.5,
    "rr": 0.5,
    "rrr": 0.2,
    "rrrr": 0.08,
    "rrrrr": 0.03
}
GROUPS_CACHE = []
muted_users = {}
BOT_USERNAME = ""
PORT = int(os.environ.get("PORT", 8080))

# RAID LINES
DEFAULT_RAID_LINES = [
    "TERI MAKI CHUT MADARCHODO {MENTION} HIZDA HAI HAI TUM MADARCHODO BOL DE YUTA TERA BAAP HAI",
    "AIR JORDEN KE JUTE SE TERI KI CHUT PR MAAR MAAR KE LAAL KR DUNGA {MENTION}",
    "MADARCHODO {MENTION} BAAP SE LADEGA APNE TERI MA KI CHUT KHA JAUNGA RAMDI",
    "TERI MAA KI CHHUT KA KHAA JAUNGA {MENTION} MADARCHODO RANDI KI AULAD",
    "{MENTION} TERI MAIYA KA BHOSDA MADARCHODO SASTI GB RAOD KI RANDI KI AULAD",
    "TERI MUMMY KI CHUT BSDK {MENTION} 🖕",
    "MADARCHOD {MENTION} TERI AUKAAT NAHI HAI BHAAG YAHAN SE 🤬",
    "BHADWE {MENTION} TERI MAA KI CHUT ITNA ATTITUDE KAHAN SE LAATA HAI 🖕",
    "SALE MADARCHOD {MENTION} TERI MA KI CHUT ME LUND DAAL KE NIKALUGA",
    "{MENTION} TERI BEHEN KI CHUT ME SSD BOOT KAR DUNGA",
    "{MENTION} TERI MAA KO TORRENT BANAKER SEED KAR DUNGA",
    "{MENTION} TERI BEHEN KA LUND OLX PE BECH DUNGA",
    "{MENTION} TERI MAA KI GAAND ME QR CODE CHIPKA DUNGA",
    "TERI MAKI CHUT {MENTION} RANDI ITACHI PAPA BOL KE THODI AUKAT BANA LE",
    "TERI MAA KI CHHUT KA KHAA JAUNGA {MENTION} MADARCHODO RANDI KI AULAD",
    "AIR JORDEN KE JUTE SE TERI KI CHUT PR MAAR MAAR KE LAAL KR DUNGA {MENTION}",
    "MADARCHODO BAAP SE LADEGA APNE {MENTION} TERI MA KI CHUT KHA JAUNGA",
    "{MENTION} TERI MAA KI CHUT ME MAINE APNA 12 INCH KA LUND GHUSAYA AUR USKO ITNA CHODA KI USKI CHUT SE KHUN AANE LAGA AUR WO CHILLANE LAGI KI BACHAAO BACHAAO LEKIN MAINE NAHI RUKA AUR USKI CHUT KO PHAD DIYA AUR USKE ANDAR APNA LUND GHUMATE RAHA JAB TAK USKI CHUT FATT KAR DO HO GAYI AUR WO BESHOOR HO GAYI TERI MAA RO RAHI THI AUR MAI HAS RAHA THA KYUKI MAI JAANTA THA KI TERI MAA RANDI HAI AUR RANDI KO CHODNA HI MERA KAAM HAI TU APNI MAA SE POOCH LE KITNA MAJA AAYA USKO CHODNE ME MAINE USKI CHUT ME APNA LUND GHUMATE WAQT USKI CHUT SE ITNA PAANI NIKLA KI POORA KAMRA BHAR GAYA AUR USKI CHUT KI SMELL ITNI AAYI KI SAB LOG BHAG GAYE LEKIN MAI RUKA AUR USKO CHODTA RAHA JAB TAK USKI CHUT ME DARD NAHI HUA AUR WO GIR GAYI TERI MAA RANDI HAI AUR RANDI HAMESHA CHUDTI HAI YEH SACH HAI JO TU MANE YA NA MAANE {MENTION}",

"{MENTION} TERI MAA KI CHUT ME MAINE GARAM LOHAA GHUSAYA AUR USKO JALA KAR RAKH KAR DIYA AUR USKI CHUT KI SMELL ITNI AAYI KI POORE MOHALLE ME BADBOO PHEL GAYI AUR SAB LOG BHAG GAYE LEKIN MAI RUKA AUR USKI CHUT KO JALATA RAHA JAB TAK USKI CHUT JAL KAR KALI NAHI HO GAYI AUR WO CHILLATI RAHI AUR MAI HASATA RAHA TERI MAA KI CHUT SE KUCH NAHI BAKI HAI AB WO SIRF EK KALI JALI HUI CHUT HAI JISE KOI DEKHNA BHI NAHI CHAHTA AUR TU AAPNI MAA KI CHUT KA DARJA LE JAA TERI MAA KI CHUT SE JAB MAINE APNA LUND NIKALA TO USKI CHUT SE KHUN AUR PAANI DONO NIKAL RAHE THE AUR WO BESHOOR HO CHUKI THI LEKIN MAI NE USKO AUR CHODA AUR USKI CHUT ME APNA LUND GHUMATE RAHA {MENTION}",

"{MENTION} TERI MAA NE JAB TUJHE JANAM DIYA THA TO USKI CHUT SE ITNA KHUN AAYA THA KI LAG RAHA THA KI KOI JANWAR PAIDA HUA HAI KYUKI TERI MAA NE JANWARO KE SAATH SO KAR TUUJHE PAIDA KIYA THA AUR TU AAPNE AAP KO INSAN SAMJHTA HAI TERI AUKAAT TO JANWAR KI BHI NAHI HAI TUU TO RANDI KI AULAD HAI JO SIRF DUSRO KA MUH DEKH KAR ZINDA HAI TERI MAA KO AGAR KOI CHODEGA TO WO PANNIE DEGI KYUKI WO RANDI HAI AUR RANDI KA KAAM HAI LOGO KA LUND CHUSNA AUR PAISA LENA {MENTION}",

"{MENTION} TERI BEHEN KI CHUT ME MAINE APNA LUND GHUSAYA AUR USKI CHUT KO ITNA CHODA KI USKI CHUT SE KHUN AANE LAGA AUR WO CHILLANE LAGI KI BHAI BACHAAO LEKIN MAINE NAHI RUKA AUR USKI CHUT KO PHAD DIYA AUR USKE ANDAR APNA LUND GHUMATE RAHA JAB TAK USKI CHUT FATT KAR DO HO GAYI AUR WO BESHOOR HO GAYI TERI BEHEN RANDI HAI AUR RANDI KO CHODNA MERA KAAM HAI TU APNI BEHEN SE POOCH LE USKO KITNA MAJA AAYA AUR USKI CHUT KA PAANI ITNA NIKLA KI POORA BED GILA HO GAYA AUR USKI CHUT SE DURGANDH ITNI AAYI KI SAB LOG BHAG GAYE {MENTION}",

"{MENTION} TERI MAA KI CHUT ME MAINE GAS PIPE DALI AUR USME AGAR LAGA KAR USKI CHUT KO JALA DIYA AUR WO CHILLATI RAHI AUR MAI HASATA RAHA KYUKI MAI JAANTA THA KI TERI MAA RANDI HAI AUR RANDI KO JALANA MERA KAAM HAI TERI MAA KI CHUT JAL GAYI AUR AB WO SIRF RAKH HAI KOI BHI USSE DEKHNA NAHI CHAHTA AUR TUU APNI MAA KA YEH HAAL DEKH AUR RONE LAG TERI MAA NE JAB TUUJHE PAIDA KIYA THA TO USKI CHUT SE ITNA BADA TATTA NIKLA THA KI LAG RAHA THA KI KOI BADA JANWAR PAIDA HUA HAI LEKIN TUU TO INSAN BHI NAHI BAN SAKA AUR RANDI KI AULAD HI REH GAYA {MENTION}",

"{MENTION} TERI BEHEN KI CHUT ME MAINE TEZAAB DAL DIYA AUR USKI CHUT PIGHAL GAYI AUR WO CHILLATI RAHI AUR MAI HASATA RAHA KYUKI MAI JAANTA THA KI TERI BEHEN RANDI HAI AUR RANDI KA KAAM HAI CHUDNA AUR JALNA TERI BEHEN KI CHUT AB SIRF TEZAAB HAI KOI BHI USKO DEKHNA NAHI CHAHTA AUR TU APNI BEHEN KA YEH HAAL DEKH AUR SOCHE KI KYA GALAT KIYA TUNE TERI BEHEN RANDI HAI AUR WO CHUDTI RAHEGI JAB TAK USKI CHUT HAI LEKIN AB USKI CHUT NAHI HAI TO WO KYA KAREGI RANDI BINA CHUT KE TADAP TI HAIN AUR PHIR BHEEK MANGTI HAIN {MENTION}",

"{MENTION} TERI MAA KI CHUT ME MAINE PHENOL DAL DIYA AUR USKI CHUT JAL KAR RAKH HO GAYI AUR USKI CHUT KI SMELL SE POORA MOHALLA BHAR GAYA AUR SAB LOG UNKI NAAK BAND KAR KE BHAG GAYE LEKIN MAI RUKA AUR USKO AUR JALATA RAHA JAB TAK USKI CHUT KI SMELL KHATAM NAHI HO GAYI TERI MAA AB RANDI NAHI REH GAYI KYUKI USKI CHUT HI NAHI HAI AUR BINA CHUT KE RANDI NAHI BAN SAKTI TU APNI MAA KO LE JA AUR BATA KI USKI CHUT KAHAN HAI TERI MAA NE RO RO KAR MUJHSE PRAY KIYA KI USE MAAF KAR DOON LEKIN MAI NE NAHI MAANA KYUKI MAI JAANTA THA KI YE RANDI HAMESHA CHUDTI HAI AUR CHUDTI RAHEGI {MENTION}",

"{MENTION} TERI BEHEN KI CHUT ME MAINE APNA BOOT GHUSAYA AUR USKI CHUT KO ITNA PHADAYA KI USKI CHUT SE KHUN AANE LAGA AUR WO BESHOOR HO GAYI AUR MAI HASATA RAHA KYUKI MAI JAANTA THA KI TERI BEHEN RANDI HAI AUR RANDI KO PHADNA MERA KAAM HAI TERI BEHEN AB APNI CHUT SE DAR GAYI HAI AUR KOI BHI USKO CHODEGA TO WO SAH NAYI PAYEGI KYUKI USKI CHUT PHAD DIY GAYI HAI AUR AB USME DARD HI DARD HAI TERI BEHEN RANDI HAI AUR RANDI HAMESHA CHUDTI HAI LEKIN AB WO CHUD BHI NAHI SAKTI KYUKI USKI CHUT PHAD DIY GAYI HAI TO AB WO KYA KAREGI RANDI BINA CHUT KE KUCH NAHI KAR SAKTI {MENTION}",
 
"{MENTION} TERI MAA KI CHUT ME MAINE APNA 12 INCH KA LUND GHUSAYA AUR USKO ITNA CHODA KI USKI CHUT SE KHUN AANE LAGA AUR WO CHILLANE LAGI KI BACHAAO BACHAAO LEKIN MAINE NAHI RUKA AUR USKI CHUT KO PHAD DIYA AUR USKE ANDAR APNA LUND GHUMATE RAHA JAB TAK USKI CHUT FATT KAR DO HO GAYI AUR WO BESHOOR HO GAYI TERI MAA RO RAHI THI AUR MAI HAS RAHA THA KYUKI MAI JAANTA THA KI TERI MAA RANDI HAI AUR RANDI KO CHODNA HI MERA KAAM HAI TU APNI MAA SE POOCH LE KITNA MAJA AAYA USKO CHODNE ME MAINE USKI CHUT ME APNA LUND GHUMATE WAQT USKI CHUT SE ITNA PAANI NIKLA KI POORA KAMRA BHAR GAYA AUR USKI CHUT KI SMELL ITNI AAYI KI SAB LOG BHAG GAYE LEKIN MAI RUKA AUR USKO CHODTA RAHA JAB TAK USKI CHUT ME DARD NAHI HUA AUR WO GIR GAYI TERI MAA RANDI HAI AUR RANDI HAMESHA CHUDTI HAI YEH SACH HAI JO TU MANE YA NA MAANE {MENTION}",

"{MENTION} TERI MAA KI CHUT ME MAINE GARAM LOHAA GHUSAYA AUR USKO JALA KAR RAKH KAR DIYA AUR USKI CHUT KI SMELL ITNI AAYI KI POORE MOHALLE ME BADBOO PHEL GAYI AUR SAB LOG BHAG GAYE LEKIN MAI RUKA AUR USKI CHUT KO JALATA RAHA JAB TAK USKI CHUT JAL KAR KALI NAHI HO GAYI AUR WO CHILLATI RAHI AUR MAI HASATA RAHA TERI MAA KI CHUT SE KUCH NAHI BAKI HAI AB WO SIRF EK KALI JALI HUI CHUT HAI JISE KOI DEKHNA BHI NAHI CHAHTA AUR TU AAPNI MAA KI CHUT KA DARJA LE JAA TERI MAA KI CHUT SE JAB MAINE APNA LUND NIKALA TO USKI CHUT SE KHUN AUR PAANI DONO NIKAL RAHE THE AUR WO BESHOOR HO CHUKI THI LEKIN MAI NE USKO AUR CHODA AUR USKI CHUT ME APNA LUND GHUMATE RAHA {MENTION}",

"{MENTION} TERI MAA NE JAB TUJHE JANAM DIYA THA TO USKI CHUT SE ITNA KHUN AAYA THA KI LAG RAHA THA KI KOI JANWAR PAIDA HUA HAI KYUKI TERI MAA NE JANWARO KE SAATH SO KAR TUUJHE PAIDA KIYA THA AUR TU AAPNE AAP KO INSAN SAMJHTA HAI TERI AUKAAT TO JANWAR KI BHI NAHI HAI TUU TO RANDI KI AULAD HAI JO SIRF DUSRO KA MUH DEKH KAR ZINDA HAI TERI MAA KO AGAR KOI CHODEGA TO WO PANNIE DEGI KYUKI WO RANDI HAI AUR RANDI KA KAAM HAI LOGO KA LUND CHUSNA AUR PAISA LENA {MENTION}",

"{MENTION} TERI BEHEN KI CHUT ME MAINE APNA LUND GHUSAYA AUR USKI CHUT KO ITNA CHODA KI USKI CHUT SE KHUN AANE LAGA AUR WO CHILLANE LAGI KI BHAI BACHAAO LEKIN MAINE NAHI RUKA AUR USKI CHUT KO PHAD DIYA AUR USKE ANDAR APNA LUND GHUMATE RAHA JAB TAK USKI CHUT FATT KAR DO HO GAYI AUR WO BESHOOR HO GAYI TERI BEHEN RANDI HAI AUR RANDI KO CHODNA MERA KAAM HAI TU APNI BEHEN SE POOCH LE USKO KITNA MAJA AAYA AUR USKI CHUT KA PAANI ITNA NIKLA KI POORA BED GILA HO GAYA AUR USKI CHUT SE DURGANDH ITNI AAYI KI SAB LOG BHAG GAYE {MENTION}",

"{MENTION} TERI MAA KI CHUT ME MAINE GAS PIPE DALI AUR USME AGAR LAGA KAR USKI CHUT KO JALA DIYA AUR WO CHILLATI RAHI AUR MAI HASATA RAHA KYUKI MAI JAANTA THA KI TERI MAA RANDI HAI AUR RANDI KO JALANA MERA KAAM HAI TERI MAA KI CHUT JAL GAYI AUR AB WO SIRF RAKH HAI KOI BHI USSE DEKHNA NAHI CHAHTA AUR TUU APNI MAA KA YEH HAAL DEKH AUR RONE LAG TERI MAA NE JAB TUUJHE PAIDA KIYA THA TO USKI CHUT SE ITNA BADA TATTA NIKLA THA KI LAG RAHA THA KI KOI BADA JANWAR PAIDA HUA HAI LEKIN TUU TO INSAN BHI NAHI BAN SAKA AUR RANDI KI AULAD HI REH GAYA {MENTION}",

"{MENTION} TERI BEHEN KI CHUT ME MAINE TEZAAB DAL DIYA AUR USKI CHUT PIGHAL GAYI AUR WO CHILLATI RAHI AUR MAI HASATA RAHA KYUKI MAI JAANTA THA KI TERI BEHEN RANDI HAI AUR RANDI KA KAAM HAI CHUDNA AUR JALNA TERI BEHEN KI CHUT AB SIRF TEZAAB HAI KOI BHI USKO DEKHNA NAHI CHAHTA AUR TU APNI BEHEN KA YEH HAAL DEKH AUR SOCHE KI KYA GALAT KIYA TUNE TERI BEHEN RANDI HAI AUR WO CHUDTI RAHEGI JAB TAK USKI CHUT HAI LEKIN AB USKI CHUT NAHI HAI TO WO KYA KAREGI RANDI BINA CHUT KE TADAP TI HAIN AUR PHIR BHEEK MANGTI HAIN {MENTION}",

"{MENTION} TERI MAA KI CHUT ME MAINE PHENOL DAL DIYA AUR USKI CHUT JAL KAR RAKH HO GAYI AUR USKI CHUT KI SMELL SE POORA MOHALLA BHAR GAYA AUR SAB LOG UNKI NAAK BAND KAR KE BHAG GAYE LEKIN MAI RUKA AUR USKO AUR JALATA RAHA JAB TAK USKI CHUT KI SMELL KHATAM NAHI HO GAYI TERI MAA AB RANDI NAHI REH GAYI KYUKI USKI CHUT HI NAHI HAI AUR BINA CHUT KE RANDI NAHI BAN SAKTI TU APNI MAA KO LE JA AUR BATA KI USKI CHUT KAHAN HAI TERI MAA NE RO RO KAR MUJHSE PRAY KIYA KI USE MAAF KAR DOON LEKIN MAI NE NAHI MAANA KYUKI MAI JAANTA THA KI YE RANDI HAMESHA CHUDTI HAI AUR CHUDTI RAHEGI {MENTION}",

"{MENTION} TERI BEHEN KI CHUT ME MAINE APNA BOOT GHUSAYA AUR USKI CHUT KO ITNA PHADAYA KI USKI CHUT SE KHUN AANE LAGA AUR WO BESHOOR HO GAYI AUR MAI HASATA RAHA KYUKI MAI JAANTA THA KI TERI BEHEN RANDI HAI AUR RANDI KO PHADNA MERA KAAM HAI TERI BEHEN AB APNI CHUT SE DAR GAYI HAI AUR KOI BHI USKO CHODEGA TO WO SAH NAYI PAYEGI KYUKI USKI CHUT PHAD DIY GAYI HAI AUR AB USME DARD HI DARD HAI TERI BEHEN RANDI HAI AUR RANDI HAMESHA CHUDTI HAI LEKIN AB WO CHUD BHI NAHI SAKTI KYUKI USKI CHUT PHAD DIY GAYI HAI TO AB WO KYA KAREGI RANDI BINA CHUT KE KUCH NAHI KAR SAKTI {MENTION}",
]

# Auto create files
for fname, fdata in [("raid_lines.json", DEFAULT_RAID_LINES), ("muted_users.json", {}), ("groups.json", [])]:
    if not os.path.exists(fname):
        with open(fname, "w") as f: json.dump(fdata, f, indent=4)

def read_json(path):
    try:
        with open(path) as f: return json.load(f)
    except: return {}

def write_json(path, data):
    with open(path, "w") as f: json.dump(data, f, indent=4)

raid_lines = read_json("raid_lines.json")
muted_users = read_json("muted_users.json")
GROUPS_CACHE = read_json("groups.json")

# =====================================================================
# 🤖 BOT INIT
# =====================================================================
bot = TelegramClient('itachi_fight_bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# =====================================================================
# 🌐 WEB SERVER
# =====================================================================
async def health_check(request):
    return web.Response(text="✅ FIGHTING BOT IS RUNNING!", status=200)

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', health_check)
    app.router.add_get('/health', health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', PORT)
    await site.start()
    print(f"🌐 Web server on port {PORT}")

# =====================================================================
# 🔐 HELPERS
# =====================================================================
async def is_auth(user_id):
    return user_id == OWNER_ID or user_id in SUDO_USERS

def get_mention(user):
    return f"[{user.first_name}](tg://user?id={user.id})"

async def resolve_target(event, args):
    if event.is_reply:
        rep = await event.get_reply_message()
        return rep.sender_id, rep.sender
    if args:
        try:
            target = args[0]
            if target.startswith("@"):
                u = await bot.get_entity(target)
                return u.id, u
            return int(target), await bot.get_entity(int(target))
        except:
            return None, None
    return None, None

def update_groups():
    global GROUPS_CACHE
    GROUPS_CACHE = read_json("groups.json")
    return GROUPS_CACHE

def save_groups():
    write_json("groups.json", GROUPS_CACHE)

# =====================================================================
# 🚀 ULTIMATE RAID ENGINE - MULTI TARGET + MAX SPEED
# =====================================================================
async def raid_worker(chat_id, target_id, mention, delay, raid_key):
    """Single worker for one target - runs until stopped"""
    while raid_active.get(raid_key, False):
        try:
            line = random.choice(raid_lines)
            msg = line.replace("{MENTION}", mention)
            await bot.send_message(chat_id, msg)
            await asyncio.sleep(delay)
        except FloodWaitError as e:
            await asyncio.sleep(e.seconds + 0.1)
        except:
            await asyncio.sleep(delay)

async def start_raid(event, cmd_type, target_ids_users):
    """Start raid with multiple targets simultaneously"""
    chat_id = event.chat_id
    delay = SPEED_CONFIG.get(cmd_type, 1.5)
    
    for target_id, target_user in target_ids_users:
        if target_id == OWNER_ID or target_id in SUDO_USERS:
            await event.reply(f"🛡️ {get_mention(target_user)} ko raid nahi kar sakta!")
            continue
        
        raid_key = f"{chat_id}_{target_id}"
        if raid_active.get(raid_key, False):
            await event.reply(f"❌ {get_mention(target_user)} pe already raid hai!")
            continue
        
        mention = get_mention(target_user)
        raid_active[raid_key] = True
        raid_speed[raid_key] = delay
        
        # Har target ke liye 3 parallel workers
        for w in range(3):
            asyncio.create_task(raid_worker(chat_id, target_id, mention, delay, raid_key))
        
        await event.reply(f"⚔️ **RAID STARTED** on {mention}\n⚡ Speed: `{delay}s` x 3 workers\n🔥 Total targets: {len(target_ids_users)}")

# =====================================================================
# 🚫 MUTE CHECK
# =====================================================================
@bot.on(events.NewMessage(incoming=True))
async def mute_checker(event):
    if not event.sender_id: return
    if event.sender_id == OWNER_ID or event.sender_id in SUDO_USERS: return
    cid = str(event.chat_id)
    uid = event.sender_id
    if cid in muted_users and uid in muted_users[cid]:
        try:
            await asyncio.sleep(0.05)
            await event.delete()
        except: pass

# =====================================================================
# 📋 COMMAND HANDLER
# =====================================================================
@bot.on(events.NewMessage(pattern=r'^[\.\/\!]'))
async def command_handler(event):
    global bot_status, raid_active, raid_speed, SUDO_USERS, muted_users, BOT_USERNAME, GROUPS_CACHE
    
    text = event.text.strip()
    user = await event.get_sender()
    user_id = user.id
    chat_id = event.chat_id
    
    if not BOT_USERNAME:
        me = await bot.get_me()
        BOT_USERNAME = me.username
    
    cmd_full = text[1:].strip()
    parts = cmd_full.split()
    cmd = parts[0].lower() if parts else ""
    args = parts[1:] if len(parts) > 1 else []
    
    # ===== ALIVE =====
    if cmd == "alive":
        if not await is_auth(user_id):
            return
        bot_status = "online"
        me = await bot.get_me()
        update_groups()
        
        total_raids = len([k for k in raid_active.keys() if raid_active[k]])
        
        await event.reply(
            f"╔══════════════════════════╗\n"
            f"   🔥 **FIGHTING BOT** 🔥\n"
            f"╚══════════════════════════╝\n\n"
            f"🤖 **Bot:** @{me.username}\n"
            f"👑 **Owner:** `{OWNER_ID}`\n"
            f"⚔️ **Active Raids:** `{total_raids}`\n"
            f"📦 **Groups:** `{len(GROUPS_CACHE)}`\n"
            f"📜 **Lines:** `{len(raid_lines)}`\n"
            f"🔇 **Muted:** `{sum(len(v) for v in muted_users.values())}`\n\n"
            f"🚀 **ULTIMATE FAST - 3 WORKERS PER TARGET**\n"
            f"✅ **BOT READY!**"
        )
        return
    
    # ===== Auth check for rest =====
    if not await is_auth(user_id):
        return
    
    # ===== MENU =====
    if cmd in ["start", "menu"]:
        me = await bot.get_me()
        btns = [
            [Button.inline("⚔️ RAID COMMANDS", data="raid_cmds")],
            [Button.inline("🔫 SPAM COMMANDS", data="spam_cmds")],
            [Button.inline("🔧 OTHER COMMANDS", data="other_cmds")],
            [Button.url("➕ ADD TO GROUP", f"https://t.me/{me.username}?startgroup=true")],
        ]
        await event.reply(
            f"╔══════════════════════════╗\n"
            f"   🔥 **FIGHTING BOT** 🔥\n"
            f"╚══════════════════════════╝\n\n"
            f"👋 {get_mention(user)}!\n"
            f"⚡ **Status:** `{'🟢 ONLINE' if bot_status == 'online' else '🔴 OFFLINE'}`\n"
            f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            buttons=btns
        )
        return
    
    # ================================================================
    # ⚔️ RAID COMMANDS - 5 SPEED LEVELS
    # ================================================================
    
    # Multiple targets ko ek saath raid
    if cmd in ["r", "rr", "rrr", "rrrr", "rrrrr"]:
        targets = []
        
        # Get all targets from reply + args
        if event.is_reply:
            rep = await event.get_reply_message()
            targets.append((rep.sender_id, rep.sender))
        
        for arg in args:
            try:
                if arg.startswith("@"):
                    u = await bot.get_entity(arg)
                    targets.append((u.id, u))
                else:
                    u = await bot.get_entity(int(arg))
                    targets.append((u.id, u))
            except:
                pass
        
        if not targets:
            await event.reply(f"❌ Usage: `.{cmd} @user1 @user2` ya kisi pe reply karo")
            return
        
        await start_raid(event, cmd, targets)
        return
    
    # ================================================================
    # 🛑 STOP COMMANDS
    # ================================================================
    
    if cmd == "s":
        # Stop all raids in this chat
        stopped = 0
        keys_to_delete = [k for k in raid_active.keys() if k.startswith(f"{chat_id}_") and raid_active[k]]
        for key in keys_to_delete:
            raid_active[key] = False
            stopped += 1
        
        if stopped > 0:
            await event.reply(f"🛑 **{stopped} RAIDS STOPPED!**")
        else:
            await event.reply("❌ Koi raid active nahi hai!")
        return
    
    if cmd == "stop":
        # Stop specific user raid
        target_id, target_user = await resolve_target(event, args)
        if not target_id:
            # Stop ALL raids everywhere
            count = sum(1 for k in raid_active.keys() if raid_active[k])
            for k in raid_active:
                raid_active[k] = False
            await event.reply(f"🛑 **ALL {count} RAIDS STOPPED GLOBALLY!**")
            return
        
        raid_key = f"{chat_id}_{target_id}"
        if raid_active.get(raid_key, False):
            raid_active[raid_key] = False
            await event.reply(f"🛑 RAID STOPPED for {get_mention(target_user)}")
        else:
            await event.reply("❌ Is user pe koi raid nahi hai!")
        return
    
    # ================================================================
    # 🔫 SPAM COMMANDS
    # ================================================================
    
    if cmd == "spam":
        if len(args) < 2:
            await event.reply("❌ Usage: `.spam [count] [msg]`")
            return
        count = int(args[0]) if args[0].isdigit() else 5
        msg = " ".join(args[1:])
        if count > 100: count = 100
        
        m = await event.reply(f"⏳ Spamming `{count}` times...")
        for i in range(count):
            try:
                await bot.send_message(chat_id, msg)
                await asyncio.sleep(0.1)
            except FloodWaitError as e:
                await asyncio.sleep(e.seconds)
            except:
                pass
        await m.edit(f"✅ **Spam Done!** `{count}` messages!")
        return
    
    if cmd == "fspam":
        """Fast spam - no delay"""
        if len(args) < 2:
            await event.reply("❌ Usage: `.fspam [count] [msg]`")
            return
        count = int(args[0]) if args[0].isdigit() else 5
        msg = " ".join(args[1:])
        if count > 100: count = 100
        
        m = await event.reply(f"⏳ Fast spamming `{count}`...")
        for i in range(count):
            try:
                await bot.send_message(chat_id, msg)
            except FloodWaitError as e:
                await asyncio.sleep(e.seconds)
            except:
                pass
        await m.edit(f"✅ **Fast Spam Done!** `{count}` msgs!")
        return
    
    if cmd == "us":
        """Ultra spam - sends same msg to all groups"""
        if not args:
            await event.reply("❌ Usage: `.us [msg]`")
            return
        msg = " ".join(args)
        update_groups()
        m = await event.reply(f"⏳ Sending to {len(GROUPS_CACHE)} groups...")
        count = 0
        for gid in GROUPS_CACHE:
            try:
                await bot.send_message(gid, msg)
                count += 1
                await asyncio.sleep(0.2)
            except:
                pass
        await m.edit(f"✅ **{count}/{len(GROUPS_CACHE)} groups!**")
        return
    
    if cmd == "ts":
        """Tag spam - tag user with message in all groups"""
        if len(args) < 2:
            await event.reply("❌ Usage: `.ts @user [msg]`")
            return
        try:
            _, target_user = await resolve_target(event, [args[0]])
            u = target_user or await bot.get_entity(args[0])
            mention = get_mention(u)
            msg = " ".join(args[1:])
            update_groups()
            m = await event.reply(f"⏳ Tag spamming {len(GROUPS_CACHE)} groups...")
            count = 0
            for gid in GROUPS_CACHE:
                try:
                    await bot.send_message(gid, f"{mention}\n\n{msg}")
                    count += 1
                except:
                    pass
            await m.edit(f"✅ **{count}/{len(GROUPS_CACHE)} groups!**")
        except Exception as e:
            await event.reply(f"❌ Error: {e}")
        return
    
    # ================================================================
    # 🔧 OTHER COMMANDS
    # ================================================================
    
    if cmd == "off":
        bot_status = "offline"
        # Stop all raids
        for k in raid_active:
            raid_active[k] = False
        await event.reply("🔴 **BOT OFFLINE!** Sab raids band!")
        return
    
    if cmd == "ping":
        start = time.time()
        m = await event.reply("📡 Pinging...")
        end = time.time()
        ping = round((end-start)*1000, 2)
        await m.edit(f"⚡ **PONG!** `{ping}ms`")
        return
    
    if cmd == "id":
        await event.reply(f"👤 **Name:** {get_mention(user)}\n🆔 **ID:** `{user_id}`\n👑 **Owner:** {'✅' if user_id==OWNER_ID else '❌'}")
        return
    
    if cmd == "info":
        target_id, target_user = await resolve_target(event, args)
        if not target_id:
            await event.reply("❌ Usage: `.info @username`")
            return
        try:
            u = target_user or await bot.get_entity(target_id)
            await event.reply(f"👤 {get_mention(u)}\n🆔 `{u.id}`\n📛 @{u.username if u.username else 'N/A'}")
        except Exception as e:
            await event.reply(f"❌ Error: {e}")
        return
    
    if cmd == "addline":
        if not args:
            await event.reply("❌ Usage: `.addline Teri maa ki chut`")
            return
        line = " ".join(args)
        if "{MENTION}" not in line:
            line = "{MENTION} " + line
        raid_lines.append(line)
        write_json("raid_lines.json", raid_lines)
        await event.reply(f"✅ **Line Added!** Total: `{len(raid_lines)}`")
        return
    
    if cmd == "lines":
        text = ""
        for i, line in enumerate(raid_lines[:10], 1):
            display = line[:50] + "..." if len(line) > 50 else line
            text += f"`{i}.` {display}\n"
        if len(raid_lines) > 10:
            text += f"\n...aur `{len(raid_lines)-10}` lines"
        await event.reply(f"📜 **RAID LINES ({len(raid_lines)})**\n\n{text}")
        return
    
    if cmd == "mute":
        target_id, target_user = await resolve_target(event, args)
        if not target_id:
            await event.reply("❌ Usage: `.mute @username`")
            return
        if target_id == OWNER_ID or target_id in SUDO_USERS:
            await event.reply("🛡️ Cannot mute owner/sudo!")
            return
        cid = str(chat_id)
        if cid not in muted_users: muted_users[cid] = []
        if target_id not in muted_users[cid]:
            muted_users[cid].append(target_id)
            write_json("muted_users.json", muted_users)
            mention = get_mention(target_user or await bot.get_entity(target_id))
            await event.reply(f"🔇 **MUTED!** {mention}")
        else:
            await event.reply("❌ Already muted!")
        return
    
    if cmd == "unmute":
        target_id, _ = await resolve_target(event, args)
        if not target_id:
            await event.reply("❌ Usage: `.unmute @username`")
            return
        cid = str(chat_id)
        if cid in muted_users and target_id in muted_users[cid]:
            muted_users[cid].remove(target_id)
            if not muted_users[cid]: del muted_users[cid]
            write_json("muted_users.json", muted_users)
            await event.reply("✅ **UNMUTED!**")
        else:
            await event.reply("❌ Not muted!")
        return
    
    if cmd == "mutedlist":
        cid = str(chat_id)
        if cid in muted_users and muted_users[cid]:
            text = "🔇 **MUTED USERS**\n\n"
            for uid in muted_users[cid]:
                try:
                    u = await bot.get_entity(uid)
                    text += f"• {get_mention(u)} - `{uid}`\n"
                except:
                    text += f"• `{uid}`\n"
            await event.reply(text)
        else:
            await event.reply("✅ Koi muted user nahi!")
        return
    
    if cmd == "sudo":
        if user_id != OWNER_ID:
            await event.reply("❌ Sirf owner!")
            return
        target_id, target_user = await resolve_target(event, args)
        if not target_id:
            await event.reply("❌ Usage: `.sudo @username`")
            return
        if target_id in SUDO_USERS:
            await event.reply("❌ Already sudo!")
            return
        SUDO_USERS.append(target_id)
        await event.reply(f"🔑 **SUDO ADDED!**")
        return
    
    if cmd == "remsudo":
        if user_id != OWNER_ID:
            await event.reply("❌ Sirf owner!")
            return
        target_id, _ = await resolve_target(event, args)
        if not target_id:
            await event.reply("❌ Usage: `.remsudo @username`")
            return
        if target_id in SUDO_USERS:
            SUDO_USERS.remove(target_id)
            await event.reply("✅ Sudo removed!")
        else:
            await event.reply("❌ Not a sudo!")
        return
    
    if cmd == "sudolist":
        text = "🔐 **SUDO USERS**\n\n"
        for sid in SUDO_USERS:
            try:
                u = await bot.get_entity(sid)
                text += f"• {get_mention(u)} - `{sid}`\n"
            except:
                text += f"• `{sid}`\n"
        await event.reply(text)
        return
    
    if cmd == "raidstatus":
        total = sum(1 for k in raid_active.keys() if raid_active[k])
        text = f"⚔️ **RAID STATUS**\n\nActive Raids: `{total}`\n\n"
        for k, v in raid_active.items():
            if v:
                parts = k.split("_")
                text += f"• Chat `{parts[0]}` → User `{parts[1]}`\n"
        await event.reply(text)
        return
    
    if cmd == "botstats":
        update_groups()
        total_raids = sum(1 for k in raid_active.keys() if raid_active[k])
        await event.reply(
            f"📊 **BOT STATS**\n\n"
            f"🤖 Status: {'🟢' if bot_status=='online' else '🔴'}\n"
            f"⚔️ Active Raids: `{total_raids}`\n"
            f"📦 Groups: `{len(GROUPS_CACHE)}`\n"
            f"📜 Lines: `{len(raid_lines)}`\n"
            f"🔇 Muted: `{sum(len(v) for v in muted_users.values())}`\n"
            f"🔑 Sudo: `{len(SUDO_USERS)}`\n"
            f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        return
    
    if cmd == "gc":
        update_groups()
        text = f"📦 **GROUPS: {len(GROUPS_CACHE)}**\n\n"
        for i, gid in enumerate(GROUPS_CACHE[:15], 1):
            try:
                chat = await bot.get_entity(gid)
                text += f"`{i}.` {chat.title[:30]}\n"
            except:
                text += f"`{i}.` `{gid}`\n"
        if len(GROUPS_CACHE) > 15:
            text += f"\n...aur `{len(GROUPS_CACHE)-15}` groups"
        await event.reply(text)
        return
    
    if cmd == "restart":
        if user_id != OWNER_ID:
            await event.reply("❌ Sirf owner!")
            return
        await event.reply("🔄 **RESTARTING...**")
        os._exit(0)
    
    # ================================================================
    # 💀 PUNISH UNAUTHORIZED
    # ================================================================
    await punish_unauthorized(event)

async def punish_unauthorized(event):
    user = await event.get_sender()
    mention = get_mention(user)
    lines = [
        f"TERI MAKI CHUT {mention} RANDI ITACHI PAPA BOL KE THODI AUKAT BANA LE",
        f"MADARCHOD {mention} TERI AUKAAT NAHI HAI BOT USE KARNE KI",
        f"{mention} RANDI KI AULAD PEHLE SUDO LE FIR AA",
    ]
    for _ in range(3):
        try:
            await event.reply(random.choice(lines))
            await asyncio.sleep(0.8)
        except:
            pass

# =====================================================================
# 🔄 CALLBACK HANDLER
# =====================================================================
@bot.on(events.CallbackQuery)
async def callback_handler(event):
    data = event.data.decode()
    
    if data == "raid_cmds":
        await event.edit(
            "⚔️ **RAID COMMANDS**\n\n"
            "`.r @user` - Slow (1.5s)\n"
            "`.rr @user` - Medium (0.5s)\n"
            "`.rrr @user` - Fast (0.2s)\n"
            "`.rrrr @user` - Extreme (0.08s)\n"
            "`.rrrrr @user` - MAXIMUM (0.03s)\n\n"
            "Multiple targets: `.r @user1 @user2`\n\n"
            "`.s` - Stop all raids in this chat\n"
            "`.stop @user` - Stop specific user\n"
            "`.stop` - Stop ALL raids everywhere\n\n"
            "`.addline [text]` - Add raid line\n"
            "`.lines` - Show raid lines\n"
            "`.raidstatus` - Show active raids",
            buttons=[[Button.inline("⬅️ Back", data="main")]])
    
    elif data == "spam_cmds":
        await event.edit(
            "🔫 **SPAM COMMANDS**\n\n"
            "`.spam [count] [msg]` - Normal spam\n"
            "`.fspam [count] [msg]` - Fast spam (no delay)\n"
            "`.us [msg]` - Ultra spam (all groups)\n"
            "`.ts @user [msg]` - Tag spam (all groups)\n\n"
            "Max count: 100 per command",
            buttons=[[Button.inline("⬅️ Back", data="main")]])
    
    elif data == "other_cmds":
        await event.edit(
            "🔧 **OTHER COMMANDS**\n\n"
            "`.alive` - Bot status\n"
            "`.off` - Bot offline\n"
            "`.ping` - Ping check\n"
            "`.id` - Your info\n"
            "`.info @user` - User info\n"
            "`.mute @user` - Mute user\n"
            "`.unmute @user` - Unmute\n"
            "`.mutedlist` - Muted users\n"
            "`.sudo @user` - Add sudo\n"
            "`.remsudo @user` - Remove sudo\n"
            "`.sudolist` - Sudo list\n"
            "`.botstats` - Bot stats\n"
            "`.gc` - Group list\n"
            "`.restart` - Restart bot",
            buttons=[[Button.inline("⬅️ Back", data="main")]])
    
    elif data == "main":
        me = await bot.get_me()
        btns = [
            [Button.inline("⚔️ RAID COMMANDS", data="raid_cmds")],
            [Button.inline("🔫 SPAM COMMANDS", data="spam_cmds")],
            [Button.inline("🔧 OTHER COMMANDS", data="other_cmds")],
            [Button.url("➕ ADD TO GROUP", f"https://t.me/{me.username}?startgroup=true")],
        ]
        await event.edit(f"🔥 **FIGHTING BOT**\n\n⚡ {'🟢 ONLINE' if bot_status == 'online' else '🔴 OFFLINE'}\n⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", buttons=btns)

# =====================================================================
# 📦 AUTO GROUP TRACK
# =====================================================================
@bot.on(events.ChatAction)
async def chat_action(event):
    if event.user_added:
        me = await bot.get_me()
        for u in event.users:
            if u.id == me.id:
                cid = event.chat_id
                if cid not in GROUPS_CACHE:
                    GROUPS_CACHE.append(cid)
                    save_groups()
                await event.reply(f"🔥 **FIGHTING BOT ADDED!**\n👑 Owner: `{OWNER_ID}`\n📋 /menu")

# =====================================================================
# 🚀 MAIN
# =====================================================================
async def main():
    await start_web_server()
    me = await bot.get_me()
    print(f"🔥 FIGHTING BOT STARTED - @{me.username}")
    await bot.run_until_disconnected()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
