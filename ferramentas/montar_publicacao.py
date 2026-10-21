#!/usr/bin/env python3
"""Monta a versão da vitrine para publicar como artifact.

Uso:  python3 montar_publicacao.py <pasta de saída>
O artifact não carrega fotos de outros sites nem centenas de arquivos soltos, então as miniaturas
de img/ são juntadas em folhas (fotos/folha-N.webp, 100 fotos cada) e cada produto passa a apontar
para a sua posição na folha. Publique <saída>/index.html com as folhas como arquivos de apoio.
"""
import json, os, re, sys
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
COL, LIN, LADO = 10, 10, 240

saida = sys.argv[1]
os.makedirs(os.path.join(saida, "fotos"), exist_ok=True)
t = open(os.path.join(AQUI, "index.html"), encoding="utf-8").read()
fotos = re.findall(r'"img": "(img/\d+\.webp)"', t)
unicas = list(dict.fromkeys(fotos))
pos = {}
folhas = []
for n in range(0, len(unicas), COL * LIN):
    lote = unicas[n:n + COL * LIN]
    lin = (len(lote) + COL - 1) // COL
    folha = Image.new("RGB", (COL * LADO, lin * LADO), (255, 255, 255))
    for i, rel in enumerate(lote):
        im = Image.open(os.path.join(AQUI, rel)).convert("RGB")
        im.thumbnail((LADO, LADO))
        folha.paste(im, ((i % COL) * LADO + (LADO - im.width) // 2, (i // COL) * LADO + (LADO - im.height) // 2))
        pos[rel] = (len(folhas), i, COL, lin)
    nome = f"fotos/folha-{len(folhas)}.webp"
    folha.save(os.path.join(saida, nome), "WEBP", quality=70, method=6)
    folhas.append(nome)

t = re.sub(r"<!-- GA:INICIO.*?<!-- GA:FIM -->\n", "", t, flags=re.S)  # o artifact bloqueia scripts de fora
t = re.sub(r'"img": "(img/\d+\.webp)"', lambda m: '"spr": ' + json.dumps(list(pos[m.group(1)])), t)
t = t.replace("const PRODUTOS = [", f"const SPRITES = {json.dumps(folhas)};\nconst PRODUTOS = [", 1)
open(os.path.join(saida, "index.html"), "w", encoding="utf-8").write(t)
print(f"{len(unicas)} fotos em {len(folhas)} folhas; página {os.path.getsize(os.path.join(saida, 'index.html')) // 1024} KB")
