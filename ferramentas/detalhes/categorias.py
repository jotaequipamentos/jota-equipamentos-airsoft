"""Textos por categoria para a seção "Sobre o produto": o que é a peça e dicas de uso.
Chave (grupo, cat, sub) vale antes de (grupo, cat). Escritos à mão, em português, a partir do que é comum no airsoft."""

TEXTOS = {
    # ---------- Magazines ----------
    ("Magazines", "Rifle", "Mid-cap"): {
        "sobre": "Magazine mid-cap para rifle elétrico: alimenta sem precisar dar corda e não faz barulho de BBs soltas. É o tipo mais usado em jogo, com capacidade intermediária.",
        "dicas": ["Leve alguns magazines carregados e um speed loader para recarregar rápido em campo.", "Use BBs limpas e sem rebarba para evitar falha de alimentação."]},
    ("Magazines", "Rifle", "Hi-cap"): {
        "sobre": "Magazine hi-cap para rifle elétrico: leva muitas BBs, mas precisa dar corda na roda da base para alimentar. Ideal para quem quer atirar muito sem trocar de magazine.",
        "dicas": ["Dê corda até sentir a roda firme e repita de tempos em tempos durante o jogo.", "As BBs soltas fazem barulho de chocalho; alguns jogadores preferem mid-cap por isso."]},
    ("Magazines", "Rifle", "Low-cap"): {
        "sobre": "Magazine low-cap para rifle elétrico: capacidade parecida com a do magazine real, sem corda. Usado em jogos milsim e por quem gosta de mais realismo.",
        "dicas": ["Confira as regras do seu campo: alguns jogos milsim exigem low-cap ou mid-cap.", "Carregue com speed loader para ganhar tempo."]},
    ("Magazines", "Rifle", "Drum"): {
        "sobre": "Magazine tipo drum (tambor) de grande capacidade para rifle, muito usado em suporte e jogos longos. Os modelos elétricos ou com som dão corda sozinhos; os manuais têm manivela.",
        "dicas": ["Nos modelos elétricos, verifique o tipo de pilha ou bateria que o drum usa.", "Não force o carregamento além da capacidade indicada."]},
    ("Magazines", "Rifle", "GBBR"): {
        "sobre": "Magazine a gás para rifle blowback (GBBR). O gás guardado no magazine empurra a BB e movimenta o ferrolho, dando o recuo característico.",
        "dicas": ["Abasteça com o gás indicado pelo fabricante (green gas ou CO2) e não exceda a pressão.", "Guarde com um pouco de gás para manter as vedações em bom estado.", "Em dias frios o rendimento do gás cai."]},
    ("Magazines", "Rifle"): {
        "sobre": "Magazine de reposição ou extra para rifle de airsoft. Ter magazines a mais evita recarregar no meio do jogo.",
        "dicas": ["Confira o modelo exato da sua réplica antes de comprar: magazines de plataformas diferentes não se misturam.", "Use BBs limpas e sem rebarba para evitar falha de alimentação."]},
    ("Magazines", "Pistola", "Gás (GBB)"): {
        "sobre": "Magazine a gás para pistola blowback (GBB). O reservatório no magazine guarda o green gas que dispara a BB e movimenta o ferrolho.",
        "dicas": ["Abasteça com o magazine de cabeça para baixo e a válvula firme no bico do gás.", "Guarde com um pouco de gás e lubrifique as vedações com óleo de silicone de vez em quando.", "Em dias frios o rendimento cai; aqueça o magazine na mão antes de usar."]},
    ("Magazines", "Pistola", "CO2"): {
        "sobre": "Magazine para pistola a CO2. Usa cápsula de CO2 de 12 g, que dá mais força e funciona melhor no frio do que o green gas.",
        "dicas": ["Não deixe a cápsula de CO2 no magazine por muito tempo para não forçar a vedação.", "Coloque uma gota de óleo de silicone na ponta da cápsula antes de perfurar."]},
    ("Magazines", "Pistola", "Elétrica (AEP)"): {
        "sobre": "Magazine para pistola elétrica (AEP). Não usa gás: só guarda e alimenta as BBs, já que a pistola funciona com bateria.",
        "dicas": ["Confira o modelo da sua AEP antes de comprar."]},
    ("Magazines", "Pistola"): {
        "sobre": "Magazine extra para pistola de airsoft. Confira o sistema da sua pistola (gás, CO2 ou elétrica) e o modelo antes de comprar.",
        "dicas": ["Magazines de marcas diferentes podem precisar de ajuste, mesmo no mesmo modelo."]},
    ("Magazines", "Shotgun"): {
        "sobre": "Magazine ou cartucho para shotgun de airsoft. Confira o modelo da sua shotgun, porque cada fabricante usa um sistema próprio.",
        "dicas": ["Cartuchos de shotgun costumam disparar 3 ou 6 BBs por vez; confira qual é o da sua réplica."]},
    ("Magazines", "Sniper"): {
        "sobre": "Magazine extra para rifle sniper de airsoft (ferrolho). Cada plataforma (VSR, L96, SSG e outras) tem o seu próprio magazine.",
        "dicas": ["Confira a plataforma exata da sua sniper antes de comprar."]},
    ("Magazines", "Revólver"): {
        "sobre": "Cartuchos ou carregador para revólver de airsoft, para recarregar mais rápido.",
        "dicas": ["Confira o modelo do revólver: os cartuchos não são universais."]},
    ("Magazines", "Peças de magazine"): {
        "sobre": "Peça de reposição para magazine: vedações, válvulas, molas, bases e outros componentes. Resolve vazamento de gás e falha de alimentação sem trocar o magazine inteiro.",
        "dicas": ["Antes de trocar, confira qual peça está com problema (vazamento na válvula, na vedação ou falta de pressão na mola).", "Use óleo de silicone nas vedações ao montar."]},
    ("Magazines",): {
        "sobre": "Magazine para réplica de airsoft. Confira o modelo exato da sua réplica antes de comprar.",
        "dicas": []},

    # ---------- BBs ----------
    ("BBs", "0.20g"): {
        "sobre": "BBs de 0,20 g, o peso mais leve e econômico. Indicadas para réplicas de baixa potência, pistolas de mola e treino.",
        "dicas": ["Em réplicas mais fortes, BBs leves sofrem mais com o vento; considere 0,25 g ou mais.", "Prefira BBs polidas e sem rebarba para não danificar o cano e a borracha do hop-up."]},
    ("BBs", "0.23g e 0.25g"): {
        "sobre": "BBs de 0,23 g a 0,25 g, o peso mais usado em rifles elétricos e pistolas a gás. Bom equilíbrio entre alcance, precisão e preço.",
        "dicas": ["Depois de trocar o peso da BB, reajuste o hop-up.", "Prefira BBs polidas e sem rebarba para não danificar o cano e a borracha do hop-up."]},
    ("BBs", "0.28g e 0.30g"): {
        "sobre": "BBs de 0,28 g a 0,30 g, mais pesadas. Sofrem menos com o vento e têm trajetória mais estável, indicadas para réplicas com upgrade e DMRs.",
        "dicas": ["Precisam de mais hop-up que as BBs leves; reajuste depois de trocar.", "Em réplicas de baixa potência podem perder alcance."]},
    ("BBs", "0.32g a 0.36g"): {
        "sobre": "BBs pesadas de 0,32 g a 0,36 g, para DMRs e réplicas de alta potência. Mais estáveis no vento e com melhor precisão a longa distância.",
        "dicas": ["Exigem réplica com potência e hop-up compatíveis.", "Confira o limite de joules do seu campo."]},
    ("BBs", "0.38g ou mais"): {
        "sobre": "BBs extra pesadas, de 0,38 g para cima, feitas para snipers e réplicas de alta potência. Mantêm a trajetória mesmo com vento.",
        "dicas": ["Exigem sniper ou DMR com potência alta e borracha de hop-up adequada.", "Confira o limite de joules do seu campo."]},
    ("BBs", "Speed loader"): {
        "sobre": "Speed loader (municiador rápido) para encher magazines de BBs em poucos segundos, sem carregar uma por uma.",
        "dicas": ["Confira se o bico do speed loader encaixa no seu tipo de magazine (rifle, pistola ou adaptador)."]},
    ("BBs",): {
        "sobre": "BBs para airsoft. Prefira BBs polidas e de boa qualidade para proteger o cano e o hop-up.",
        "dicas": []},

    # ---------- Tracers ----------
    ("Tracers", "Unidade tracer"): {
        "sobre": "Unidade tracer: ilumina as BBs fluorescentes quando saem do cano, deixando o rastro visível. Ótima para jogo noturno e ambientes fechados.",
        "dicas": ["Funciona com BBs tracer (fluorescentes); BBs comuns não brilham.", "Confira a rosca (14 mm anti-horária é a mais comum) e a fonte de energia."]},
    ("Tracers", "Silenciador com tracer"): {
        "sobre": "Silenciador com tracer embutido: tem o visual de um supressor e ilumina as BBs fluorescentes, que ficam visíveis na trajetória.",
        "dicas": ["Funciona com BBs tracer (fluorescentes).", "Confira a rosca do cano externo da sua réplica (14 mm anti-horária é a mais comum)."]},
    ("Tracers", "Para pistola e SMG"): {
        "sobre": "Tracer compacto para pistola e SMG, que ilumina as BBs fluorescentes no disparo.",
        "dicas": ["Funciona com BBs tracer.", "Confira a rosca e o tamanho do cano da sua pistola ou SMG."]},
    ("Tracers", "Para shotgun"): {
        "sobre": "Tracer para shotgun de airsoft, que ilumina as BBs fluorescentes de cada disparo.",
        "dicas": ["Funciona com BBs tracer.", "Confira o encaixe na sua shotgun."]},
    ("Tracers", "Cronógrafo com tracer"): {
        "sobre": "Unidade que combina tracer e cronógrafo: ilumina as BBs fluorescentes e também mede a velocidade dos disparos.",
        "dicas": ["Útil para conferir o FPS da réplica antes do jogo."]},
    ("Tracers", "Capas e acessórios"): {
        "sobre": "Capa ou acessório para unidade tracer.",
        "dicas": ["Confira o modelo do tracer que você tem antes de comprar."]},
    ("Tracers",): {"sobre": "Acessório tracer para airsoft.", "dicas": ["Funciona com BBs tracer (fluorescentes)."]},

    # ---------- Baterias ----------
    ("Baterias", "LiPo", "7.4V"): {
        "sobre": "Bateria LiPo de 7.4V (2 células). Leve e com boa resposta de gatilho, é a escolha mais comum para rifles elétricos de série.",
        "dicas": ["Carregue só com carregador balanceador próprio para LiPo.", "Não descarregue abaixo de 3,0V por célula e guarde com carga média (cerca de 3,8V por célula).", "Confira o conector (Tamiya ou Deans) e o espaço para a bateria na sua réplica."]},
    ("Baterias", "LiPo", "11.1V"): {
        "sobre": "Bateria LiPo de 11.1V (3 células). Dá mais cadência e resposta, indicada para réplicas com mosfet ou upgrade.",
        "dicas": ["Em réplica sem mosfet, 11.1V pode desgastar os contatos do gatilho; o ideal é instalar um mosfet.", "Carregue só com carregador balanceador próprio para LiPo.", "Confira o conector (Tamiya ou Deans) e o espaço para a bateria na sua réplica."]},
    ("Baterias", "LiPo"): {
        "sobre": "Bateria LiPo para airsoft: leve e com boa resposta de gatilho.",
        "dicas": ["Carregue só com carregador balanceador próprio para LiPo.", "Guarde com carga média (cerca de 3,8V por célula) e longe de calor."]},
    ("Baterias", "Li-Ion"): {
        "sobre": "Bateria Li-Ion: segura a carga por muito tempo parada e aguenta muitos ciclos. Boa para quem joga de vez em quando.",
        "dicas": ["Use carregador compatível com Li-Ion.", "Confira o conector e o espaço para a bateria na sua réplica."]},
    ("Baterias", "LiFe"): {
        "sobre": "Bateria LiFe (LiFePO4): mais segura e resistente que a LiPo, com tensão um pouco menor.",
        "dicas": ["Use carregador com modo LiFe."]},
    ("Baterias", "NiMH"): {
        "sobre": "Bateria NiMH: tecnologia mais antiga e pesada, mas robusta e fácil de carregar. Vem em muitas réplicas de entrada.",
        "dicas": ["Use carregador para NiMH (de preferência com corte automático).", "Não guarde totalmente descarregada."]},
    ("Baterias", "Carregadores e fontes"): {
        "sobre": "Carregador ou fonte para baterias de airsoft. Um bom carregador aumenta a vida útil e a segurança da bateria.",
        "dicas": ["Confira os tipos de bateria suportados (LiPo, Li-Ion, LiFe, NiMH) e o conector de balanceamento.", "Nunca deixe a bateria carregando sem supervisão."]},
    ("Baterias", "Acessórios de bateria"): {
        "sobre": "Acessório para baterias de airsoft: adaptadores, conectores, bolsas de segurança, testadores e similares.",
        "dicas": ["Para carregar LiPo com mais segurança, use uma bolsa anti-chamas."]},
    ("Baterias", "Pilhas para mira e lanterna"): {
        "sobre": "Pilha ou bateria pequena para red dot, lanterna, tracer e outros acessórios.",
        "dicas": ["Retire a pilha do acessório se ele ficar muito tempo sem uso."]},
    ("Baterias",): {"sobre": "Item de energia para airsoft.", "dicas": []},

    # ---------- Canos internos ----------
    ("Canos internos", "AEG"): {
        "sobre": "Cano interno para rifle elétrico (AEG). O diâmetro e o acabamento interno influenciam a precisão e a consistência; canos de precisão (tight bore, de 6,01 a 6,03 mm) costumam melhorar o agrupamento.",
        "dicas": ["Meça o cano original ou confira o comprimento indicado para o seu modelo antes de comprar.", "Combine com uma borracha de hop-up nova para melhor resultado.", "Canos mais justos pedem BBs de boa qualidade."]},
    ("Canos internos", "Pistola e SMG"): {
        "sobre": "Cano interno para pistola ou SMG de airsoft. Um cano de precisão melhora a consistência e o agrupamento dos disparos.",
        "dicas": ["Confira o modelo e o comprimento exato do cano da sua réplica.", "Combine com uma borracha de hop-up nova para melhor resultado."]},
    ("Canos internos", "Sniper"): {
        "sobre": "Cano interno para rifle sniper de airsoft. Em snipers, cano de precisão é um dos upgrades que mais fazem diferença no alcance e no agrupamento.",
        "dicas": ["Confira a plataforma (VSR, L96, SSG e outras) e o comprimento do cano.", "Use BBs pesadas e de boa qualidade para aproveitar a precisão."]},
    ("Canos internos", "GBBR e PTW"): {
        "sobre": "Cano interno para rifle a gás (GBBR) ou PTW. Esses sistemas usam câmaras e comprimentos próprios.",
        "dicas": ["Confira o modelo exato da sua réplica antes de comprar."]},
    ("Canos internos", "Estabilizadores e espaçadores"): {
        "sobre": "Estabilizador ou espaçador de cano interno: centraliza o cano dentro do cano externo, reduzindo vibração e melhorando a consistência.",
        "dicas": ["Confira o diâmetro externo do cano interno e o diâmetro interno do cano externo."]},
    ("Canos internos", "Kits com cano externo"): {
        "sobre": "Kit com cano externo e interno, para trocar o conjunto de uma vez.",
        "dicas": ["Confira o modelo exato da sua réplica antes de comprar."]},
    ("Canos internos",): {"sobre": "Cano interno de airsoft.", "dicas": ["Confira o comprimento e o modelo da sua réplica."]},

    # ---------- Peças internas ----------
    ("Peças internas", "Gearbox", "Gearbox completa"): {
        "sobre": "Gearbox completa e montada, com engrenagens, pistão, cilindro e mola. Serve para substituir uma gearbox quebrada ou como base para upgrade sem comprar peça por peça.",
        "dicas": ["Confira a versão (V2, V3 e outras) e o lado da fiação (frontal ou traseira) da sua réplica.", "Após instalar, acerte a altura do motor (pinhão) para evitar ruído e desgaste."]},
    ("Peças internas", "Gearbox", "Carcaça"): {
        "sobre": "Carcaça de gearbox (shell): a caixa onde ficam engrenagens, pistão e cilindro. Carcaças reforçadas aguentam molas mais fortes.",
        "dicas": ["Confira a versão (V2, V3 e outras) e o tipo de bushing (7, 8 ou 9 mm)."]},
    ("Peças internas", "Gearbox", "Parafusos e clamps"): {
        "sobre": "Parafusos ou clamps para gearbox e montagem interna.",
        "dicas": ["Não aperte demais parafusos em carcaças de liga leve."]},
    ("Peças internas", "Gearbox"): {
        "sobre": "Peça de gearbox para rifle elétrico (AEG).",
        "dicas": ["Confira a versão da gearbox (V2, V3 e outras) da sua réplica."]},
    ("Peças internas", "Engrenagens", "Jogos"): {
        "sobre": "Jogo de engrenagens (bevel, spur e sector). A relação (ratio) define o equilíbrio entre cadência e força: ratios baixos (13:1 a 16:1) dão mais cadência, e ratios altos (18:1 para cima) aguentam molas mais fortes.",
        "dicas": ["Escolha o ratio de acordo com o motor e a mola que você usa.", "Faça o shim (ajuste de folga) ao instalar, para as engrenagens durarem mais."]},
    ("Peças internas", "Engrenagens"): {
        "sobre": "Engrenagem avulsa para gearbox de AEG.",
        "dicas": ["Engrenagens costumam ser trocadas em jogo; confira o ratio do restante do conjunto.", "Faça o shim (ajuste de folga) ao instalar."]},
    ("Peças internas", "Buchas, rolamentos e shims"): {
        "sobre": "Buchas, rolamentos ou shims para gearbox: sustentam as engrenagens e ajustam a folga entre elas. Um bom shim deixa a gearbox mais silenciosa e durável.",
        "dicas": ["Confira o diâmetro (7, 8 ou 9 mm) que a sua carcaça usa."]},
    ("Peças internas", "Cilindro e cabeça"): {
        "sobre": "Cilindro ou cabeça de cilindro para AEG. O volume do cilindro precisa combinar com o comprimento do cano para ter boa eficiência de ar.",
        "dicas": ["Para canos curtos use cilindros com furo (ported); para canos longos, cilindros cheios.", "Lubrifique com graxa de silicone e confira a vedação."]},
    ("Peças internas", "Pistão e cabeça"): {
        "sobre": "Pistão ou cabeça de pistão para AEG. Um pistão bem vedado e resistente garante compressão constante e mais durabilidade com molas fortes.",
        "dicas": ["Confira o ângulo de ataque entre o pistão e o setor para não desgastar os dentes.", "Use graxa de silicone no o-ring."]},
    ("Peças internas", "Nozzles e tappet"): {
        "sobre": "Nozzle ou tappet plate. O nozzle leva o ar até a BB e precisa ter o comprimento certo para o seu modelo; o tappet empurra o nozzle no ciclo.",
        "dicas": ["Confira o comprimento do nozzle indicado para a sua réplica (M4, AK, G36 e outras usam tamanhos diferentes)."]},
    ("Peças internas", "Molas e guias", "Molas"): {
        "sobre": "Mola principal para AEG ou sniper. A mola define a potência (FPS/joules) da réplica.",
        "dicas": ["Confira o limite de FPS ou joules do campo onde você joga antes de trocar.", "Molas mais fortes exigem gearbox e motor preparados."]},
    ("Peças internas", "Molas e guias", "Guias"): {
        "sobre": "Guia de mola para AEG ou sniper. Guias com rolamento deixam a mola girar livre e reduzem o desgaste.",
        "dicas": ["Confira se a guia é para gearbox com troca rápida de mola (quick change)."]},
    ("Peças internas", "Molas e guias"): {"sobre": "Mola ou guia para réplica de airsoft.", "dicas": []},
    ("Peças internas", "Hop-up", "Borrachas"): {
        "sobre": "Borracha de hop-up (bucking): dá o giro (backspin) que faz a BB subir e ir mais longe. Trocar uma borracha gasta ou usar uma de melhor qualidade melhora muito o alcance e a precisão.",
        "dicas": ["Borrachas mais duras (70° a 80°) são para réplicas mais fortes; as mais macias (50° a 60°) para baixa potência e frio.", "Limpe o cano e a borracha antes de instalar e reajuste o hop-up depois."]},
    ("Peças internas", "Hop-up", "Câmaras"): {
        "sobre": "Câmara de hop-up: segura o cano interno e a borracha e regula o hop-up. Câmaras de metal ou com regulagem fina dão ajuste mais preciso e estável.",
        "dicas": ["Confira o modelo da réplica (M4, AK e outras) e o tipo de borracha compatível."]},
    ("Peças internas", "Hop-up", "Braços, nubs e tensores"): {
        "sobre": "Peça de ajuste do hop-up (braço, nub ou tensor) que pressiona a borracha sobre a BB. Um bom nub deixa o efeito mais regular.",
        "dicas": ["Confira se a peça é para o mesmo modelo de câmara e borracha."]},
    ("Peças internas", "Hop-up"): {
        "sobre": "Peça do sistema de hop-up, que dá o giro na BB para aumentar o alcance.",
        "dicas": ["Confira a compatibilidade com a câmara e a borracha da sua réplica."]},
    ("Peças internas", "Motores"): {
        "sobre": "Motor para rifle elétrico. Motores de alta rotação (high speed) aumentam a cadência; motores de torque (high torque) puxam molas mais fortes com resposta melhor.",
        "dicas": ["Confira o tipo de eixo: long (M4, AK, G3), medium (G36) ou short (P90, UMP e similares).", "Ajuste a altura do motor (pinhão) depois de instalar."]},
    ("Peças internas", "Mosfets e fiação"): {
        "sobre": "Mosfet, gatilho eletrônico ou fiação para AEG. O mosfet protege os contatos do gatilho, melhora a resposta e, nos programáveis, permite modos como burst e freio ativo. Fios de baixa resistência entregam mais corrente ao motor.",
        "dicas": ["Confira o lado da fiação (frontal ou traseira) e a versão da gearbox.", "A instalação pede solda; se não tiver prática, procure um técnico."]},
    ("Peças internas", "Gatilho, seletor e travas"): {
        "sobre": "Peça do conjunto de gatilho, seletor ou trava. Reposição para quando o gatilho falha, o seletor não trava ou a peça quebrou.",
        "dicas": ["Confira o modelo exato da réplica e a versão da gearbox."]},
    ("Peças internas", "HPA"): {
        "sobre": "Peça para sistema HPA (ar comprimido): engines, reguladores, mangueiras e conexões. HPA dá cadência e potência consistentes e ajustáveis.",
        "dicas": ["Confira a rosca e o padrão de conexão (por exemplo, US/Foster) do seu sistema.", "Respeite a pressão máxima de cada componente."]},
    ("Peças internas", "O-rings"): {
        "sobre": "O-rings (anéis de vedação) de reposição, para resolver vazamento de ar ou gás.",
        "dicas": ["Lubrifique com óleo ou graxa de silicone ao instalar."]},
    ("Peças internas", "Kits de upgrade"): {
        "sobre": "Kit de upgrade com várias peças internas que trabalham juntas para melhorar o desempenho.",
        "dicas": ["A instalação exige desmontar a gearbox; se não tiver prática, procure um técnico."]},
    ("Peças internas",): {"sobre": "Peça interna de reposição ou upgrade para réplica de airsoft.", "dicas": ["Confira o modelo exato da sua réplica antes de comprar."]},

    # ---------- AAP01 ----------
    ("Peças AAP01",): {
        "sobre": "Peça para a Action Army AAP01, pistola a gás muito usada em speedsoft e personalização. Boa parte dessas peças também serve na AAP01C, que é a versão compacta.",
        "dicas": ["Confira se a peça é para AAP01, AAP01C ou ambas.", "Algumas peças de upgrade exigem ajuste fino; se não tiver prática, procure um técnico."]},
    ("Peças AAP01", "Magazines e HPA"): {
        "sobre": "Magazine ou adaptador HPA para a Action Army AAP01.",
        "dicas": ["Abasteça os magazines com green gas e guarde com um pouco de gás.", "Em HPA, use regulador com pressão adequada à pistola."]},
}


def texto(grupo, cat, sub):
    for k in ((grupo, cat, sub), (grupo, cat), (grupo,)):
        if k in TEXTOS:
            return TEXTOS[k]
    return {"sobre": "", "dicas": []}
