"""Gera detalhes/REF.json (seção "Sobre o produto" da página de cada produto).

Junta três fontes, nesta ordem de prioridade:
  1. manual.json   - textos revisados à mão, com pesquisa em sites de fabricantes e lojas (por Ref.)
  2. arsenal_bruto.json - descrição e código do fabricante lidos da Arsenal (coletar_arsenal.py)
  3. categorias.py - o que é a peça e dicas, por categoria

Uso, na raiz do repositório:  python3 ferramentas/detalhes/gerar_detalhes.py
"""
import json, os, re, sys
from datetime import date

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from categorias import texto

RAIZ = sys.argv[1] if len(sys.argv) > 1 else "."
SAIDA = os.path.join(RAIZ, "detalhes")

# linhas da Arsenal que não acrescentam nada para o cliente
LIXO = re.compile(r"^(peça de (reposição|atualização)|produto original|características?:?$|especificaç(ão|ões):?$|descrição:?$|"
                  r"partes internas$|para airsoft$|uso exc?lu[is]+vo|alta qualidade|altíssima qualidade|alta durabilidade|"
                  r"\*|as descrições|calibre:? ?6 ?mm|6 ?mm$|cnc$|peso [\d,.]+ libras|dimensões [\d,.]+ ?× ?[\d,.]+ ?× ?[\d,.]+ ?em|"
                  r"polido à perfeição|várias cores|adequad[oa] para (o )?airsoft\.?$|acabado à mão$|estilo ousado|aviso:?$|obs\.?:?$|observação:?$|observe:?$)", re.I)
# chaves que não vão para a ficha (repetem o que já está na página, ou podem contradizer a variante de cor)
CHAVE_FORA = {"fabricante", "marca", "fornecedor", "sku", "item número.", "nome do produto", "cor", "cor do produto", "cor principal",
              "bb cor", "modelo", "peso bruto", "embalagem do produto", "calibre", "bb", "pistola", "rifle"}
CHAVE_COMPAT = {"compatibilidade", "compatbilidade", "compatiblidade", "modelo aplicável", "plataforma", "aplicação", "adequado para"}
CHAVE_INCLUI = {"conteúdo da embalagem", "o pacote inclui", "conteúdo", "conteúdo do pacote", "inclui", "acompanha"}
NOME_CHAVE = {"capacidade de carga": "Capacidade", "materiais": "Material", "voltagem": "Tensão", "peso líquido": "Peso",
              "peso do produto": "Peso", "peso líquido do produto": "Peso", "peso líquido (g)": "Peso", "dimensão": "Dimensões",
              "tamanho do produto": "Dimensões", "tamanho": "Dimensões", "diâmetro interno do cano": "Diâmetro interno",
              "batteria": "Bateria", "tipo de célula de bateria": "Tipo de célula", "capacidade nominal": "Capacidade",
              "relação": "Relação (ratio)", "tamanho do bb": "Tamanho da BB", "bb qualidade": "Qualidade da BB",
              "tipo de gás": "Gás", "sistema": "Sistema", "especificação": "Especificação"}
MATERIAL = {"metal": "Metal", "polímero": "Polímero", "aluminum": "Alumínio", "alumínio": "Alumínio", "aço": "Aço",
            "nylon": "Nylon", "aço inoxidável": "Aço inox", "borracha": "Borracha", "silicone": "Silicone"}


ERROS = {"Aliminum": "Alumínio", "Aluminium": "Alumínio", "Aluminum": "Alumínio", "excluisvo": "exclusivo", "maganesa": "manganês",
         "inovadorem": "inovador em", "Compatbilidade": "Compatibilidade", "Compatiblidade": "Compatibilidade",
         "barris": "canos", "Barris": "Canos", "barril": "cano", "Barril": "Cano", "caixas de engrenagens": "gearboxes",
         "caixa de engrenagens": "gearbox", "Caixa de engrenagens": "Gearbox", "placa de tucho": "tappet plate", "Válvula de bico": "Válvula do nozzle"}


def limpa(s):
    s = re.sub(r"\s+", " ", s.replace("​", "")).strip(" -•·\t")
    for a, b in ERROS.items():
        s = s.replace(a, b)
    s = re.sub(r"\b(\d+)\s*Rounds?\b", r"\1 BBs", s, flags=re.I)
    s = re.sub(r"\bRondas\b", "BBs", s)
    return s


def analisa(desc):
    specs, compat, inclui, destaques = [], [], [], []
    vistos = set()
    modo = None
    for linha in desc.split("\n"):
        l = limpa(linha)
        if len(l) < 3 or LIXO.match(l):
            continue
        m = re.match(r"^([A-Za-zÀ-ÿ][^:;]{1,31})[:;]\s*(.*)$", l)
        if m:
            chave, valor = m.group(1).strip(), m.group(2).strip()
            k = chave.lower()
            if not valor:  # cabeçalho de uma lista nas linhas seguintes
                modo = "inclui" if k in CHAVE_INCLUI else "compat" if k in CHAVE_COMPAT else None
                continue
            modo = None
            if k in CHAVE_FORA:
                continue
            if k in CHAVE_COMPAT:
                compat.append(valor); continue
            if k in CHAVE_INCLUI:
                inclui += [limpa(x) for x in re.split(r",|;| e (?=\d)", valor) if limpa(x)]; continue
            nome = NOME_CHAVE.get(k, chave[:1].upper() + chave[1:])
            if nome == "Material":
                valor = MATERIAL.get(valor.lower(), valor[:1].upper() + valor[1:])
            if nome == "Material":
                valor = MATERIAL.get(valor.lower(), valor[:1].upper() + valor[1:])
            if nome.lower() in vistos or len(valor) > 140 or len(nome) > 28:
                if len(l) <= 220: destaques.append(l)
                continue
            vistos.add(nome.lower()); specs.append([nome, valor])
            continue
        if modo == "inclui" and len(l) <= 100:
            inclui.append(l); continue
        if modo == "compat" and len(l) <= 200:
            compat.append(l); continue
        if re.fullmatch(r"(\d{2,3}\.?\d{3})\s*RPM", l, re.I):
            if "rotação" not in vistos: vistos.add("rotação"); specs.append(["Rotação", l.upper().replace(" ", "")])
            continue
        mt = re.fullmatch(r"(long|short|medium)\s*type", l, re.I)
        if mt:
            if "eixo" not in vistos: vistos.add("eixo"); specs.append(["Eixo", {"long": "Longo (long type)", "short": "Curto (short type)", "medium": "Médio (medium type)"}[mt.group(1).lower()]])
            continue
        if re.fullmatch(r"\d{1,2}[.,]\d\s*V", l, re.I):
            if "tensão" not in vistos: vistos.add("tensão"); specs.append(["Tensão", l.replace(" ", "")])
            continue
        if len(l) < 16:
            continue
        mf = re.match(r"^feit[oa] (?:em|de) (.+)$", l, re.I)
        if mf:
            mat = MATERIAL.get(mf.group(1).strip().lower(), mf.group(1).strip())
            if "material" not in vistos:
                vistos.add("material"); specs.append(["Material", mat])
            continue
        if re.match(r"^(para (a )?(linha|o|série|uso)|compatível com|compatível:|adequad[oa] para|serve (em|para))", l, re.I) and len(l) <= 200:
            compat.append(l); continue
        if 8 <= len(l) <= 220 and l not in destaques:
            destaques.append(l)
    return specs, compat, inclui, destaques


def frase(s):
    s = s.strip().rstrip(".")
    return s[:1].upper() + s[1:] + "." if s else ""


def specs_bateria(nome):
    """Lê do nome da bateria tensão, capacidade, descarga, células e conector (ex.: 'LIPO 25C / 11.1 / 1500 / 3S1P Deans')."""
    n, s = nome.upper(), []
    v = re.search(r"(\d{1,2}[.,]\d{1,2})\s*V?\b(?!\s*MAH)", n)
    mah = re.search(r"(\d{3,5})\s*(MAH)?\b(?!\s*RPM)", re.sub(r"\d+C\b|\d{1,2}[.,]\d+\s*V?", "", n))
    c = re.search(r"\b(\d{2,3})C\b", n)
    cel = re.search(r"\b(\d)S(\d)P\b", n) or re.search(r"\b(\d)S\b", n)
    if v: s.append(["Tensão", v.group(1).replace(",", ".") + "V"])
    if mah: s.append(["Capacidade", mah.group(1) + " mAh"])
    if c: s.append(["Descarga", c.group(1) + "C"])
    if cel: s.append(["Células", cel.group(0)])
    for chave, nome_c in (("NUNCHUCK", "Nunchuck (2 partes ligadas por fio)"), ("BUTTERFLY", "Butterfly (3 partes)"), ("TRIPLE", "Triple (3 bastões)"),
                          ("BUTTER STICK", "Butter stick"), ("AK STICK", "Stick para AK"), ("STICK", "Stick (bastão único)"), ("MICRO SIZE", "Micro (para HPA e AEP)")):
        if chave in n:
            s.append(["Formato", nome_c]); break
    for chave, nome_c in (("DEANS", "Deans (T-plug)"), ("T PLUG", "Deans (T-plug)"), ("MINI TAMIYA", "Mini Tamiya"), ("TAMIYA", "Tamiya"), ("JST", "JST")):
        if chave in n:
            s.append(["Conector", nome_c]); break
    return s


def familia(p, familias):
    for f in familias:
        if f.get("marca") and f["marca"] != p["marca"]: continue
        if f.get("grupo") and f["grupo"] != p["grupo"]: continue
        if f.get("cat") and f["cat"] != p["cat"]: continue
        if re.search(f["nome"], p["nome"], re.I) or re.search(f["nome"], p.get("orig") or "", re.I):
            return f
    return {}


def gera(p, bruto, manual):
    t = texto(p["grupo"], p["cat"], p.get("sub") or "")
    b = bruto.get(p["sku"]) or {}
    specs, compat, inclui, destaques = analisa(b.get("desc", ""))
    if p["grupo"] == "Baterias" and p["cat"] in ("LiPo", "Li-Ion", "LiFe", "NiMH"):
        doNome = specs_bateria(p.get("orig") or p["nome"])
        tem = {k.lower() for k, _ in specs}
        specs = [x for x in doNome if x[0].lower() not in tem] + specs
    f = familia(p, manual.get("familias", []))
    if f.get("specs"):
        tem = {k.lower() for k, _ in specs}
        specs = f["specs"] + [x for x in specs if x[0].lower() not in {k.lower() for k, _ in f["specs"]}]
    d = {
        "resumo": t["sobre"],
        "specs": specs[:10],
        "compat": " ".join(frase(c) for c in dict.fromkeys(compat))[:600] if compat else (p.get("specs") or "").replace("Compatível: ", "Compatível com "),
        "inclui": inclui[:12],
        "destaques": destaques[:6],
        "dicas": t["dicas"],
        "fab": b.get("fab", ""),
        "fontes": ["arsenalsports.com"],
    }
    if f:
        if f.get("resumo"): d["resumo"] = f["resumo"]
        if f.get("compat"): d["compat"] = f["compat"]
        if f.get("dicas"): d["dicas"] = f["dicas"]
        d["fontes"] = d["fontes"] + f.get("fontes", [])
    if p["sku"] in manual.get("produtos", {}):
        d["destaques"] = []  # o texto revisado já cobre a descrição da Arsenal
        d.update(manual["produtos"][p["sku"]])
    d = {k: v for k, v in d.items() if v not in ("", [], None)}
    d["atualizado"] = date.today().isoformat()
    return d


def main():
    produtos = json.load(open(os.path.join(RAIZ, "produtos.json")))["produtos"]
    bruto = json.load(open(os.path.join(AQUI, "arsenal_bruto.json")))
    manual = json.load(open(os.path.join(AQUI, "manual.json")))
    os.makedirs(SAIDA, exist_ok=True)
    n = 0
    for p in produtos:
        d = gera(p, bruto, manual)
        nome = re.sub(r"[^\w.-]", "_", str(p["sku"])) + ".json"
        caminho = os.path.join(SAIDA, nome)
        try:
            antigo = json.load(open(caminho))
            if {k: v for k, v in antigo.items() if k != "atualizado"} == {k: v for k, v in d.items() if k != "atualizado"}:
                continue  # nada mudou: mantém a data antiga e não gera diff
        except Exception:
            pass
        json.dump(d, open(caminho, "w"), ensure_ascii=False, separators=(",", ":"))
        n += 1
    print(f"{n} arquivos gravados em {SAIDA} ({len(produtos)} produtos)")


if __name__ == "__main__":
    main()
