"""Lê a aba Descrição/Especificações de cada produto na Arsenal e guarda o texto bruto em arsenal_bruto.json (por Ref.)."""
import re, html, json, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor
PASTA = sys.argv[1] if len(sys.argv) > 1 else "."
produtos = json.load(open(sys.argv[2] if len(sys.argv) > 2 else "produtos.json"))["produtos"]
saida = f"{PASTA}/arsenal_bruto.json"
try: bruto = json.load(open(saida))
except Exception: bruto = {}
def ler(p):
    for t in range(3):
        try:
            s = urllib.request.urlopen(urllib.request.Request(p["arsenal"]["url"], headers={"User-Agent": "Mozilla/5.0"}), timeout=30).read().decode("utf8", "ignore")
            break
        except Exception: time.sleep(3 * (t + 1))
    else: return p["sku"], None
    t = re.sub(r"<script.*?</script>|<style.*?</style>", "", s, flags=re.S)
    t = html.unescape(re.sub(r"<[^>]+>", "\n", t)); t = re.sub(r"[ \t]+", " ", t); t = re.sub(r"\n\s*\n*", "\n", t)
    a = t.find("Descrição\nEspecificações\n")
    fim = [i for i in (t.find("*As descri", a), t.find("* As descri", a), t.find("SKU\n", a)) if i > 0]
    desc = t[a + len("Descrição\nEspecificações\n"):min(fim)].strip() if a >= 0 and fim else ""
    fab = re.search(r"Código Fabricante\n\s*(.+)", t)
    return p["sku"], {"desc": desc, "fab": fab.group(1).strip() if fab else ""}
faltam = [p for p in produtos if p["sku"] not in bruto]
print(len(faltam), "para ler")
with ThreadPoolExecutor(4) as ex:
    for i, (sku, d) in enumerate(ex.map(ler, faltam)):
        if d is not None: bruto[sku] = d
        if i % 200 == 0:
            json.dump(bruto, open(saida, "w"), ensure_ascii=False); print(i, flush=True)
json.dump(bruto, open(saida, "w"), ensure_ascii=False)
print("ok", len(bruto))
