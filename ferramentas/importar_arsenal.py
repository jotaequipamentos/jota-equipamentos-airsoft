#!/usr/bin/env python3
"""Importa produtos da Arsenal Sports para a vitrine.

Uso:  python3 importar_arsenal.py
Lê as buscas e categorias em FONTES, baixa as miniaturas para img/, grava produtos.json
e atualiza o bloco de produtos dentro de index.html.
Produto sem preço na Arsenal ("Avise-me quando chegar") entra como indisponível.

Na vitrine cada produto tem: grupo (linha de categorias), cat (tipo de peça) e sub (modelo da arma, opcional).
"""
import html, io, json, os, re, sys, time, urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone, timedelta

AQUI = os.path.dirname(os.path.abspath(__file__))
BASE = "https://www.arsenalsports.com"

# Peças da AAP01: o tipo sai do nome da peça. A primeira regra que casar vence.
TIPOS_AAP = [
    ("Kits de conversão", r"CONVERSION KIT|RECEIVER KIT|UPPER KIT|KITS DE CONVERSAO|\bAP7\b|PCC|HANDGUARD|STOCK"),
    ("Magazines e HPA", r"MAGAZINE(?! RELEASE| CATCH)|\bHPA\b|MAG BASE|MAGAZINE LIP|\bLIP\b"),
    ("Gatilho, hammer e sear", r"TRIGGER|HAMMER|\bSEAR\b|DISCONNECTOR|KNOCKER"),
    ("Nozzle e blowback", r"NOZZ|BLOWBACK|\bBOLT\b(?! REL)|PISTON"),
    ("Hop-up, válvulas e vedação", r"HOP[\s-]?UP|BUCKING|VALVE|SEAL|GAS ROUTE|CHAMBER"),
    ("Canos, compensadores e silenciadores", r"COMPENSATOR|SILENCER|SUPPRESSOR|BARREL|TRACER|MUZZLE|THREAD"),
    ("Slides, ferrolhos e frames", r"UPPER RECEIVER|RECEIVER|FRAME|SLIDE(?! LOCK)|SIDE PANEL|SHELL"),
    ("Magwell, grip e apoio", r"MAGWELL|GRIP|THUMB|STOPPER|REST\b|BACKSTRAP"),
    ("Alavancas, travas e seletor", r"SELECTOR|CHARGING|COCKING|RELEASE|RELAEASE|LOCK|SAFETY|CHARGE RING|SWITCH|LEVER"),
    ("Molas, guias e pinos", r"SPRING|GUIDE ROD|GUIDE|\bPINS?\b|SCREW"),
    ("Miras, trilhos e montagens", r"RAIL|MOUNT|\bRMR\b|SIGHT|PICATINNY|GHOST RING|ADAPTER"),
    ("Outras peças", r"."),
]

# Canos internos: tipo pela plataforma, subdivisão pelo diâmetro.
TIPOS_CANO = [(n, None) for n in ("AEG", "Pistola e SMG", "Sniper", "GBBR e PTW", "Kits com cano externo",
                                   "Estabilizadores e espaçadores", "Outros canos")]
RX_SNIPER = r"VSR|L96|\bM24\b|\bM40|MB0\d|TYPE 96|MK 96|M700|PSG1|APM40|FIELDCRAFT|SNIPER|\bSRS\b|TAC41|AS01|STRIKER|\bLTR\b|BAR10|TYPE 89|SR25|DMR|T21"
RX_GBBR = r"GBBR|\bPTW\b|\bKSC\b|KWA M4|MASADA|PTS MEGA|AR-10|HK416"
RX_PISTOLA = r"\bGBB\b|\bAEP\b|PISTOL|\bG1[789]|\bG2[3-9]|G SERIES|GLOCK|HI-CAPA|MK23|1911|\bM9\b|DESERT EAGLE|M&P|PX-?4|MP7|\bACP\b|SR92|CZ-P09|VECTOR|P226|USP|SMG|JOHN WICK|\bM45\b"


def tipo_cano(x):
    n = x["nome"].upper()
    if re.search(r"STABILIZER|SPACER|\bIBS\b|\bBSU\b", n):
        return "Estabilizadores e espaçadores"
    if re.search(r"OUTER|OUTTER|SILENCER|GAS BLOCK", n):
        return "Kits com cano externo"
    if re.search(RX_SNIPER, n):
        return "Sniper"
    medidas = [float(m.replace(",", ".")) for m in re.findall(r"(\d{2,3}(?:[.,]\d)?)\s?MM\b", n)]
    comp = max([m for m in medidas if m >= 60], default=None)
    if re.search(r"\bAEG\b", n) and not re.search(r"GBBR|\bPTW\b", n):
        return "AEG"
    if re.search(RX_GBBR, n) or (re.search(r"\bGBB\b", n) and comp and comp >= 200):
        return "GBBR e PTW"
    if re.search(RX_PISTOLA, n):
        return "Pistola e SMG"
    if re.search(r"\bAEG\b", n) or (comp and comp >= 200):
        return "AEG"
    if comp:
        return "Pistola e SMG"
    return "Outros canos"


# Tracers: o tipo sai do nome, como na AAP01.
TIPOS_TRACER = [
    ("Silenciador com tracer", r"SILENCER|SUPPRESSOR"),
    ("Cronógrafo com tracer", r"CHRONOGRAPH"),
    ("Para shotgun", r"SHOTGUN|M870"),
    ("Para pistola e SMG", r"\bG19\b|MAXIM|KRISS|VECTOR"),
    ("Capas e acessórios", r"\bCASE\b"),
    ("Unidade tracer", r"."),
]

# Cada fonte vira um grupo de categorias na vitrine. Na ordem: quem vem antes fica com o produto repetido.
# "subcats": (endereço da subcategoria na Arsenal, d=, tipo na vitrine). Depois de ler as subcategorias,
# a categoria-mãe é lida para pegar o que ficou sem subcategoria (vai para "resto").
FONTES = [
    {"grupo": "Peças AAP01", "busca": ["aap01", "aap-01"], "nome_tem": r"AAP[\s-]?01", "tipos": TIPOS_AAP, "modelo": "AAP01"},
    {"grupo": "Magazines", "mae": ("airsoft-magazines-para-replicas-de-airsoft", 114), "resto": "Outros magazines", "subcats": [
        ("airsoft-magazines-para-replicas-de-airsoft-magazines-para-pistolas", 118, "Pistola"),
        ("airsoft-magazines-para-replicas-de-airsoft-magazines-para-rifles", 116, "Rifle"),
        ("airsoft-magazines-para-replicas-de-airsoft-magazines-para-snipers", 122, "Sniper"),
        ("airsoft-magazines-para-replicas-de-airsoft-magazines--shells-para-shotguns", 123, "Shotgun"),
        ("airsoft-magazines-para-replicas-de-airsoft-shells-para-pistolas-revolver", 431, "Revólver"),
        ("airsoft-magazines-para-replicas-de-airsoft-pecas-e-acessorios-para-magazines", 115, "Peças de magazine")]},
    {"grupo": "BBs", "mae": ("airsoft-bbs-", 163), "resto": "Outras BBs", "subcats": [
        ("airsoft-bbs--bbs-020g", 165, "0.20g"), ("airsoft-bbs--bbs-023g", 1209, "0.23g e 0.25g"),
        ("airsoft-bbs--bbs-025g--", 166, "0.23g e 0.25g"), ("airsoft-bbs--bbs-028g", 167, "0.28g e 0.30g"),
        ("airsoft-bbs--bbs-030g", 1211, "0.28g e 0.30g"), ("airsoft-bbs--bbs-032g", 1215, "0.32g a 0.36g"),
        ("airsoft-bbs--bbs-036g", 1217, "0.32g a 0.36g"), ("airsoft-bbs--bbs-038g", 1219, "0.38g ou mais"),
        ("airsoft-bbs--bbs-040g", 1213, "0.38g ou mais"), ("airsoft-bbs--bbs-042g", 1221, "0.38g ou mais"),
        ("airsoft-bbs--bbs-043g", 1225, "0.38g ou mais"), ("airsoft-bbs--bbs-045g", 1223, "0.38g ou mais"),
        ("airsoft-bbs--bbs-046g", 1231, "0.38g ou mais"), ("airsoft-bbs--bbs-048g", 1227, "0.38g ou mais"),
        ("airsoft-bbs--bbs-050g", 1229, "0.38g ou mais"), ("airsoft-bbs--speed-loader-carregador-bbs", 169, "Speed loader")]},
    {"grupo": "Baterias", "mae": ("airsoft-baterias--carregadores", 104), "resto": "Outros", "subcats": [
        ("airsoft-baterias--carregadores-lipo-batteries", 109, "LiPo"),
        ("airsoft-baterias--carregadores-liion-batteries", 639, "Li-Ion"),
        ("airsoft-baterias--carregadores-life-batteries", 108, "LiFe"),
        ("airsoft-baterias--carregadores-nimh-batteries", 110, "NiMH"),
        ("airsoft-baterias--carregadores-carregadores-de-bateria--fontes-de-energia", 112, "Carregadores e fontes"),
        ("airsoft-baterias--carregadores-acessorios-de-bateria", 105, "Acessórios de bateria"),
        ("airsoft-baterias--carregadores-cameras--scope--red-dot-batteries", 1247, "Pilhas para mira e lanterna"),
        ("airsoft-baterias--carregadores-flashlight-and-tracer-batteries", 106, "Pilhas para mira e lanterna")]},
    {"grupo": "Canos internos", "tipo_fn": tipo_cano, "tipos": TIPOS_CANO,
     "categorias": [("airsoft-pecas-internas-para-replicas-de-airsoft-canos-de-precisao-internos", 241)],
     "busca": ["inner+barrel", "inner-barrel", "tightbore", "cano+interno", "precision+barrel"],
     "nome_tem": r"INNER BARREL|INNER & OUT|TIGHTBORE|PRECISION BARREL|CANO INTERNO",
     # carabinas de pressão (PCP, chumbinho) não são airsoft
     "fora": r"\b(4[.,]5|5[.,]5|6[.,]35)\s?MM|\bPCP\b|\.(22|25|30)\b|AIRGUN|\bRING\b"},
    {"grupo": "Peças internas", "mae": ("airsoft-pecas-internas-para-replicas-de-airsoft", 229), "resto": "Outras peças internas", "subcats": [
        ("airsoft-pecas-internas-para-replicas-de-airsoft-gearbox", 238, "Gearbox"),
        ("airsoft-pecas-internas-para-replicas-de-airsoft-gears-e-partes-relacionadas", 239, "Engrenagens"),
        ("airsoft-pecas-internas-para-replicas-de-airsoft-pistons", 244, "Pistão e cabeça"),
        ("airsoft-pecas-internas-para-replicas-de-airsoft-piston-heads", 245, "Pistão e cabeça"),
        ("airsoft-pecas-internas-para-replicas-de-airsoft-cylinders", 235, "Cilindro e cabeça"),
        ("airsoft-pecas-internas-para-replicas-de-airsoft-cylinder-heads", 234, "Cilindro e cabeça"),
        ("airsoft-pecas-internas-para-replicas-de-airsoft-springs", 249, "Molas e guias"),
        ("airsoft-pecas-internas-para-replicas-de-airsoft-spring-guides", 250, "Molas e guias"),
        ("airsoft-pecas-internas-para-replicas-de-airsoft-hopup", 240, "Hop-up"),
        ("airsoft-pecas-internas-para-replicas-de-airsoft-nozzles", 601, "Nozzles e tappet"),
        ("airsoft-pecas-internas-para-replicas-de-airsoft-tappet-plates", 252, "Nozzles e tappet"),
        ("airsoft-pecas-internas-para-replicas-de-airsoft-motors-and-acessories", 242, "Motores"),
        ("airsoft-pecas-internas-para-replicas-de-airsoft-electronic-trigger-wiring--mosfets", 255, "Mosfets e fiação"),
        ("airsoft-pecas-internas-para-replicas-de-airsoft-trigger-internal-parts", 578, "Gatilho, seletor e travas"),
        ("airsoft-pecas-internas-para-replicas-de-airsoft-selector-plates", 246, "Gatilho, seletor e travas"),
        ("airsoft-pecas-internas-para-replicas-de-airsoft-antireversal-latches", 231, "Gatilho, seletor e travas"),
        ("airsoft-pecas-internas-para-replicas-de-airsoft-cut-off-levers", 233, "Gatilho, seletor e travas"),
        ("airsoft-pecas-internas-para-replicas-de-airsoft-delayers", 236, "Gatilho, seletor e travas"),
        ("airsoft-pecas-internas-para-replicas-de-airsoft-bushings--bearings", 247, "Buchas, rolamentos e shims"),
        ("airsoft-pecas-internas-para-replicas-de-airsoft-shims", 67, "Buchas, rolamentos e shims"),
        ("airsoft-pecas-internas-para-replicas-de-airsoft-orings", 243, "O-rings"),
        ("airsoft-pecas-internas-para-replicas-de-airsoft-kits-de-upgrade", 254, "Kits de upgrade"),
        ("airsoft-pecas-internas-para-replicas-de-airsoft-hpa-pecas-e-acessorios", 1147, "HPA")]},
    {"grupo": "Tracers", "mae": ("airsoft-pecas-externas-para-replicas-de-airsoft-silencers--tracers--amplifiers-tracer", 1689),
     "subcats": [], "tipos": TIPOS_TRACER},
]

# Categorias da Arsenal que não são peças (réplicas inteiras, coldres, roupas).
EXCLUIR_CAT = {"REPLICAS DE AIRSOFT", "COLDRES", "EQUIPAMENTO E VESTUARIO"}
# Sacos de BBs de 10kg ou mais também ficam fora (pedido do jota).
EXCLUIR_NOME = re.compile(r"HOLSTER|COLDRE|BLOWBACK (AIRSOFT )?PISTOL\b|\b([1-9]\d+)\s?KG\b", re.I)
# Itens que o jota pediu para tirar da vitrine (Ref. da Arsenal).
EXCLUIR_SKU = {"130776", "268776", "168045"}

MARCAS = {"CTM-TAC": "CTM-TAC", "COWCOW TECHNOLOGY": "CowCow", "COWCOW": "CowCow", "T-N.T.": "TNT", "TNT": "TNT",
          "ACTION ARMY": "Action Army", "TTI AIRSOFT": "TTI Airsoft", "G&G": "G&G", "A&K": "A&K", "KWA": "KWA",
          "KWC": "KWC", "APS": "APS", "SHS": "SHS", "SRC": "SRC", "UFC": "UFC", "ASG": "ASG", "WE": "WE", "VFC": "VFC",
          "ICS": "ICS", "BBQ": "BBQ", "CYMA": "Cyma", "E&C": "E&C", "LCT": "LCT", "JG": "JG", "SKYRC": "SkyRC", "PDI": "PDI"}
SIGLAS = {"RGB", "BT", "AAP01", "AAP01C", "CNC", "RMR", "GBB", "HPA", "TM", "G18", "G18C", "DDW", "FDE", "PCC", "AP7", "SSP18",
          "M4", "V2", "SS", "TTI", "CTM", "RIS", "TDC", "AW", "WE", "ABS", "TPU", "NBR", "AEG", "QD", "CO2", "TYPE",
          "AK", "AR", "SR", "MP5", "G36", "SVD", "VSR", "BB", "BBS", "USB", "USB-C", "LED", "AB", "PDW", "AUG", "HK",
          "SMG", "PTW", "GBBR", "MWS", "KWA", "KWC", "APS", "SHS", "SRC", "UFC", "ASG", "VFC", "ICS", "LCT", "JG",
          "M16", "M14", "M249", "MK", "DMR", "PKM", "CQB", "EBB", "MOSFET", "ETU", "LIPO", "NIMH",
          "6061", "7075", "XL", "XS", "SL", "SP", "KA", "SBD", "PEQ", "MPX", "MCX", "SCAR", "MTW", "PDX", "G&G", "A&K",
          "E&C", "S&T", "S&W", "M&P9", "M&P", "CA", "CM", "TK", "TK.45", "TK.45C", "1X", "2X", "3S1P", "2S1P", "II", "III", "IV", "MDRX", "EMG", "LMG", "DTU", "RPM", "PCS", "2PCS", "5PCS"}
MINUSC = {"for", "and", "with", "of", "the", "to", "in", "&", "or"}


# Subdivisões dentro de alguns tipos, pelo nome original da Arsenal. A primeira regra que casar vence;
# a última de cada lista pega o resto.
DIAMETROS = [("6.01mm", r"6[.,]01"), ("6.02mm a 6.03mm", r"6[.,]0[23]|\b0[23] FOR"), ("6.04mm a 6.05mm", r"6[.,]0[45]|\b05 FOR"),
             ("6.08mm ou mais", r"6[.,](0[6-9]|1\d)|\b(08|12) FOR"), ("Diâmetro não informado", r".")]
SUBTIPOS = {
    ("Magazines", "Rifle"): [("Drum", r"DRUM"), ("GBBR", r"\bGBBR?\b|\bGAS\b"), ("Hi-cap", r"HI[\s-]?CAP"),
                             ("Mid-cap", r"MID[\s-]?CAP"), ("Low-cap", r"LOW[\s-]?CAP|REAL[\s-]?CAP"), ("Outros", r".")],
    ("Magazines", "Pistola"): [("CO2", r"CO2"), ("Gás (GBB)", r"\bGBB\b|\bGAS\b|GREEN"), ("Elétrica (AEP)", r"\bAEP\b|ELECTRIC"),
                               ("Outros", r".")],
    ("Peças internas", "Gearbox"): [("Gearbox completa", r"COMPLETE"), ("Carcaça", r"SHELL|CASE"),
                                    ("Parafusos e clamps", r"SCREW|CLAMP"), ("Outras peças de gearbox", r".")],
    ("Peças internas", "Hop-up"): [("Borrachas", r"BUCKING|RUBBER"), ("Câmaras", r"CHAMBER"),
                                   ("Braços, nubs e tensores", r"\bNUB|\bARM\b|TENSIONER|LEVER|TROLLEY"), ("Outros", r".")],
    ("Peças internas", "Molas e guias"): [("Guias", r"GUIDE"), ("Molas", r".")],
    ("Peças internas", "Engrenagens"): [("Jogos", r"\bSET\b|\bGEARS\b"), ("Avulsas", r".")],
    **{("Canos internos", c): DIAMETROS for c, _ in TIPOS_CANO},
    ("Peças internas", "Canos de precisão"): [("6.01mm", r"6\.01"), ("6.02mm", r"6\.02"), ("6.03mm", r"6\.03"),
                                              ("6.04mm a 6.05mm", r"6\.0[45]"), ("Outros", r".")],
    ("Baterias", "LiPo"): [("7.4V", r"7\.4"), ("11.1V", r"11\.1"), ("Outras", r".")],
}

# Tradução curta do nome. Na ordem: frases antes das palavras soltas.
TRADUCAO = [
    (r"\bOut(t)?er (& |and )?Inner Barrel\b", "Cano externo e interno"), (r"\bOuter Barrel\b", "Cano externo"),
    (r"\bInner Barrel Stabilizer\b|\bBarrel Stabilizer\b", "Estabilizador de cano"), (r"\bInner Barrel Spacer\b|\bBarrel Spacer\b", "Espaçador de cano"),
    (r"\bInner Barrel\b", "Cano interno"), (r"\bHop-Up Chamber\b", "Câmara de hop-up"),
    (r"\bHop-Up Bucking\b", "Borracha de hop-up"), (r"\bBucking\b", "borracha"),
    (r"\bGearbox Shell\b", "Carcaça de gearbox"), (r"\bGearbox Complete\b|\bComplete Gearbox\b", "Gearbox completa"),
    (r"\bPiston Head\b", "Cabeça de pistão"), (r"\bCylinder Head\b", "Cabeça de cilindro"),
    (r"\bSpring Guide\b|\bGuide Rod\b", "Guia de mola"), (r"\bSprings\b", "Molas"), (r"\bSpring\b", "Mola"),
    (r"\bPiston\b", "Pistão"), (r"\bCylinder\b", "Cilindro"), (r"\bGear Set\b|\bGears Set\b", "Jogo de engrenagens"),
    (r"\bGears\b", "Engrenagens"), (r"\bGear\b", "Engrenagem"), (r"\bBearings\b", "rolamentos"), (r"\bBearing\b", "rolamento"),
    (r"\bBushings\b", "buchas"), (r"\bBushing\b", "bucha"), (r"\bCharger Battery\b|\bBattery Charger\b", "Carregador de bateria"),
    (r"\bSilencer Tracer\b", "Silenciador tracer"), (r"\bTracer Unit\b", "Unidade tracer"), (r"\bUnit\b", "unidade"),
    (r"\bCarbon Fiber Case\b", "Capa de fibra de carbono"), (r"\bFlare Case\b", "Capa Flare"), (r"\bCase\b", "capa"),
    (r"\bChronograph\b", "Cronógrafo"), (r"\bwith Remote (.*?) Control\b", r"com controle remoto \1"),
    (r"\bRemovable Battery\b", "bateria removível"), (r"\bRechargeable\b", "recarregável"), (r"\bColorful Lights\b", "luzes coloridas"),
    (r"\bShape\b", "formato"), (r"\bfor Green BBs Only\b", "só para BBs verdes"), (r"\bCcw\b", "CCW"),
    (r"\bPrecision\b", "precisão"), (r"\bSilencer\b(?! Tracer)", "silenciador"), (r"\bCharger\b", "Carregador"), (r"\bBattery\b", "Bateria"), (r"\bPower Supply\b", "Fonte"),
    (r"\bFemale Plug\b", "plug fêmea"), (r"\bMale Plug\b", "plug macho"), (r"\bBottle\b", "garrafa"), (r"\bBag\b", "saco"),
    (r"\bTrigger\b", "Gatilho"), (r"\bSelector Plate\b", "Placa seletora"), (r"\bSelector\b", "Seletor"),
    (r"\bRear Wire[ds]?\b", "fiação traseira"), (r"\bFront Wire[ds]?\b", "fiação frontal"), (r"\bWiring\b", "fiação"),
    (r"\bStainless Steel\b", "aço inox"), (r"\bSteel\b", "aço"), (r"\bAlumin(i)?um\b", "alumínio"), (r"\bPolymer\b", "polímero"),
    (r"\bCarbon\b", "carbono"), (r"\bRubber\b", "borracha"), (r"\bTeeth\b", "dentes"), (r"\bHigh Torque\b", "alto torque"),
    (r"\bHigh Speed\b", "alta velocidade"), (r"\bReplacement\b", "reposição"), (r"\bAdapter\b", "adaptador"),
    (r"\bfor ([\w.&/-]+) Series\b", r"para série \1"), (r"\bSeries\b", "série"), (r"\bfor\b", "para"), (r"\bwith\b", "com"),
    (r"\band\b", "e"), (r"\bFlat Dark Earth\b", "FDE"), (r"\bBlack\b", "preto"), (r"\bRed\b", "vermelho"), (r"\bSilver\b", "prata"),
    (r"\bGold\b", "dourado"), (r"\bBlue\b", "azul"), (r"\bGreen\b", "verde"), (r"\bGr[ae]y\b", "cinza"), (r"\bPink\b", "rosa"),
    (r"\bViolet\b|\bPurple\b", "roxo"), (r"\bOrange\b", "laranja"), (r"\bWhite\b", "branco"), (r"\bClear\b", "transparente"),
    (r"\bDesert\b", "deserto"), (r"\bAirsoft\b ?", ""),
    (r"^Tracer Capa (.*)", r"Capa para tracer \1"), (r" e\s*$", ""), (r"\bfor verde BBS Only\b|\bpara verde BBS Only\b", "só para BBs verdes"),
]


def traduz(nome, grupo):
    t = nome
    if grupo == "Magazines":
        t = re.sub(r"\b(\d+)R\b", r"\1 BBs", t)
    for rx, novo in TRADUCAO:
        t = re.sub(rx, novo, t)
    t = re.sub(r"(\d)MM\b", r"\1mm", t)
    t = re.sub(r"^(.*?\bCano interno\b.*?)\s+Cano interno\b", r"\1", t)
    t = re.sub(r"\s{2,}", " ", t).strip(" -/")
    return t[:1].upper() + t[1:]


def subtipo(p):
    regras = SUBTIPOS.get((p["grupo"], p["cat"]))
    if not regras:
        return p["sub"]
    for nome, rx in regras:
        if re.search(rx, p["arsenal"]["nome"], re.I):
            return nome


def baixar(url, tentativas=3):
    for i in range(tentativas):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (vitrine-airsoft)"})
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read()
        except Exception:
            if i == tentativas - 1:
                raise
            time.sleep(2 ** i)


def limpa(s):
    return html.unescape(re.sub(r"\s+", " ", s)).strip() if s else None


def ler_listagem(t):
    """Devolve os cartões de produto de uma página de listagem."""
    out = []
    for b in t.split('class="product-wrap"')[1:]:
        m = re.search(r'/produto/([^"]+)-(\d+)\.html', b)
        if not m:
            continue
        g = lambda p: limpa((re.search(p, b, re.S) or [None, None])[1])
        preco = g(r'class="new-price">\s*USD\s*([\d\.,]+)')
        out.append({
            "id": int(m.group(2)),
            "url": f"{BASE}/produto/{m.group(1)}-{m.group(2)}.html",
            "cat_arsenal": g(r'<h3 class="product-name"[^>]*>\s*([^<]+?)\s*</h3>'),
            "img": g(r'<img src="([^"]+)"'),
            "marca": g(r'class="product-cat"[^>]*>\s*<a[^>]*>([^<]+)</a>'),
            "ref": g(r'Ref\.:\s*([^<]+)<br>'),
            "nome": g(r'Ref\.:[^<]*<br>\s*([^<]+)</a>'),
            "usd": float(preco.replace(".", "").replace(",", ".")) if preco else None,
        })
    return out


def listar(url):
    """Lê todas as páginas de uma listagem (busca ou categoria)."""
    vistos, pagina = {}, 1
    while True:
        t = baixar(f"{url}&pagina={pagina}").decode("utf-8", errors="replace")
        itens = [x for x in ler_listagem(t) if x["id"] not in vistos]
        if not itens:
            return list(vistos.values())
        for x in itens:
            vistos[x["id"]] = x
        pagina += 1


def titulo(nome, marca):
    nome = re.sub(r"^(COWCOW TECHNOLOGY|COWCOW|T-N\.T\.|TNT|" + re.escape(marca) + r")\s+(TNT\s+)?", "", nome, flags=re.I)
    out = []
    for i, w in enumerate(nome.split()):
        u = w.upper()
        if re.fullmatch(r"\d+(\.\d+)?MM", u):
            out.append(u[:-2] + "mm")
        elif re.fullmatch(r"\d+MAH", u):
            out.append(u[:-3] + "mAh")
        elif re.fullmatch(r"[\d.]+G", u):
            out.append(u[:-1] + "g")
        elif w != u and re.search(r"\d", w):
            out.append(w)  # já vem com caixa certa, como 600mAh
        elif u.strip(",()/") in SIGLAS or "." in w or re.search(r"\d", w) and len(w) <= 8:
            out.append(u)
        elif w.lower() in MINUSC and i:
            out.append(w.lower())
        else:
            out.append("-".join(p.capitalize() for p in w.split("-")))
    t = " ".join(out)
    for a, b in (("Relaease", "Release"), ("Nozzel", "Nozzle"), ("Eletroplated", "Electroplated"),
                 ("Coonverter", "Converter"), ("Suply", "Supply")):
        t = t.replace(a, b)
    return t


def tipo_por_nome(x, regras):
    for alvo in (x["nome"], x["cat_arsenal"] or ""):  # primeiro o nome, depois a categoria da Arsenal
        for nome, rx in regras[:-1]:
            if re.search(rx, alvo, re.I):
                return nome
    return regras[-1][0]  # a última regra é o "outros"


def specs_aap(nome):
    compat = ["AAP01"]
    if re.search(r"AAP01C", nome):
        compat.append("AAP01C")
    if re.search(r"\bG18\b|G SERIES|TM G", nome):
        compat.append("série G (Glock)")
    return "Compatível: " + ", ".join(compat)


def miniatura(pid, url):
    """Baixa a foto da Arsenal e salva uma miniatura leve em img/<id>.webp."""
    from PIL import Image
    rel = f"img/{pid}.webp"
    dest = os.path.join(AQUI, rel)
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        return rel
    if not url:
        return None
    try:
        im = Image.open(io.BytesIO(baixar(url))).convert("RGBA")
        fundo = Image.new("RGB", im.size, (255, 255, 255))
        fundo.paste(im, mask=im.split()[3])
        fundo.thumbnail((320, 320))
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        fundo.save(dest, "WEBP", quality=72)
        return rel
    except Exception as e:
        print("  sem foto:", pid, e, file=sys.stderr)
        return None


def coletar(f):
    """Devolve [(item da Arsenal, tipo)] de uma fonte."""
    if "tipo_fn" in f:  # categorias da Arsenal + buscas, tipo decidido pelo nome
        brutos = {}
        for slug, d in f["categorias"]:
            for x in listar(f"{BASE}/produtos/{slug}/filter?d={d}"):
                brutos[x["id"]] = x
        for q in f["busca"]:
            for x in listar(f"{BASE}/produtos/filter?q={q}"):
                if x["nome"] and re.search(f["nome_tem"], x["nome"], re.I):
                    brutos[x["id"]] = x
        return [(x, f["tipo_fn"](x)) for x in brutos.values()
                if x["nome"] and not re.search(f["fora"], f"{x['nome']} {x['cat_arsenal'] or ''}", re.I)]
    if "busca" in f:
        brutos = {}
        for q in f["busca"]:
            for x in listar(f"{BASE}/produtos/filter?q={q}"):
                brutos[x["id"]] = x
        return [(x, tipo_por_nome(x, f["tipos"])) for x in brutos.values()
                if x["nome"] and re.search(f["nome_tem"], x["nome"], re.I)]
    out, vistos = [], set()
    for slug, d, tipo in f["subcats"]:
        for x in listar(f"{BASE}/produtos/{slug}/filter?d={d}"):
            if x["id"] not in vistos:
                vistos.add(x["id"]); out.append((x, tipo))
    slug, d = f["mae"]
    for x in listar(f"{BASE}/produtos/{slug}/filter?d={d}"):
        if x["id"] not in vistos:
            vistos.add(x["id"]); out.append((x, tipo_por_nome(x, f["tipos"]) if "tipos" in f else f["resto"]))
    return out


def main(so=None):
    """Lê a Arsenal. Com so="Grupo", lê só esse grupo e mantém o resto do produtos.json."""
    produtos, ordem_tipos, antes = {}, [], {}
    if so:
        dados = json.load(open(os.path.join(AQUI, "produtos.json"), encoding="utf-8"))
        produtos = {p["arsenal"]["id"]: p for p in dados["produtos"]
                    if p["grupo"] != so and p["sku"] not in EXCLUIR_SKU and not EXCLUIR_NOME.search(p["arsenal"]["nome"])}
        antes = {g["grupo"]: g for g in dados["estrutura"]}
    for f in FONTES:
        if so and f["grupo"] != so:
            if f["grupo"] in antes:
                ordem_tipos.append(antes[f["grupo"]])
            continue
        itens = coletar(f)
        tipos = [t for t, _ in f["tipos"]] if "tipos" in f else list(dict.fromkeys([s[2] for s in f["subcats"]] + [f["resto"]]))
        ordem_tipos.append({"grupo": f["grupo"], "cats": tipos})
        novos = 0
        for x, tipo in itens:
            if so and x["id"] in produtos and produtos[x["id"]]["grupo"] != "Peças AAP01":
                del produtos[x["id"]]
            if x["id"] in produtos or not x["nome"]:
                continue
            if (x["cat_arsenal"] or "").upper() in EXCLUIR_CAT or EXCLUIR_NOME.search(x["nome"]):
                continue
            if (x["ref"] or "") in EXCLUIR_SKU:
                continue
            marca = MARCAS.get((x["marca"] or "").upper(), (x["marca"] or "").title())
            produtos[x["id"]] = {
                "sku": x["ref"] or f"A{x['id']}",
                "nome": titulo(x["nome"], x["marca"] or ""),
                "marca": marca,
                "grupo": f["grupo"],
                "cat": tipo,
                "sub": f.get("modelo", ""),
                "specs": specs_aap(x["nome"]) if f.get("modelo") == "AAP01" else "",
                "usd": x["usd"],
                "disponivel": x["usd"] is not None,
                "img": None,
                "arsenal": {"id": x["id"], "url": x["url"], "ref": x["ref"], "nome": x["nome"], "marca_arsenal": x["marca"],
                            "categoria": x["cat_arsenal"], "img": x["img"]},
            }
            novos += 1
        print(f"{f['grupo']}: {novos} produtos", flush=True)

    finalizar(list(produtos.values()), ordem_tipos)


def finalizar(lista, ordem_tipos):
    """Nome em português, subdivisões, ordem, fotos, produtos.json e o bloco do index.html."""
    for p in lista:
        p["orig"] = titulo(p["arsenal"]["nome"], p["arsenal"].get("marca_arsenal") or p["marca"])
        p["nome"] = traduz(p["orig"], p["grupo"])
        p["sub"] = subtipo(p)
    ordem_sub = {(g, c): {s: i for i, (s, _) in enumerate(r)} for (g, c), r in SUBTIPOS.items()}
    pos = {(g["grupo"], c): (i, j) for i, g in enumerate(ordem_tipos) for j, c in enumerate(g["cats"])}
    lista = sorted(lista, key=lambda p: (pos[(p["grupo"], p["cat"])], ordem_sub.get((p["grupo"], p["cat"]), {}).get(p["sub"], 0),
                                         p["marca"], p["nome"]))
    # só mostra tipos que têm produto
    ordem_tipos = [{"grupo": g["grupo"], "cats": [c for c in g["cats"] if any(p["grupo"] == g["grupo"] and p["cat"] == c for p in lista)]}
                   for g in ordem_tipos]

    with ThreadPoolExecutor(8) as ex:
        fotos = list(ex.map(lambda p: miniatura(p["arsenal"]["id"], p["arsenal"]["img"]), lista))
    for p, img in zip(lista, fotos):
        p["img"] = img

    agora = datetime.now(timezone(timedelta(hours=-3))).replace(microsecond=0).isoformat()
    json.dump({"atualizado_em": agora, "fonte": BASE, "estrutura": ordem_tipos, "produtos": lista},
              open(os.path.join(AQUI, "produtos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    # Atualiza o bloco embutido no index.html (o artifact não consegue buscar arquivos de fora).
    caminho = os.path.join(AQUI, "index.html")
    pagina = open(caminho, encoding="utf-8").read()
    campos = ("sku", "nome", "orig", "marca", "grupo", "cat", "sub", "specs", "usd", "disponivel", "img")
    linhas = ",\n".join("  " + json.dumps({k: p[k] for k in campos if p[k] not in ("", None) or k == "usd"}, ensure_ascii=False)
                        for p in lista)
    bloco = ("// PRODUTOS:INICIO (gerado por importar_arsenal.py, não edite à mão)\n"
             f"const ATUALIZADO_EM = \"{agora}\";\n"
             f"const ESTRUTURA = {json.dumps(ordem_tipos, ensure_ascii=False)};\n"
             f"const PRODUTOS = [\n{linhas}\n];\n// PRODUTOS:FIM")
    novo, n = re.subn(r"// PRODUTOS:INICIO.*?// PRODUTOS:FIM", lambda m: bloco, pagina, flags=re.S)
    if n != 1:
        sys.exit("Não achei o bloco // PRODUTOS:INICIO ... // PRODUTOS:FIM no index.html")
    open(caminho, "w", encoding="utf-8").write(novo)

    disp = sum(p["disponivel"] for p in lista)
    print(f"{len(lista)} produtos ({disp} disponíveis, {len(lista) - disp} indisponíveis)")
    for (g, c), n in sorted(Counter((p["grupo"], p["cat"]) for p in lista).items(), key=lambda k: pos[k[0]]):
        print(f"  {n:5d}  {g} / {c}")


if __name__ == "__main__":
    if "--reprocessar" in sys.argv:  # refaz nomes, subdivisões e a página a partir do produtos.json, sem ler a Arsenal
        dados = json.load(open(os.path.join(AQUI, "produtos.json"), encoding="utf-8"))
        finalizar([p for p in dados["produtos"] if p["sku"] not in EXCLUIR_SKU and not EXCLUIR_NOME.search(p["arsenal"]["nome"])],
                  dados["estrutura"])
    elif "--so" in sys.argv:  # lê só um grupo: --so "Tracers"
        main(sys.argv[sys.argv.index("--so") + 1])
    else:
        main()
