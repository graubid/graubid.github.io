#!/usr/bin/env python3
# Builds index.html (ES), en/index.html, pt/index.html from one template.
import os, html

CSS = r"""
:root{--navy:#0F254A;--navy2:#16305C;--green:#2EA670;--green-soft:#E6F4EC;--green-line:#BFE3CF;--paper:#F7F8F6;--white:#FFFFFF;--ink:#0F254A;--ink2:#3C4654;--muted:#6A7179;--line:#DDE2E0;--mint:#BFD8D5}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;font-family:'DM Sans',Arial,sans-serif;color:var(--ink);background:var(--white);line-height:1.5;-webkit-font-smoothing:antialiased}
a{color:inherit}
.wrap{width:min(1120px,100% - 32px);margin-inline:auto}
.eyebrow{font-size:14px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:var(--green);margin:0 0 12px}
h1,h2,h3{margin:0;line-height:1.12;font-weight:700}
h2{font-size:clamp(28px,4vw,40px);max-width:820px}
p{margin:0}
.sub{font-size:clamp(17px,2vw,20px);color:var(--ink2);max-width:760px;margin-top:14px}
section{padding:72px 0}
@media(max-width:640px){section{padding:52px 0}}
header{position:sticky;top:0;z-index:10;background:rgba(255,255,255,.94);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.nav{display:flex;align-items:center;gap:22px;height:68px}
.logo{display:inline-flex;flex-direction:column;text-decoration:none;line-height:1;margin-right:auto}
.logo b{font-size:26px;letter-spacing:-.5px;color:var(--navy)}
.logo i{display:block;height:4px;width:46px;background:var(--green);border-radius:2px;margin-top:4px}
.nav ul{display:flex;gap:24px;list-style:none;margin:0;padding:0}
.nav ul a{text-decoration:none;font-weight:500;color:var(--ink2);font-size:15px}
.nav ul a:hover{color:var(--navy)}
.lang{display:flex;gap:4px;border:1px solid var(--line);border-radius:999px;padding:3px}
.lang a{text-decoration:none;font-size:13px;font-weight:700;letter-spacing:.5px;padding:5px 10px;border-radius:999px;color:var(--muted)}
.lang a[aria-current]{background:var(--navy);color:#fff}
.lang a:hover:not([aria-current]){color:var(--navy)}
.btn{display:inline-block;padding:12px 22px;border-radius:999px;font-weight:700;text-decoration:none;font-size:16px;border:2px solid transparent;transition:.15s}
.btn-green{background:var(--green);color:#fff}
.btn-green:hover{background:#25905f}
.btn-ghost{border-color:var(--mint);color:#fff}
.btn-ghost:hover{background:rgba(255,255,255,.08)}
@media(max-width:860px){.nav ul,.nav .btn{display:none}}
.hero{background:var(--navy);color:#fff;padding:96px 0 88px}
.hero h1{font-size:clamp(38px,6.2vw,72px);letter-spacing:-1px;max-width:900px}
.hero h1 span{color:var(--green)}
.hero .sub{color:var(--mint);font-size:clamp(18px,2.2vw,24px);max-width:720px}
.hero .cta{display:flex;flex-wrap:wrap;gap:14px;margin-top:36px}
.grid{display:grid;gap:22px;margin-top:40px}
.g3{grid-template-columns:repeat(3,1fr)}
.g2{grid-template-columns:repeat(2,1fr)}
@media(max-width:860px){.g3,.g2{grid-template-columns:1fr}}
.card{background:var(--paper);border:1px solid var(--line);border-radius:20px;padding:30px}
.card h3{font-size:22px;margin-bottom:10px}
.card p{color:var(--ink2);font-size:17px}
.card .tag{font-size:13px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:var(--green);margin-bottom:8px}
.alt{background:var(--paper)}
.alt .card{background:#fff}
.steps{display:grid;grid-template-columns:repeat(5,1fr);gap:16px;margin-top:40px}
@media(max-width:960px){.steps{grid-template-columns:repeat(2,1fr)}}
@media(max-width:560px){.steps{grid-template-columns:1fr}}
.step{background:#fff;border:1px solid var(--line);border-radius:18px;padding:24px}
.step .k{font-size:34px;font-weight:700;color:var(--green);line-height:1}
.step h3{font-size:19px;margin:12px 0 8px}
.step p{font-size:15.5px;color:var(--ink2)}
.rules{list-style:none;padding:0;margin:36px 0 0;display:grid;gap:14px;grid-template-columns:repeat(2,1fr)}
@media(max-width:760px){.rules{grid-template-columns:1fr}}
.rules li{display:flex;gap:14px;align-items:flex-start;background:#fff;border:1px solid var(--line);border-radius:16px;padding:20px 22px;font-size:17px;color:var(--ink2)}
.rules li::before{content:"";flex:none;width:12px;height:12px;border-radius:50%;background:var(--green);margin-top:8px}
.note{display:flex;gap:16px;align-items:flex-start;background:var(--green-soft);border:1px solid var(--green-line);border-radius:18px;padding:22px 26px;margin-top:28px;font-size:17px}
.note svg{flex:none;margin-top:3px}
.tbl{width:100%;border-collapse:separate;border-spacing:0;margin-top:36px;border:1px solid var(--line);border-radius:16px;overflow:hidden;font-size:16px}
.tbl th{background:var(--navy);color:#fff;text-align:left;padding:16px 18px;font-weight:700}
.tbl td{padding:16px 18px;border-top:1px solid var(--line);vertical-align:top;color:var(--ink2)}
.tbl td:first-child{font-weight:700;color:var(--navy);white-space:nowrap;width:22%}
.tbl td.when{width:24%}
@media(max-width:760px){
 .tbl thead{display:none}
 .tbl tr{display:block;border-top:1px solid var(--line)}
 .tbl td{display:block;border:0;padding:8px 18px;width:auto}
 .tbl td:first-child{padding-top:18px;font-size:18px}
 .tbl td:last-child{padding-bottom:18px}
 .tbl td.how::before{content:var(--lbl-how);font-weight:700;color:var(--navy)}
 .tbl td.when::before{content:var(--lbl-when);font-weight:700;color:var(--navy)}
}
.final{background:var(--navy);color:#fff}
.final h2{color:#fff}
.final .sub{color:var(--mint)}
.final .cta{display:flex;flex-wrap:wrap;gap:14px;margin-top:32px}
footer{background:#0B1C39;color:var(--mint);padding:28px 0;font-size:14px}
footer .wrap{display:flex;flex-wrap:wrap;gap:12px;justify-content:space-between}
footer a{color:var(--mint)}
"""

ICON_INFO = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#2EA670" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 8v5M12 16h.01"/></svg>'
ICON_STAR = '<svg width="24" height="24" viewBox="0 0 24 24" fill="#2EA670" aria-hidden="true"><path d="M12 2.5l2.9 6.1 6.6.8-4.9 4.6 1.3 6.6L12 17.3l-5.9 3.3 1.3-6.6L2.5 9.4l6.6-.8z"/></svg>'
LI_COMPANY = "https://www.linkedin.com/company/graubid/"

T = {}

T["es"] = dict(
 lang="es", title="GrauBid · Más oportunidades. Mejores propuestas.",
 desc="GrauBid ayuda a empresas tecnológicas a conseguir más contratos: vigilancia de concursos públicos y RFPs, análisis en 72 h y redacción de memorias técnicas y propuestas.",
 lbl_how="Cómo se cobra: ", lbl_when="Cuándo: ",
 nav=[("#servicios","Servicios"),("#proceso","Cómo trabajamos"),("#costes","Costes")],
 cta_nav="Empezar sin coste",
 h1a="Más oportunidades.", h1b="Mejores propuestas.",
 hero_sub="Concursos públicos y ofertas a clientes privados, para empresas tecnológicas que quieren presentarse a más sin parar el negocio.",
 cta1="Empezar con un caso real, sin coste", cta2="Conocer los servicios",
 prob_eb="El problema", prob_h="Las oportunidades existen. Lo que falta es tiempo para encontrarlas y escribirlas bien.",
 prob=[("No te enteras","Concursos y convocatorias se publican y se cierran sin que nadie en la empresa los haya visto."),
       ("No hay tiempo","La propuesta la escribe a última hora quien tiene otro trabajo, entre proyecto y proyecto."),
       ("No puntúa","Se pierden contratos por pocos puntos, o se queda fuera por no llegar al umbral técnico.")],
 serv_eb="Qué hacemos", serv_h="Tres servicios. Tú eliges cuáles.",
 serv_sub="Son independientes. Puedes empezar solo con el vigía, o solo con la redacción de una propuesta concreta.",
 serv=[("1 · Vigía","Te avisamos de lo que encaja","Concursos públicos, convocatorias y RFPs abiertas, filtrados por lo que hace tu empresa. Solo te llega lo que merece una mirada."),
       ("2 · Análisis en 72 h","Te decimos si merece la pena","Qué puntúa, qué piden, qué hay que demostrar y qué posibilidades tienes. Con eso decides presentarte o no."),
       ("3 · Redacción","Escribimos la propuesta","Memoria técnica en lo público, propuesta al cliente en lo privado. Con tus materiales, alineada con lo que puntúa, lista para entregar.")],
 src_eb="De dónde salen las oportunidades", src_h="Fuentes públicas que cualquiera puede ver. El valor está en el filtro.",
 src=[("Concursos públicos","Plataforma de Contratación del Sector Público, con alertas por código de actividad: servicios TI, software, consultoría. Portales autonómicos y locales, y Portugal cuando interese."),
      ("RFPs y ofertas privadas","Portales de proveedores de grandes empresas y licitaciones privadas publicadas. Convocatorias de innovación y ayudas que exigen propuesta técnica. Alta como proveedor en los portales de las empresas que te interesen, para que te inviten.")],
 src_note="En privado no se ve todo: la mayoría de las RFPs llegan por invitación directa y no se publican. Por eso el alta en portales y tu propia red son parte del servicio. Para afinar el filtro nos basta con una presentación o un documento de lo que hacéis.",
 proc_eb="Cómo trabajamos", proc_h="Cinco pasos. En cada uno decides tú.",
 steps=[("Tu negocio","Nos mandas una presentación o documento de lo que hacéis. Te devolvemos nuestras preguntas."),
        ("Filtro","De cada oportunidad que encaja te mandamos una ficha corta: qué es, importe, plazo y por qué encaja. Tú dices sí o no."),
        ("Análisis 72 h","Puntos, requisitos, plazos y nuestra lectura. Decides si vamos."),
        ("Redacción","Escribimos con tus materiales. Revisas y apruebas cada versión."),
        ("Entrega","Documento final listo para presentar. La presentas tú, en tu nombre.")],
 rules_eb="Tus reglas", rules_h="El negocio es tuyo. La propuesta también.",
 rules=["Nada se presenta sin tu aprobación. Tú decides a qué, cuándo y con qué precio.",
        "Acuerdo de confidencialidad firmado antes de ver nada tuyo.",
        "Tus materiales son tuyos. No reutilizamos contenido de un cliente con otro y lo borramos al cerrar cada oferta.",
        "Nunca dos ofertas para el mismo concurso. Y nunca un concurso donde haya conflicto de interés por nuestra parte."],
 sec_eb="Para quién", sec_h="Empresas tecnológicas que venden a cualquier industria.",
 sec=[("Qué hace tu empresa","Software a medida y plataformas. Inteligencia artificial y datos. Ciberseguridad y sistemas. Consultoría y formación TI."),
      ("A quién le vendes","Administración pública, sanidad y educación. Banca, seguros y energía. Industria, automoción y farma. Retail, logística y servicios. Y cualquier otra industria."),
      ("Dónde encaja mejor","Concursos donde la propuesta técnica vale más que el precio. Ofertas privadas donde el cliente compara varias propuestas. Equipos pequeños con picos de trabajo.")],
 cost_eb="Costes", cost_h="Pagas por oportunidad, no por una nómina más.",
 cost_th=["Servicio","Cómo se cobra","Cuándo"],
 cost=[("Vigía","Cuota mensual, sin permanencia.","Cada mes"),
       ("Análisis en 72 h","Precio cerrado por cada pliego analizado. Si después quieres que escribamos la propuesta de ese mismo pliego, lo pagado por el análisis se descuenta del precio de la propuesta.","A la entrega del análisis"),
       ("Redacción","Precio cerrado según tamaño y plazo, acordado antes de empezar. Opcional: parte variable si ganáis.","A la entrega de la propuesta")],
 cost_note="El primer caso, sin coste. Después, cada propuesta con su precio cerrado antes de empezar. Sin sorpresas y sin compromiso a largo plazo.",
 fin_eb="Siguiente paso", fin_h="Empezamos con un caso real, sin coste.",
 fin_sub="Nos mandas una presentación o documento de lo que hacéis. Durante una semana buscamos oportunidades reales que encajen y te mandamos dos o tres con nuestra lectura. Si lo que recibes te convence, acordamos cómo seguir. Si no, no tienes ningún compromiso.",
 fin_cta1="Escríbenos en LinkedIn", fin_cta2="GrauBid en LinkedIn",
 foot="© 2026 GrauBid",
)

T["en"] = dict(
 lang="en", title="GrauBid · More opportunities. Better proposals.",
 desc="GrauBid helps tech companies win more contracts: public tender and RFP monitoring, 72 h bid analysis and proposal writing.",
 lbl_how="How it is billed: ", lbl_when="When: ",
 nav=[("#servicios","Services"),("#proceso","How we work"),("#costes","Pricing")],
 cta_nav="Start at no cost",
 h1a="More opportunities.", h1b="Better proposals.",
 hero_sub="Public tenders and private bids, for tech companies that want to compete for more without stopping the business.",
 cta1="Start with a real case, at no cost", cta2="See the services",
 prob_eb="The problem", prob_h="The opportunities exist. What is missing is time to find them and write them well.",
 prob=[("You never hear about them","Tenders and calls are published and closed without anyone in the company having seen them."),
       ("There is no time","The proposal gets written at the last minute by someone who has another job, between projects."),
       ("It does not score","Contracts are lost by a few points, or the bid is excluded for not reaching the technical threshold.")],
 serv_eb="What we do", serv_h="Three services. You choose which ones.",
 serv_sub="They are independent. You can start with monitoring only, or only with the writing of one specific proposal.",
 serv=[("1 · Watch","We alert you to what fits","Public tenders, calls and open RFPs, filtered by what your company does. Only what deserves a look reaches you."),
       ("2 · 72 h analysis","We tell you if it is worth it","What scores, what is required, what must be proven and what your chances are. With that you decide whether to bid."),
       ("3 · Writing","We write the proposal","Technical submission for public tenders, client proposal for private bids. Built on your materials, aligned with what scores, ready to deliver.")],
 src_eb="Where the opportunities come from", src_h="Public sources anyone can see. The value is in the filter.",
 src=[("Public tenders","Spain's public procurement platform, with alerts by activity code: IT services, software, consulting. Regional and local portals, and Portugal when relevant."),
      ("RFPs and private bids","Supplier portals of large companies and published private tenders. Innovation calls and grants that require a technical proposal. Supplier registration on the portals of the companies you care about, so they invite you.")],
 src_note="In the private sector not everything is visible: most RFPs arrive by direct invitation and are never published. That is why portal registration and your own network are part of the service. To fine tune the filter, a presentation or a document about what you do is enough.",
 proc_eb="How we work", proc_h="Five steps. At each one, you decide.",
 steps=[("Your business","You send us a presentation or document about what you do. We send back our questions."),
        ("Filter","For each opportunity that fits you get a short brief: what it is, value, deadline and why it fits. You say yes or no."),
        ("72 h analysis","Scoring, requirements, deadlines and our reading. You decide whether to go."),
        ("Writing","We write with your materials. You review and approve every version."),
        ("Delivery","Final document ready to submit. You submit it, in your name.")],
 rules_eb="Your rules", rules_h="The business is yours. So is the proposal.",
 rules=["Nothing is submitted without your approval. You decide what, when and at what price.",
        "Non disclosure agreement signed before we see anything of yours.",
        "Your materials are yours. We never reuse one client's content with another, and we delete it when each bid closes.",
        "Never two bids for the same tender. And never a tender where we have a conflict of interest."],
 sec_eb="Who it is for", sec_h="Tech companies selling to any industry.",
 sec=[("What your company does","Custom software and platforms. Artificial intelligence and data. Cybersecurity and systems. IT consulting and training."),
      ("Who you sell to","Public sector, healthcare and education. Banking, insurance and energy. Manufacturing, automotive and pharma. Retail, logistics and services. And any other industry."),
      ("Where it fits best","Tenders where the technical proposal counts more than price. Private bids where the client compares several proposals. Small teams with peaks of work.")],
 cost_eb="Pricing", cost_h="You pay per opportunity, not for one more salary.",
 cost_th=["Service","How it is billed","When"],
 cost=[("Watch","Monthly fee, no minimum term.","Every month"),
       ("72 h analysis","Fixed price per tender analysed. If you then ask us to write the proposal for that same tender, the analysis fee is deducted from the proposal price.","On delivery of the analysis"),
       ("Writing","Fixed price by size and deadline, agreed before starting. Optional: a variable part if you win.","On delivery of the proposal")],
 cost_note="The first case is free. After that, every proposal has a fixed price agreed before starting. No surprises and no long term commitment.",
 fin_eb="Next step", fin_h="We start with a real case, at no cost.",
 fin_sub="You send us a presentation or document about what you do. For one week we look for real opportunities that fit and send you two or three with our reading. If what you receive convinces you, we agree how to continue. If not, there is no commitment.",
 fin_cta1="Message us on LinkedIn", fin_cta2="GrauBid on LinkedIn",
 foot="© 2026 GrauBid",
)

T["pt"] = dict(
 lang="pt", title="GrauBid · Mais oportunidades. Melhores propostas.",
 desc="A GrauBid ajuda empresas tecnológicas a ganhar mais contratos: vigilância de concursos públicos e RFPs, análise em 72 h e redação de memórias técnicas e propostas.",
 lbl_how="Como se cobra: ", lbl_when="Quando: ",
 nav=[("#servicios","Serviços"),("#proceso","Como trabalhamos"),("#costes","Custos")],
 cta_nav="Começar sem custo",
 h1a="Mais oportunidades.", h1b="Melhores propostas.",
 hero_sub="Concursos públicos e propostas a clientes privados, para empresas tecnológicas que querem concorrer a mais sem parar o negócio.",
 cta1="Começar com um caso real, sem custo", cta2="Conhecer os serviços",
 prob_eb="O problema", prob_h="As oportunidades existem. O que falta é tempo para as encontrar e escrever bem.",
 prob=[("Não fica a saber","Concursos e convocatórias são publicados e encerrados sem que ninguém na empresa os tenha visto."),
       ("Não há tempo","A proposta é escrita à última hora por quem tem outro trabalho, entre projeto e projeto."),
       ("Não pontua","Perdem-se contratos por poucos pontos, ou fica-se de fora por não atingir o limiar técnico.")],
 serv_eb="O que fazemos", serv_h="Três serviços. A sua empresa escolhe quais.",
 serv_sub="São independentes. Pode começar só com a vigilância, ou só com a redação de uma proposta concreta.",
 serv=[("1 · Vigilância","Avisamos do que encaixa","Concursos públicos, convocatórias e RFPs abertas, filtrados pelo que a sua empresa faz. Só chega o que merece uma leitura."),
       ("2 · Análise em 72 h","Dizemos se vale a pena","O que pontua, o que pedem, o que é preciso demonstrar e que possibilidades tem. Com isso decide concorrer ou não."),
       ("3 · Redação","Escrevemos a proposta","Memória técnica no público, proposta ao cliente no privado. Com os seus materiais, alinhada com o que pontua, pronta a entregar.")],
 src_eb="De onde vêm as oportunidades", src_h="Fontes públicas que qualquer pessoa pode ver. O valor está no filtro.",
 src=[("Concursos públicos","Plataformas de contratação pública de Espanha e Portugal, com alertas por código de atividade: serviços TI, software, consultoria. Portais regionais e locais."),
      ("RFPs e propostas privadas","Portais de fornecedores de grandes empresas e concursos privados publicados. Convocatórias de inovação e apoios que exigem proposta técnica. Registo como fornecedor nos portais das empresas que lhe interessam, para que o convidem.")],
 src_note="No privado não se vê tudo: a maioria das RFPs chega por convite direto e não é publicada. Por isso o registo em portais e a sua própria rede fazem parte do serviço. Para afinar o filtro basta-nos uma apresentação ou um documento sobre o que fazem.",
 proc_eb="Como trabalhamos", proc_h="Cinco passos. Em cada um, decide a sua empresa.",
 steps=[("O seu negócio","Envia-nos uma apresentação ou documento sobre o que fazem. Devolvemos as nossas perguntas."),
        ("Filtro","De cada oportunidade que encaixa enviamos uma ficha curta: o que é, valor, prazo e porque encaixa. Diz sim ou não."),
        ("Análise 72 h","Pontos, requisitos, prazos e a nossa leitura. Decide se avançamos."),
        ("Redação","Escrevemos com os seus materiais. Revê e aprova cada versão."),
        ("Entrega","Documento final pronto a apresentar. Apresenta-o a sua empresa, em seu nome.")],
 rules_eb="As suas regras", rules_h="O negócio é seu. A proposta também.",
 rules=["Nada é apresentado sem a sua aprovação. Decide a quê, quando e com que preço.",
        "Acordo de confidencialidade assinado antes de ver o que quer que seja.",
        "Os seus materiais são seus. Não reutilizamos conteúdo de um cliente com outro e apagamo-lo ao fechar cada proposta.",
        "Nunca duas propostas para o mesmo concurso. E nunca um concurso onde haja conflito de interesses da nossa parte."],
 sec_eb="Para quem", sec_h="Empresas tecnológicas que vendem a qualquer indústria.",
 sec=[("O que faz a sua empresa","Software à medida e plataformas. Inteligência artificial e dados. Cibersegurança e sistemas. Consultoria e formação TI."),
      ("A quem vende","Administração pública, saúde e educação. Banca, seguros e energia. Indústria, automóvel e farmacêutica. Retalho, logística e serviços. E qualquer outra indústria."),
      ("Onde encaixa melhor","Concursos onde a proposta técnica vale mais do que o preço. Propostas privadas onde o cliente compara várias propostas. Equipas pequenas com picos de trabalho.")],
 cost_eb="Custos", cost_h="Paga por oportunidade, não por mais um salário.",
 cost_th=["Serviço","Como se cobra","Quando"],
 cost=[("Vigilância","Quota mensal, sem fidelização.","Todos os meses"),
       ("Análise em 72 h","Preço fechado por cada caderno de encargos analisado. Se depois quiser que escrevamos a proposta desse mesmo concurso, o valor da análise é descontado do preço da proposta.","Na entrega da análise"),
       ("Redação","Preço fechado segundo dimensão e prazo, acordado antes de começar. Opcional: parte variável se ganhar.","Na entrega da proposta")],
 cost_note="O primeiro caso, sem custo. Depois, cada proposta com o seu preço fechado antes de começar. Sem surpresas e sem compromisso a longo prazo.",
 fin_eb="Próximo passo", fin_h="Começamos com um caso real, sem custo.",
 fin_sub="Envia-nos uma apresentação ou documento sobre o que fazem. Durante uma semana procuramos oportunidades reais que encaixem e enviamos duas ou três com a nossa leitura. Se o que recebe o convencer, acordamos como continuar. Se não, não tem qualquer compromisso.",
 fin_cta1="Escreva-nos no LinkedIn", fin_cta2="GrauBid no LinkedIn",
 foot="© 2026 GrauBid",
)

def e(s): return html.escape(s, quote=False)

def page(t, depth):
    up = "../" * depth
    links = {"es": up + "index.html", "en": up + "en/index.html", "pt": up + "pt/index.html"}
    lang_html = "".join(
        f'<a href="{links[k]}" hreflang="{k}" lang="{k}"' + (' aria-current="page"' if k == t["lang"] else "") + f'>{k.upper()}</a>'
        for k in ("es", "en", "pt"))
    nav_html = "".join(f'<li><a href="{h}">{e(n)}</a></li>' for h, n in t["nav"])
    cards = lambda items: "".join(f'<div class="card"><h3>{e(a)}</h3><p>{e(b)}</p></div>' for a, b in items)
    serv = "".join(f'<div class="card"><p class="tag">{e(a)}</p><h3>{e(b)}</h3><p>{e(c)}</p></div>' for a, b, c in t["serv"])
    steps = "".join(f'<div class="step"><p class="k">{i}</p><h3>{e(a)}</h3><p>{e(b)}</p></div>' for i, (a, b) in enumerate(t["steps"], 1))
    rules = "".join(f'<li>{e(r)}</li>' for r in t["rules"])
    th = "".join(f"<th>{e(x)}</th>" for x in t["cost_th"])
    rows = "".join(f'<tr><td>{e(a)}</td><td class="how">{e(b)}</td><td class="when">{e(c)}</td></tr>' for a, b, c in t["cost"])
    alts = "".join(f'<link rel="alternate" hreflang="{k}" href="https://graubid.es/{"" if k=="es" else k+"/"}">' for k in ("es","en","pt"))
    return f"""<!doctype html>
<html lang="{t['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(t['title'])}</title>
<meta name="description" content="{e(t['desc'])}">
<meta property="og:title" content="{e(t['title'])}">
<meta property="og:description" content="{e(t['hero_sub'])}">
<meta property="og:type" content="website">
<meta property="og:url" content="https://graubid.es/{'' if t['lang']=='es' else t['lang']+'/'}">
{alts}
<link rel="icon" href="{up}favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&display=swap" rel="stylesheet">
<style>{CSS}
:root{{--lbl-how:"{t['lbl_how']}";--lbl-when:"{t['lbl_when']}"}}
</style>
</head>
<body>
<header>
  <div class="wrap nav">
    <a class="logo" href="#top" aria-label="GrauBid"><b>GrauBid</b><i></i></a>
    <ul>{nav_html}</ul>
    <a class="btn btn-green" href="#empezar">{e(t['cta_nav'])}</a>
    <nav class="lang" aria-label="Language">{lang_html}</nav>
  </div>
</header>
<main id="top">
<section class="hero"><div class="wrap">
  <h1>{e(t['h1a'])}<br><span>{e(t['h1b'])}</span></h1>
  <p class="sub">{e(t['hero_sub'])}</p>
  <div class="cta"><a class="btn btn-green" href="#empezar">{e(t['cta1'])}</a><a class="btn btn-ghost" href="#servicios">{e(t['cta2'])}</a></div>
</div></section>
<section id="problema"><div class="wrap">
  <p class="eyebrow">{e(t['prob_eb'])}</p><h2>{e(t['prob_h'])}</h2>
  <div class="grid g3">{cards(t['prob'])}</div>
</div></section>
<section id="servicios" class="alt"><div class="wrap">
  <p class="eyebrow">{e(t['serv_eb'])}</p><h2>{e(t['serv_h'])}</h2><p class="sub">{e(t['serv_sub'])}</p>
  <div class="grid g3">{serv}</div>
</div></section>
<section id="fuentes"><div class="wrap">
  <p class="eyebrow">{e(t['src_eb'])}</p><h2>{e(t['src_h'])}</h2>
  <div class="grid g2">{cards(t['src'])}</div>
  <div class="note">{ICON_INFO}<p>{e(t['src_note'])}</p></div>
</div></section>
<section id="proceso" class="alt"><div class="wrap">
  <p class="eyebrow">{e(t['proc_eb'])}</p><h2>{e(t['proc_h'])}</h2>
  <div class="steps">{steps}</div>
  <p class="eyebrow" style="margin-top:64px">{e(t['rules_eb'])}</p><h2>{e(t['rules_h'])}</h2>
  <ul class="rules">{rules}</ul>
</div></section>
<section id="sectores"><div class="wrap">
  <p class="eyebrow">{e(t['sec_eb'])}</p><h2>{e(t['sec_h'])}</h2>
  <div class="grid g3">{cards(t['sec'])}</div>
</div></section>
<section id="costes" class="alt"><div class="wrap">
  <p class="eyebrow">{e(t['cost_eb'])}</p><h2>{e(t['cost_h'])}</h2>
  <table class="tbl"><thead><tr>{th}</tr></thead><tbody>{rows}</tbody></table>
  <div class="note">{ICON_STAR}<p>{e(t['cost_note'])}</p></div>
</div></section>
<section id="empezar" class="final"><div class="wrap">
  <p class="eyebrow">{e(t['fin_eb'])}</p><h2>{e(t['fin_h'])}</h2><p class="sub">{e(t['fin_sub'])}</p>
  <div class="cta"><a class="btn btn-green" href="{LI_COMPANY}" target="_blank" rel="noopener">{e(t['fin_cta1'])}</a><a class="btn btn-ghost" href="{LI_COMPANY}" target="_blank" rel="noopener">{e(t['fin_cta2'])}</a></div>
</div></section>
</main>
<footer><div class="wrap"><span>{e(t['foot'])}</span><span><a href="{LI_COMPANY}" target="_blank" rel="noopener">linkedin.com/company/graubid</a></span></div></footer>
</body>
</html>
"""

here = os.path.dirname(os.path.abspath(__file__))
for k, depth, path in (("es", 0, "index.html"), ("en", 1, "en/index.html"), ("pt", 1, "pt/index.html")):
    full = os.path.join(here, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(page(T[k], depth))
    print("wrote", path)
