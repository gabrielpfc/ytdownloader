import os
import random
import re
import asyncio
import edge_tts
from datetime import timedelta
from pydub import AudioSegment
from pydub.utils import which

# ==========================================
# 🔻 LISTA DE TEXTOS (JÁ INCLUÍDA) 🔻
# ==========================================

TEXTOS_CORRIDA =[
    # Bloco 1 - O Padrão Invisível e a Prisão Comportamental
    "Existe um padrão invisível e brutal que governa absolutamente todas as tuas reações, decisões e falhas. A maioria das pessoas passa a vida inteira cega a este código, reagindo por instinto, batendo com a cabeça nas mesmas paredes e destruindo a sua evolução por pura ignorância. O livro apresenta este código através do modelo DISC, mas neste laboratório de forja mental, isto é a tua grelha de combate tático. Tu tens operado no escuro, assumindo que a forma como vês o mundo é a única perspetiva possível. Isso é uma mentira estratégica que te deixa vulnerável, rígido e previsível. Imagina teres nas mãos o mapa genético do comportamento humano. Um mapa que te permite decifrar não apenas o porquê de tu colidires violentamente com certas pessoas e te fundires com outras, mas que te dá a chave para antecipares cada movimento no terreno. O verdadeiro poder não reside na força bruta cega e descontrolada; reside na capacidade de leitura e na adaptação instantânea ao ambiente. Tu precisas de entender com clareza clínica que o teu comportamento é uma ferramenta externa, não a tua identidade definitiva. Tu não és apenas o somatório das tuas reações automáticas programadas no passado. Quando começas a dominar a engrenagem destes quatro estilos comportamentais, tu deixas de ser uma peça sacrificável no tabuleiro e passas a ser o mestre do jogo, capaz de ditar o ritmo da tua própria existência.",

    # Bloco 2 - A Aceitação do Abismo
    "Os pássaros da floresta partilham uma verdade absoluta que o ser humano, cego pelo seu conforto doentio, tenta constantemente esquecer ou subverter: para voar, para dominar os céus, tens primeiro de largar a segurança ilusória do ramo. Tens obrigatoriamente de dar o salto para o desconhecido. O título da obra exige a ação de voar, e a sua premissa é letal na sua simplicidade. Tu estás neste momento agarrado a uma estrutura invisível que te dá uma falsa, morna e apodrecida sensação de segurança. Pode ser uma mentalidade medíocre, um hábito tóxico, ou pior, um traço de personalidade obsoleto que tu usas como escudo de desculpas. Tu dizes com orgulho 'eu sou mesmo assim', como se essa teimosia fosse uma medalha de honra, quando na verdade é a tua corrente mais pesada. Se desejas ascender a níveis de excelência cruéis e inexplorados, se queres subjugar as tuas fraquezas, o primeiro e inegociável requisito é o risco total da queda. Não existe a majestade do voo sem a aceitação fria e corajosa do vazio debaixo dos teus pés. A gravidade vai tentar puxar-te para baixo com uma força brutal, o medo vai uivar e arranhar o teu ouvido interno, mas a aplicação tática da tua vontade tem de obrigar as tuas asas a baterem. A tua velha e conformada identidade tem de morrer agora para que o predador absoluto dos céus possa finalmente assumir o controlo.",

    # Bloco 3 - A Árvore Caída e a Ilusão do Controlo
    "Ouve a ressonância do estrondo no meio da floresta. O cenário descreve o momento caótico em que a normalidade estagnada é estilhaçada num segundo. Começa com um som minúsculo, quase impercetível, um crepitar nos ramos, uma leve vibração nas fundações, e, subitamente, um gigante de mais de sessenta metros despenha-se violentamente contra o solo com um impacto ensurdecedor. A sombra protetora desaparece, o abrigo seguro é esmagado em pó. Fica a saber que é exatamente isto que a vida faz. O teu refúgio de conveniência será sempre, em qualquer momento, um alvo temporário. O caos primitivo não manda um aviso prévio, nem pede permissão para arrombar as portas da tua vida. Um corte financeiro, uma falha de saúde, uma traição impiedosa, a desintegração de um pilar. A questão analítica nunca é sobre se a árvore vai cair ou não; a questão cirúrgica é sobre a forma exata como vais reagir no segundo imediato ao impacto brutal da realidade. O choque espalha ondas de ansiedade paralisante pelos habitantes da floresta. Os fracos retraem-se e petrificam. A poeira asfixia a visão. É exatamente neste milissegundo de fogo cruzado que o teu estilo comportamental base é testado até à quebra. Tu podes escolher ficar a olhar de forma passiva para os escombros, a lamentar a injustiça do universo, ou podes forçar a ativação do teu estado de prontidão letal, procurando focar imediatamente a próxima vantagem tática. O colapso do ambiente é o teste definitivo da tua máquina mental.",

    # Bloco 4 - A Patrulha do Predador (Dominância)
    "Muito acima das nuvens de poeira e destruição, patrulha Dorian, a águia majestosa. A águia recusa-se a aterrar nos escombros para lamentar o destino da árvore desfeita. Ela opera noutra frequência. A águia possui uma visão microscópica, um foco frio e absoluto, e um instinto de responsabilidade agressivo sobre o seu território. Este é o avatar da Dominância pura. Quando a catástrofe se instala, o sexto sentido da águia desencadeia imediatamente uma engrenagem de sobrevivência superior. Ela não se perde em discussões filosóficas sobre como as coisas deveriam ter sido; ela faz uma avaliação nua e crua dos factos e mergulha para aniquilar a raiz do problema. Tu precisas urgentemente de despertar e libertar este predador tático que jaz no teu interior. A águia não consome recursos nem tempo com minúcias dramáticas que não produzem resultados concretos. Ela rasga o vento com agressividade e decisão. Na tua vida real, quando o stress e a dor formarem um cerco em teu redor, tu tens de invocar a frieza magnética de Dorian. Tens de aprender a sobrevoar a tua própria mente de forma desapegada, identificar a ameaça sem pânico e executar a erradicação da fraqueza. A águia domina o espaço aéreo simplesmente porque entende que a hesitação é a mãe da morte. Funde a tua mente a esta atitude inegociável de foco inquebrável.",

    # Bloco 5 - A Fundação Intacta (Estabilidade)
    "Contudo, a mecânica da floresta não sobrevive unicamente através de predadores solitários. Escondidas nos ramos densos e silenciosos, operam as pombas da história. Elas carregam a bandeira da Estabilidade, a constância imperativa, o suporte seguro quando a tempestade descarrega a sua fúria. A águia implacável frequentemente falha em compreender por que razão os outros elementos procuram a pomba, mas a lei de sobrevivência dita que a infraestrutura de qualquer império é a lealdade inquebrável e a coesão pacífica. No momento em que o colapso ecoou, o som harmonioso das pombas cessou brutalmente. O estrondo abalou-lhes a paz. E aqui reside a armadilha fatal da estabilidade: a aversão mórbida ao conflito e o medo paralisante perante a disrupção. Tu deves auditar e extrair a força colossal da pomba — a sua resiliência inabalável, a sua capacidade estóica para absorver a dor, a sua paciência quase geológica — mas és forçado a erradicar a sua tendência para a passividade. A desordem exterior nunca pode retirar-te a autoridade da tua própria voz. A verdadeira, imutável estabilidade não deriva da presença de uma árvore gigantesca que não cai; resulta antes da tua arquitetura emocional profunda que permanece estruturalmente intacta mesmo quando as chamas devoram tudo à volta.",

    # Bloco 6 - A Eletricidade do Caos (Influência)
    "Vira o teu foco para lá do lago, onde o rescaldo da queda colide com a energia vulcânica dos papagaios. Estas aves recusam-se a voar no silêncio contemplativo. Elas são explosões de cor e som constante, movendo-se sob a crença ardente de que o peso da vida tem de ser diluído em alegria coletiva e colaboração. Eles personificam a Influência máxima. A sua tática é lançarem-se ao ar na incerteza e só decidirem a trajetória no meio do caos. A águia solitária olha para baixo, vê esta orgia de sons e processa-a apenas como desordem, um total desperdício de eficiência tática. Mas a águia comete um erro de leitura, pois ali repousa uma arma indispensável: o motor inesgotável para forjar o ânimo. Quando os recursos físicos falham, quando o teu tanque está na reserva e a lógica nua te ordena parar, a frieza isolada não é suficiente. Precisas do fogo caótico do papagaio para incendiar os neurónios. O teu trabalho de extração é capturar a radiação magnética deste arquétipo, mas castrando sumariamente o seu defeito de distração. Tu vais canalizar esta energia absurda para galvanizar o teu compromisso interno, convencendo o cérebro que a agonia não é tortura, mas um processo glorioso. Modula o ruído interno para criar uma frequência afiada de ataque.",

    # Bloco 7 - O Analista Impassível (Consciência)
    "Enquanto a poeira do impacto ainda não assentou completamente, ocultos no nevoeiro da folhagem espessa, os mochos mantêm uma vigilância fria. Eles são a Consciência, a capacidade impessoal de esmagar o erro através do cálculo minucioso. Ao contrário do ataque visceral da águia, do êxtase caótico do papagaio ou da inércia pacífica da pomba, o mocho processa bytes de informação. Ele recusa mover-se por picos de impulso adrenal. Exige leis, rigor estrutural, mapeamento de falhas e uma busca doentia por precisão. Tu deves instalar este módulo no teu próprio cérebro como o teu juiz interno e implacável. No decorrer do teu progresso, quando a dor e a confusão causarem fissuras no teu plano, não podes estar constantemente a invocar apenas a agressividade cega; muitas vezes é crítico utilizar a distância clínica do mocho para identificar a rachadura milimétrica que está a causar a tua falha. No entanto, fica o aviso de que o cancro do analista é a paralisia perante os dados. A perfeição é um escudo para a inação e a verdadeira execução odeia a demora. Integra o processador do mocho, devora os dados do terreno, mas proíbe que a lógica congele o movimento dos teus braços e pernas. Absorve com o olho do mocho, finaliza com a garra da águia.",

    # Bloco 8 - A Fricção Cegante dos Perfils
    "Coloca sob observação atenta a tensão mecânica que se desenrola nos céus da floresta. A águia desliza por cima da zona de influência dos papagaios e sentencia-os de imediato como incompetentes. A sua mente acelerada condena-os: 'Como ousam brincar quando a ordem estrutural está em perigo?'. Este atrito primitivo é exatamente a brecha pelo qual os teus esquemas falham estrepitosamente no mundo real, tanto com as tuas equipas como no conflito civil que deflagra dentro da tua cabeça. Tu estás programado para fuzilar os processos alheios baseando-te na métrica enferrujada do teu próprio espelho. Aquilo que tu designas por prioridade de vida e morte, a pomba experiencia como um ataque selvagem e abusivo; o papagaio ressente-se de um aprisionamento letal; e o mocho condena como uma precipitação primária rumo ao abismo. Despedaça imediatamente a cortina do teu ego julgador. Assim que reconheceres friamente que comportamentos contrários não são declarações de guerra, mas sim a aplicação de táticas variadas para neutralizar a mesma crise, abandonas a postura de vitimização mesquinha. A irritação com o método do outro é um luxo de mentes limitadas. Transforma as incompatibilidades do terreno numa equação manipulável em proveito da tua máquina.",

    # Bloco 9 - A Erradicação da Bolha Segura
    "O espaço harmonioso desta fábula atendia pelo nome suave de 'Lar'. Uma construção irreal e pacífica, uma imensa tenda de complacência psicológica que foi completamente obliterada pelo peso seco da gravidade, quando a base vital da floresta foi abaixo em fracções de segundo. Examina agora com frieza: quantos desses 'Lares' sintéticos tu já teimaste em edificar na base da tua rotina mental? Quantas vezes declaraste, na tua profunda e estúpida ignorância, que o teu conforto económico, os teus hábitos blindados, a tua bolha afetiva, eram invulneráveis às tempestades? A realidade em constante movimento não nutre o mínimo respeito pela tua necessidade infantil de previsibilidade. O pilar vai estalar e partir-se. As métricas confortáveis do teu desempenho vão desaparecer. Se mantiveres a arrogância fixa da águia perante o erro, ou a covardia assustadiça de uma pomba na tempestade, o esfacelamento deste suposto 'Lar' será a tua própria sentença de morte tática. A tua verdadeira e única residência deve ser um estado de paranoia ativa, de vigilância indestrutível e adaptabilidade feroz. Um operador tático não ergue alicerces na madeira de uma árvore moribunda; ele aloja a sua sobrevivência na perícia constante do seu voo em ambientes imprevisíveis.",

    # Bloco 10 - O Ajuste Fino da Central de Comando
    "A genialidade letal que retiras da estrutura DISC revela que o teu cérebro funciona como uma consola de aviação avançada, com vários interruptores e potenciômetros. Dominância, Influência, Estabilidade, Consciência. O calcanhar de Aquiles do civil vulgar reside em prender os seletores com supercola num padrão repetitivo, independentemente do terreno. A tua obrigação tática é seres o maestro cirúrgico destes controlos em plena velocidade. A contingência apanha-te desprevenido no campo de batalha? Aumenta drasticamente a barra da Dominância, esmaga a Estabilidade inerte da espera, aplica a execução imediata. Enfrentas a necessidade de dissecar um falhanço estrutural severo? Potencia os filtros da Consciência, congela o instinto de celebração ilusória e examina os destroços ao nível do milímetro quadrado. Sentes o manto sombrio da apatia mental ou física a minar o passo? Empurra a alavanca da Influência até ao vermelho e inunda a biologia com um diálogo interno enlouquecido e eletrizante. Tu recusas-te veementemente a ser apenas uma caricatura alada fixa num quadrante rígido. Atropelas os teus reflexos animais com a mestria de uma calibragem intelectual implacável.",

    # Bloco 11 - A Morte da Mentira da Identidade Fixa
    "Existe um escudo psicológico barato onde te costumas refugiar em momentos de tensão: a desculpa conformista do 'é o que a minha personalidade dita'. Esta mentira enfadonha deve ser destroçada aqui e agora no asfalto. As tendências pré-fabricadas que governaram os teus sucessos medíocres no passado transformam-se, imediatamente, nos grilhões de aço da tua destruição futura. O mapeamento do teu padrão inato serve como ponto de partida da engenharia reversa para o mudares, não como desculpa para continuares na mesma ruela. Se nasceste com o molde de uma Águia sem remorsos, o teu individualismo que te tirou da base irá atrofiar o teu domínio na escala avançada por alienação total da rede à tua volta. Se envergas a matriz dócil da Pomba fiel, a tua aceitação silenciosa de injustiças manterá o teu pescoço sempre debaixo do jugo alheio, para a eternidade. A tua psique não é um estuque seco impossível de dobrar; é aço em brasa numa fornalha, pedindo as marteladas brutais da adaptação, da tortura e do redirecionamento diário. Recusa enquadrar a tua evolução nas grades de uma taxonomia psicológica estática. Alarga e corrompe o limite daquilo de que te achas capaz.",

    # Bloco 12 - A Frequência Silenciosa vs O Alarme Ensudecedor
    "Observa atentamente o vazio acústico extremo que se instalou entre as pombas durante a crise, em contraste com a onda contínua e turbulenta de vibrações emitidas pelos papagaios em brincadeira. A mecânica da influência ruidosa recruta oxigénio, dita presença ativa e agita as águas inertes, enquanto a técnica do silêncio protetor retém calor, processa a turbulência invisível e fomenta a pacificação curativa no fundo do poço. O ser humano mal treinado rebola constantemente entre o extremismo ruidoso que o desgasta e o silêncio ressentido que o consome vivo. Quando enfrentas um trilho de dor insuportável no processo da tua disciplina, vai existir uma fatia de tempo exata em que necessitarás da vocalização agressiva, da explosão gutural para apagar os detetores da dor. Instantes depois, terás de apelar ao voto absoluto de um silêncio quase monástico para refreares a sangria da tua vitalidade. Um peão apenas atua como a sua corda o puxa, um mestre da guerra psicológica joga cirurgicamente com a intensidade das suas cordas vocais e da sua calma tática conforme a pressão do fogo inimigo o exige.",

    # Bloco 13 - O Radar Antecipatório de Sobrevivência
    "Regressa aos instantes anteriores à derrocada total e estuda Dorian. A ave predatória não detinha a totalidade da fotografia da crise que estava prestes a desenrolar-se, mas uma micro-frequência interior fez tocar os alarmes invisíveis do seu corpo. Este sinal não é magia ou dom divino, é o fruto destilado da vigília perpétua. O seu radar estalou antes mesmo do primeiro estilhaço do tronco. Tu és exigido, pelo imperativo de sobrevivência, a lapidar este mesmo radar para combater a anestesia rotineira da civilização que te rodeia. Não esperes que a corda rebente e que o machado divida o bloco para finalmente ajustares o corpo à agressão. Varre os padrões micro-decadentes das tuas métricas antes que desencadeiem o contágio fatal do falhanço orgânico. O cérebro começa a justificar uma ligeira folga na tua rotina? Deteta o odor rasteiro da complacência. Aciona de forma impetuosa o modo de contra-ataque. Elimina a emboscada na raiz. Tu não geres os desastres, tu dominas a premissa das tendências de desgaste com a antecedência do instinto cirúrgico.",

    # Bloco 14 - A Absorção e Aniquilação dos Padrões
    "Substitui, definitivamente, o perigoso fetiche de te julgares o dono indisputável do quadrante tático ideal, enquanto desvalorizas brutalmente as aves que voam noutra frequência. Uma mente formatada neste narcisismo condena-se a morrer solitária e cega numa armadilha de orgulho. A tua Águia avança insensível, não calibrada pelos sensores cruciais de perigo que pertencem à reserva metodológica do Mocho; a tua Águia derrete num banho de exaustão precoce, despojada da imperturbável constância rítmica suportada pela Pomba. E a mesma agressividade cega deixa o perímetro limpo, mas vazio de suporte humano e da coesão febril incitada pelo Papagaio contagiante. O milagre perturbador na descodificação deste manuscrito mental é que aquilo que tu olhas com o maior desdém é o exato espelho do elo mais quebrado na tua própria armadura. Vira do avesso o desprezo impulsivo que nutres pelos processos das mentes diferentes; em vez de sentires fúria, engole a tua bazófia com ferocidade e faz engenharia reversa das fraquezas contrárias para cimentar as fendas táticas na espinha dorsal da tua capacidade de domínio global. Só então te erguerás invulnerável aos ataques sistémicos.",

    # Bloco 15 - O Abraço Esmagador da Destruição
    "Um pilar orgânico inamovível, a casa primordial que se julgava estar para lá da data de validade, esmagou dezenas de níveis da hierarquia arbórea num único ruído explosivo. Olha agora para dentro da tua própria bolha de mentiras intocáveis. Contempla os tetos falsos que revestem os pilares apodrecidos das tuas ideologias paralisantes. Quando este cataclismo biológico ou financeiro varrer o conforto rasteiro e projetar o caos contra o betão da tua mente, arranca o verniz emocional e foca a lente cínica sobre as fendas resultantes. A poeira esconde um benefício obscuro: o expurgo necessário do espaço morto, a devassa brutal para que os raios implacáveis da adaptação possam forjar músculo novo a partir de material estéril. A tua ignorância teimosa vai ser trucidada e espalhada pelo campo. O verdadeiro choque impulsionador que isto desencadeia na tua maquinaria não é um tempo letárgico para a dor de um adeus, mas antes uma libertação psicótica de adrenalina face à folha em branco da destruição iminente. O impacto desfez os entraves antigos em poeira; agora arranca o solo até o encontrares virgem e edifica, impiedosamente, um obelisco inviolável para substituir o lixo derruído.",

    # Bloco 16 - A Responsabilidade Esmagadora do Perímetro
    "Dorian vasculha os céus do despontar até ao crepúsculo, transportando sobre as próprias asas uma responsabilidade visceral pelo espaço partilhado, desprovido do falso ego que anseia por uma aprovação popular ou palmas rascas por parte de multidões sem estofo. A verdadeira elevação de qualquer perfil requer assumires que o centro de comando não dita simplesmente o alinhamento exclusivo do próprio esqueleto de ossos e artérias, mas impõe por radiação cósmica o termómetro moral e tático de todo o setor em redor. Tomar a soberania e agarrar o comando vertical do voo é um contrato violento onde te responsabilizas diretamente pela atmosfera magnética que injetas nos espaços em que operaste de forma clandestina. Permitires que um nuvem patológica recheada de medíocres hesitações ofusque o radar dos teus aliados equivale a estares a perfurar a resistência defensiva do teu esquadrão com balas amigáveis. Policia e condena veementemente o acesso das opiniões baratas e lamentos enfraquecedores dentro das tuas muralhas invisíveis como a Águia aniquila e oblitera todo o invasor descuidado de entrar na grelha vigiada.",

    # Bloco 17 - A Erradicação do Intervalo Paralisante
    "Nas entrelinhas cinzentas da desgraça, a ave silenciosa congelou as cordas vocais, retendo subitamente o fôlego num impasse biológico atordoante. Experimentar o travão inicial perante o desconhecido ou a catástrofe iminente faz parte do manual natural da nossa biologia primitiva; contudo, conceder a rendição contínua à estagnação petrificante durante segundos a mais é uma sentença ativamente redigida pela inação. Não deves abrigar qualquer autorização de perdoar os travões da tua máquina motriz passada a onda inicial do susto e do estrondo. Desliga inteiramente o mecanismo complacente que sugere um adiamento do raciocínio analítico sob fogo para te acomodares à poeira que não assenta. Ensina forçosamente ao coração em choque que o perigo não atua como sinal absoluto de interrupção motora, antes impõe por força muscular uma aceleração de evasão instantânea. Recusa em absoluto ser a massa informe atada ao peso da tragédia em câmara lenta, estilhaça a inércia fria a murro e atira as garras do instinto num contra-ataque de sobrevivência feroz que faz esquecer num abrir e piscar de olhos a existência letárgica em que se vivia encurralado na estaca inicial.",

    # Bloco 18 - A Forja Suprema da Adaptação Letal
    "Quando o horizonte for forçado a ceder sob o escopo absoluto da expansão da tua mentalidade combativa, esta doutrina do mapeamento comportamental converte-se do nível inofensivo para o degrau da fusão balística em pleno processamento orgânico do teu crânio. Tu transmutas a teoria num reflexo predatório implacável. Avalias de rapina furtiva tal qual a perspicácia calculista do Mocho vigiando o escuro; incendeias o éter motivacional reciclando o fervor estridente da matriz do Papagaio. Emolduras a estrutura inabalável que resiste às lamas das dificuldades com o enraizamento maciço típico da resiliência contínua da Pomba imperturbável; para de seguida arranhares o tecido do espaço no último limite da linha ofensiva, onde desencadeias a pressão bélica, direta, despida de apelos românticos e totalmente predatória da força destrutiva da Águia de guerra. As paredes divisórias da frouxa taxonomia comportamental derretem no atrito constante desta alternância camuflada, transformando os teus feixes operacionais numa massa indecifrável e mortífera pelo oponente não avisado. És o vazio moldável, apto para encaixar impunemente e devorar toda e qualquer exigência.",

    # Bloco 19 - A Aniquilação das Barreiras Desculpatórias
    "Esta dissecação teórica dilacera agora diretamente as ilusões da película frágil que usas, na tua vida miserável de queixas baratas, com a justificação patética de que o mundo externo ou certas individualidades adversas figuram como fortalezas impossíveis de rodear pelo flanco mental. O momento em que cedes e desistes a partir de uma opinião antagónica que rotulaste num impasse estanque reflete somente um suicídio de controlo por vaidade pessoal entranhada. De facto, esta refrega com posições táticas ou comportamentais dissonantes ao teu viés atua como câmara hiperbárica, forjando de forma exaustiva o plano ótimo caso engulas secamente os picos cegos da tua própria arrogância e o preconceito rasca de te sentires ofendido. Conquistando a proeza imaterial que é a mestria dos comportamentos invisíveis em campo de visão livre e impenetrável perante a hostilidade verbal, erradicas de modo decisivo as fronteiras táticas de bloqueio e esmagas o potencial atrito até escravizares a discordância, transformando qualquer energia destrutiva oponente na turbina oculta a favor da progressão brutal das tuas conquistas mais ferozes na vanguarda da competição.",

]
TEXTO_CONGRATS ="A convergência de todos estes fios cruzados colapsa de forma singular no veredicto inflexível que iniciou este mergulho tático: atira a tua carcaça, o teu medo e a tua estrutura gasta do maldito ramo de silêncio e zona neutra, diretamente sobre os confins agressivos do abismo vertical rumo ao arremate imprevisível de tudo. Esta biblioteca de conceitos e matrizes destilada torna-se absolutamente lixo impotente se mantiver a fixação como arquivamento teórico num recanto não oxidado pelo suor real do piso. Exige-se o investimento contínuo, a quebra controlada, a agressividade perante o limite ósseo que grita trégua num tom apavorado de sobrevivência ineficaz. Desliga a corda de escape que ata os pés nos trejeitos programados do teu homem ou mulher de ontem, injeta fluidez maciça onde existiu pedra seca de amadorismo comportamental no confronto de stress real a suceder nas próximas doze horas em campo. Arranca em definitivo o fantasma retido que paralisa os teus músculos à vista cega da destruição da raiz frágil que antes protegia a folhagem cimentada na mediocridade, afasta a desculpa patética do teu radar existencial aguçado e fende as nuvens com uma ferocidade cega rumo a assumir a posse territorial completa. Queima a herança da recusa anterior na propulsão explosiva das garras para lá da margem, domina, abate e apodera-te do teu voo majestoso."
# ==========================================
# 🔺 FIM DA CONFIGURAÇÃO DOS TEXTOS 🔺
# ==========================================

# ----- CONFIGURAÇÃO -----
musicas_dir = r"C:\Users\User\Documents\QA\Runners"
tts_dir = r"C:\Users\User\Documents\QA\TTS"
saida = r"C:\Users\User\Documents\QA\levanta_voo-resumo-com-musica.mp3"

# Configuração da Voz IA
VOZ = "pt-BR-FranciscaNeural"

REDUCAO_DB = -16  # redução da música durante TTS (dB)
REDUCAO_GLOBAL = -7  # redução global da música (dB)
FADE_MS = 2200    # fade in/out em ms

# Inicializa ffmpeg para pydub
AudioSegment.converter = which("ffmpeg")
AudioSegment.ffprobe = which("ffprobe")

# ----- FUNÇÕES AUXILIARES -----
def m_to_ms(minutes): return int(minutes * 60 * 1000)
def fmt_ms(ms): return str(timedelta(seconds=int(ms/1000)))
def limpar_nome(f): 
    nome = os.path.splitext(f)[0]
    nome = re.sub(r"\[.*?\]", "", nome).strip()
    return nome

# ----- FUNÇÃO DE GERAÇÃO DE TTS (ASÍNCRONA) -----
async def gerar_audios_tts(n_slots):
    print("\n🎙️ A gerar áudios com IA...")
    
    # Cria a pasta TTS se não existir
    os.makedirs(tts_dir, exist_ok=True)

    # 1. Gera os áudios da corrida (1.mp3, 2.mp3, etc.)
    for i in range(n_slots):
        # Texto original
        texto_atual = TEXTOS_CORRIDA[i % len(TEXTOS_CORRIDA)]
        
        # --- CORREÇÃO APLICADA AQUI ---
        # Remove asteriscos para evitar que o TTS diga "asterisco"
        texto_limpo = texto_atual.replace("*", "")
        
        nome_arquivo = f"{i + 1}.mp3"
        caminho = os.path.join(tts_dir, nome_arquivo)
        
        print(f"  -> Gerando {nome_arquivo}...")
        communicate = edge_tts.Communicate(texto_limpo, VOZ)
        await communicate.save(caminho)

    # 2. Gera o áudio de Congrats
    caminho_congrats = os.path.join(tts_dir, "Congrats.mp3")
    print("  -> Gerando Congrats.mp3...")
    texto_congrats_limpo = TEXTO_CONGRATS.replace("*", "") # Limpa também o congrats por segurança
    communicate = edge_tts.Communicate(texto_congrats_limpo, VOZ)
    await communicate.save(caminho_congrats)
    
    print("✅ Todos os áudios TTS foram gerados!\n")

# ----- LÓGICA PRINCIPAL -----
def main():
    # ----- INPUT DO UTILIZADOR -----
    try:
        duracao_input = float(input("Digite a duração da corrida em minutos: ").strip())
        intervalo_min = float(input("Digite o intervalo entre cada TTS (em minutos): ").strip())
    except ValueError:
        print("Erro: Digite apenas números válidos (ex: 30 ou 30.5).")
        return

    if duracao_input <= 0 or intervalo_min <= 0:
        raise ValueError("Duração e intervalo devem ser maiores que zero.")

    # ----- CALCULO DOS SLOTES DE TTS -----
    n_slots = int(duracao_input // intervalo_min)
    tts_times_min = [i * intervalo_min for i in range(n_slots)]
    if not tts_times_min:
        tts_times_min = [0.0]

    # Chama a função asíncrona para gerar os áudios ANTES de misturar a música
    asyncio.run(gerar_audios_tts(len(tts_times_min)))

    # ----- DISTRIBUIÇÃO DOS ÁUDIOS GERADOS -----
    tts_timeline = []
    for idx, t_min in enumerate(tts_times_min):
        tts_file = f"{idx + 1}.mp3" # Puxa exatamente os ficheiros que acabaram de ser gerados
        tts_timeline.append((t_min, tts_file))

    # ----- LÓGICA DO CONGRATS E AJUSTE DE DURAÇÃO -----
    congrats_fname = "Congrats.mp3"
    congrats_path = os.path.join(tts_dir, congrats_fname)

    # Define onde o congrats começa (15 segs antes do tempo pedido)
    congrats_start_min = duracao_input - 0.25 

    # Garante que não sobrepõe o último TTS normal
    if tts_timeline:
        last_tts_min = tts_timeline[-1][0]
        if abs(congrats_start_min - last_tts_min) < 0.01:
            congrats_start_min = max(last_tts_min + (1/60.0), 0.0)

    duracao_final_ms = m_to_ms(duracao_input)

    if os.path.exists(congrats_path):
        tts_timeline.append((congrats_start_min, congrats_fname))
        congrats_audio = AudioSegment.from_file(congrats_path)
        congrats_len_ms = len(congrats_audio)
        congrats_start_ms = m_to_ms(congrats_start_min)
        congrats_end_ms = congrats_start_ms + congrats_len_ms
        
        if congrats_end_ms > duracao_final_ms:
            duracao_final_ms = congrats_end_ms + 1000

    tts_timeline.sort(key=lambda x: x[0])

    # ----- MOSTRA RESUMO -----
    duracao_final_min = duracao_final_ms / 60000
    print(f"📋 Duração pedida: {duracao_input:.2f} min")
    print(f"📋 Duração REAL (ajustada): {duracao_final_min:.2f} min")
    print(f"📋 Intervalo entre áudios: {intervalo_min:.2f} min")
    print(f"📋 TTS efetivos a inserir: {len(tts_timeline)}")
    if os.path.exists(congrats_path):
        print(f"🎉 Áudio de comemoração: {fmt_ms(m_to_ms(congrats_start_min))} → {congrats_fname}")
        if duracao_final_ms > m_to_ms(duracao_input):
            print("   ⚠️ AVISO: A música foi estendida para o Congrats tocar até ao fim.")

    # ----- CARREGA MÚSICAS -----
    def load_music_mix(folder, duracao_ms):
        arquivos = [os.path.join(folder, f) for f in os.listdir(folder) 
                    if f.lower().endswith((".mp3", ".wav", ".webm", ".m4a", ".ogg"))]
        if not arquivos:
            raise FileNotFoundError("Nenhuma música encontrada em: " + folder)
        random.shuffle(arquivos)
        mix = AudioSegment.silent(0)
        used = []
        
        while len(mix) < duracao_ms:
            random.shuffle(arquivos)
            for p in arquivos:
                seg = AudioSegment.from_file(p)
                mix += seg
                used.append(p)
                if len(mix) >= duracao_ms:
                    break
                    
        return mix[:duracao_ms], used

    mix, musicas_usadas = load_music_mix(musicas_dir, duracao_final_ms)
    mix = mix.apply_gain(REDUCAO_GLOBAL)

    # ----- INSERÇÃO DOS TTS -----
    corrida = mix
    for minuto, nome in tts_timeline:
        inicio_ms = m_to_ms(minuto)
        caminho = os.path.join(tts_dir, nome)
        if not os.path.exists(caminho):
            print(f"Aviso: {nome} não encontrado. Pulando.")
            continue

        tts_seg = AudioSegment.from_file(caminho)
        fim_ms = inicio_ms + len(tts_seg)
        
        if fim_ms > len(corrida):
            silencio_extra = AudioSegment.silent(duration=(fim_ms - len(corrida)) + 1000)
            corrida += silencio_extra

        fundo = corrida[inicio_ms:fim_ms]
        fundo_reduzido = fundo.apply_gain(REDUCAO_DB).fade_in(FADE_MS//2).fade_out(FADE_MS//2)
        combinado = fundo_reduzido.overlay(tts_seg)
        corrida = corrida[:inicio_ms] + combinado + corrida[fim_ms:]

        print(f"🎧 Inserido {nome:<15} em {fmt_ms(inicio_ms)} (duração {fmt_ms(len(tts_seg))})")

    # ----- EXPORTA RESULTADO -----
    print("\n💾 Exportando áudio final... (isto pode demorar um pouco)")
    corrida.export(saida, format="mp3", bitrate="192k")
    print(f"🏁 Corrida gerada com sucesso → {saida}\n")

    print("🎶 Músicas usadas:")
    musicas_unicas = list(dict.fromkeys(musicas_usadas))
    for i, m in enumerate(musicas_unicas, 1):
        print(f"{i}. {limpar_nome(os.path.basename(m))}")

if __name__ == "__main__":
    main()