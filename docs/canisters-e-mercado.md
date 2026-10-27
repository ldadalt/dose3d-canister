# Canisters de irradiação de sangue e o mercado

Consulta em 27 de outubro de 2026. Este arquivo lista os recipientes que os irradiadores de sangue de fato usam, com o diâmetro, a altura e o volume publicados, e descreve para onde o parque instalado está indo.

Os números de dimensão vêm de folheto do fabricante ou de artigo que mediu o equipamento. O volume nominal do folheto e o cilindro calculado com o diâmetro e a altura publicados nem sempre fecham. Para um mapa de dose, vale o certificado de dosimetria da unidade, não uma conta feita em cima do catálogo. A dose clínica de cada país está em [referencias-irradiacao-de-sangue.md](referencias-irradiacao-de-sangue.md).

Não há censo público de “qual modelo é o mais vendido”. O que dá para afirmar é quais geometrias dominam a base instalada, quais aparecem nas compras novas e em que país cada uma é o caso típico.

## Três recipientes, não um canister só

O nome canister cobre três máquinas diferentes.

| Família | O que se move | Forma do volume | Onde ainda é o caso comum |
| --- | --- | --- | --- |
| Cilindro alto no próprio eixo | o canister gira entre fontes fixas de Cs-137 | alto e estreito | base instalada de gama: Gammacell e IBL 437C |
| Cilindro baixo, parado | nada gira; dois tubos de raios X ficam em oposição | largo e baixo | compra nova da Best Theratronics, o Raycell Mk2 |
| Canister de 1 L em carrossel | os canisters orbitam o tubo; o conteúdo não tomba | seis volumes de 1 L | compra nova da Rad Source, o RS 3400 |
| Bandeja | a bandeja entra na câmara; não é um cilindro alto | disco de dezenas de milímetros de espessura | Japão: Sangray nos centros, MBR nos hospitais mais antigos |

A simetria azimutal que este repositório usa vale para a primeira linha. Nas outras, girar um plano diametral em volta do eixo descreve uma máquina que não é a que está na sala.

## Cilindro alto que gira

É o irradiador de Cs-137 autoblindado. Fontes fixas, canister de alumínio que gira no eixo, tempo corrigido pela meia-vida. O mapa típico tem o centro como referência, a parede mais quente e as tampas mais frias. É a geometria do preset deste pacote.

| Modelo | Diâmetro interno | Altura interna | Volume publicado | Bolsas por ciclo, no folheto ou no artigo | Uniformidade publicada com 25 Gy no centro |
| --- | --- | --- | --- | --- | --- |
| Gammacell 3000 Elan, Best Theratronics | 124 mm | 194 mm | 2,34 L | 4 bolsas de 300 mL | 19 / 25 / 33 Gy (1,7 : 1) |
| Gammacell 1000 Elite, Best Theratronics | 80 mm | 164 mm | 0,824 L | 1 bolsa de 300 mL | 21 / 25 / 29 Gy (1,4 : 1) |
| IBL 437C, CIS / ORIS | 130 mm | 290 mm | 3,8 L | artigos descrevem 2 ou 3 bolsas de 300 mL na carga medida | não há um par único de mínimo e máximo de catálogo; o mapa é da unidade |

Fontes:

- Best Theratronics, folheto Gammacell 1000 Elite / 3000 Elan, revisão citada como 16 de março de 2023: https://www.theratronics.ca/PDFs/03_16_2023_BT_MBTS_8005_GC1000E_3000E_brochure.pdf
- IBL 437C, diâmetro, altura e 3,8 L repetidos em dois trabalhos independentes. Bogner e Häring, *Strahlentherapie und Onkologie*, 1998, dosimetria de uma unidade com duas fontes: https://epub.uni-regensburg.de/23393/1/BognerL_DosimterieBlutbestrahlung_StrahlentherOnkol1998.pdf. Centro da Cruz Vermelha da Tailândia, mapeamento com Fricke: https://inis.iaea.org/records/dp4da-mq312/files/33055351.pdf. Descrição de uma unidade turca, com as mesmas cotas: https://onkoloji.dergisi.org/text.php?id=732

O cilindro de 124 mm por 194 mm dá 2,34 L, e o de 80 mm por 164 mm dá 0,824 L. Nesses dois o folheto e a conta fecham. O de 130 mm por 290 mm dá cerca de 3,85 L; os artigos arredondam para 3,8 L.

O 3000 Elan é o canister grande da Best. O 1000 Elite é o pequeno, de uma bolsa, com uniformidade mais apertada. Os dois ainda constam do catálogo de 2023. A atividade típica publicada é 1 300 Ci (48,1 TBq) ou 2 200 Ci (81,4 TBq); o 1000 Elite também tem um modelo de 575 Ci. A taxa no centro, no 3000 Elan, é 4,5 ou 7,4 Gy/min, e o tempo para 25 Gy no centro é 5,6 ou 3,4 min, conforme o modelo da fonte. O mesmo folheto publica o outro ponto de operação, o de mínimo 25 Gy em todo o canister: no 3000 Elan isso fica 25 / 33 / 43,5 Gy. É o mesmo desenho de campo, com o timer mais longo. O ponto 19 / 25 / 33 cumpre o FDA e não cumpre o EDQM.

O IBL 437C é o outro cilindro alto que a literatura de serviço encontra na Europa, na Ásia e na América Latina. É mais alto que o 3000 Elan (290 mm contra 194 mm) e um pouco mais largo. A rotação existe; a velocidade não é um número único de catálogo. Um artigo alemão mediu 28 rpm e um turco descreveu 18 rpm. A carga de fontes também varia: a unidade de Regensburg tinha duas fontes, a turca três. Tratar “IBL 437C” como um mapa só, copiado de um certificado, erra a unidade vizinha.

Esta é a base instalada histórica. Não é o que os programas de substituição estão comprando.

## Cilindro baixo, parado, entre dois tubos

O Raycell Mk2, da mesma Best Theratronics, troca a fonte de Cs-137 por dois tubos de raios X opostos. O canister fica parado no meio. O folheto não descreve rotação. A uniformidade vem dos dois feixes em cone, não da média azimutal de um giro.

| Versão no folheto de 2023 | Diâmetro publicado | Altura publicada | Volume nominal | Bolsas por ciclo | 25 Gy no centro | 25 Gy no mínimo |
| --- | --- | --- | --- | --- | --- | --- |
| 2,0 L | 167 mm | 97 mm | 2,0 L | 4 de 300 mL, ou 2 de 600 mL | cerca de 20 a 30 Gy (1,5 : 1), em cerca de 2 min | cerca de 25 a 37,5 Gy, em cerca de 3,2 min |
| 5,0 L | 240,5 mm | 119,5 mm | 5,0 L | 6 de 300 mL | cerca de 21,4 a 35,3 Gy (1,65 : 1), em cerca de 5,5 min | cerca de 27,3 a 45,5 Gy, em cerca de 6 min |

Fonte: https://www.theratronics.ca/PDFs/11_13_2023_BT_MBTS_8014_RCMK2_v13_2023.pdf. A página do produto confirma os dois tubos e o canister no centro: https://www.theratronics.ca/product_raycell_mk2.html. Um folheto anterior do grupo, de janeiro de 2022, chama a versão grande de 4,8 L e cita 5,8 Gy/min no centro. O folheto de 2023, usado aqui, diz 5,0 L e 5,0 Gy/min. É revisão de catálogo, não duas máquinas medidas lado a lado.

O cilindro de 167 mm por 97 mm dá cerca de 2,12 L, e o de 240,5 mm por 119,5 mm dá cerca de 5,4 L. O volume nominal do folheto é menor. Diâmetro e altura podem incluir parede, ou o volume útil pode ser o do miolo. Não dá para gravar essas cotas como interno varrido sem o desenho da unidade.

O ponto de 25 Gy no centro do canister de 2,0 L desce a cerca de 20 Gy. Isso passa no critério americano de 15 Gy na borda e falha onde o mínimo em qualquer ponto é 25 Gy. O fabricante já publica o outro timer.

## Carrossel de seis canisters de 1 L

O RS 3400, da Rad Source Technologies, é o irradiador de raios X que mais aparece nas trocas recentes de Cs-137, inclusive no Brasil. Um tubo Quastar fica no centro. Até seis canisters orbitam esse tubo. A patente que o fabricante cita gira o canister em volta da fonte sem tombar o conteúdo. Não é o giro no próprio eixo do Gammacell.

O que o fabricante publica sobre o recipiente:

- volume interno de 1 L; com os insertos de apoio, cerca de 868 mL
- material atual em policarbonato ABS; a geração anterior era fibra de carbono
- razão de uniformidade cerca de 1,6, e cerca de 1,35 com os insertos
- um ciclo leva até 6 bolsas de 600 mL, ou 6 plaquetas de 500 mL, ou 18 seringas de 60 mL
- tempo de ciclo para 25 Gy no centro, inferior a 5 min; a taxa citada no folheto fica entre 5,5 e 6,5 Gy/min

Diâmetro e altura do canister de 1 L não estão no folheto público consultado. A página que o próprio folheto anuncia como “dimensions on next page” traz a foto do canister de fibra de carbono, do porta-seringa e do fantoma, sem cota. Um revendedor lista o acessório “4 inch fiber canisters”; isso é nome de peça, não diâmetro interno mais altura. Sem as duas cotas, este pacote não tem um cilindro para clipar.

Fontes: folha do canister, https://labex.dk/wp-content/uploads/Rad-Source-Product-Sheet_RS-3400-Canister-1.pdf. Folheto do equipamento, https://radsource.com/wp-content/uploads/Blood-Brochure-International-1.pdf e a revisão de abril de 2026, https://radsource.com/wp-content/uploads/Blood-Brochure-International-Rev-5-042026.pdf. Página do produto: https://radsource.com/products/rs-3400-blood-irradiator/.

O folheto internacional separa um ponto “FDA” (15 Gy no mínimo, 25 Gy no centro, 50 Gy no máximo) de um ponto “EDQM / Reino Unido” (25 Gy no mínimo, 50 Gy no máximo). A página do produto, na consulta de 2026, escreve 25 Gy de mínimo e 50 Gy de máximo também na linha dos Estados Unidos. Isso é texto de fabricante, e as duas páginas não dizem a mesma coisa. O critério americano continua o do memorando de 1993, no outro documento desta pasta. O próprio fabricante avisa que a dose da borda muda com o ponto de operação escolhido.

A frase “o irradiador de raios X número um do mundo” é capa de folheto da Rad Source. Não é contagem de parque.

## Bandeja, o caso japonês

No Japão a irradiação é quase universal e o recipiente usual não é o cilindro alto. A Cruz Vermelha descreve o processo atual com irradiador de raios X dedicado, na faixa de 15 Gy a não mais que 50 Gy: https://www.jrc.or.jp/mr/blood_product/safety/irradiation/. A diretriz VI diz que, em muitos centros, o botão de 15 Gy é o mínimo em todo o campo, e o produto fornecido fica em geral até cerca de 25 Gy.

O aparelho de sangue corrente com registro japonês é o SANGRAY. Dois tubos em oposição, na vertical. A bandeja grande publicada é de 350 mm de diâmetro por 70 mm de espessura, e cabe a sete bolsas de 400 mL. Há uma bandeja mais fina: produto com menos de 35 mm de espessura vai nela. O registro na PMDA está com a Fujifilm Medical (aprovação 22700BZX00036000; instruções revisadas em julho de 2024). O 510(k) americano K172087, de 27 de outubro de 2017, foi submetido pela Hitachi. O número do painel e o corte da bandeja estão na seção seguinte.

Fontes: ficha de produto, https://www.eizojoho.co.jp/medicaldevice/detail/105872. Instruções notificadas à PMDA: https://www.pmda.go.jp/PmdaSearch/kikiDetail/ResultDataSetPDF/671001_22700BZX00036000_A_03_01. 510(k): https://fda.innolitics.com/device/K172087.

Antes do SANGRAY, o irradiador de hospital no Japão era a série Hitachi MBR, em especial o MBR-1520. Tubo único de 150 kV e 20 mA, filtro de 1 mm de alumínio, bolsas num balde sobre a mesa, espessura máxima publicada de 60 mm no MBR-1520A-TW, campo da ordem de 430 mm de diâmetro. O gradiente que importa é o da espessura da pilha, não o raio de um cilindro de 124 mm. A série MBR que a Hitachi Power Solutions lista hoje é de pesquisa (animal, célula, planta), sucessora do MBR-1520R, e não é o irradiador de sangue.

## Outros de raios X que entram na mesma conversa

O levantamento de 2020 do Sandia, no programa de alternativas da NNSA, nomeia seis aparelhos de raios X então aprovados nos Estados Unidos, na União Europeia ou na China: Best Theratronics Mk1 e Mk2, Rad Source RS 3400, Hitachi Sangray, Gilardoni RadGil, Actemium NDT BloodXrad e Livzon X-Rad 3000. https://www.osti.gov/servlets/purl/1888648

O RadGil 2, da Gilardoni, é o que mais se parece com um canister girante do lado dos raios X. O folheto padrão traz dois canisters de plástico, de três e de quatro compartimentos, até seis bolsas ou 1 800 mL, e diz que 25 Gy levam cerca de 5 minutos. A câmara, com o canister removido, aceita uma amostra de até 29 cm de diâmetro e 29 cm de altura. O folheto consultado não publica o diâmetro interno do canister de sangue. https://www.gamma-medical.info/fileadmin/user_upload/Bilder/Dateien/Radgil2_data_sheet.pdf

BloodXrad e X-Rad 3000 aparecem nessa lista de 2020. Não achei, nesta consulta, cota de canister comparável às da tabela acima, então ficam de fora do desenho.

Acelerador linear e bomba de cobalto de radioterapia não têm canister. A Portaria brasileira os admite quando o serviço não tem irradiador de células. É outra geometria, de feixe externo, e outro controle de tempo e de temperatura da bolsa.

## Comparação na mesma escala

As seis cotas completas, postas no mesmo cilindro. O volume da coluna “cilindro” é π r² h a partir do diâmetro e da altura publicados. O volume nominal é o que o fabricante ou o artigo declara. Onde os dois divergem, o desenho usa o diâmetro e a altura, e o litro nominal fica como o fabricante o escreveu.

| Modelo | Ø mm | Altura mm | Altura / Ø | Cilindro | Nominal | Contra o 3000 Elan, Ø / altura / volume |
| --- | --- | --- | --- | --- | --- | --- |
| Gammacell 1000 Elite | 80 | 164 | 2,05 | 0,82 L | 0,824 L | 0,65 / 0,85 / 0,35 |
| Gammacell 3000 Elan | 124 | 194 | 1,56 | 2,34 L | 2,34 L | 1 / 1 / 1 |
| IBL 437C | 130 | 290 | 2,23 | 3,85 L | 3,8 L | 1,05 / 1,49 / 1,64 |
| Raycell Mk2, 2,0 L | 167 | 97 | 0,58 | 2,12 L | 2,0 L | 1,35 / 0,50 / 0,91 |
| Raycell Mk2, 5,0 L | 240,5 | 119,5 | 0,50 | 5,43 L | 5,0 L | 1,94 / 0,62 / 2,32 |
| SANGRAY, bandeja | 350 | 70 | 0,20 | 6,73 L | não publicado | 2,82 / 0,36 / 2,87 |

O 6,73 L da bandeja é o disco de 350 mm por 70 mm, não um volume de sangue. A bandeja leva até sete bolsas de 400 mL, deitadas. O 2,12 L e o 5,43 L do Raycell são o cilindro das cotas do folheto; o fabricante chama essas peças de 2,0 L e 5,0 L. Um trabalho de dosimetria do Mk2 repete 167 mm por 97 mm e também chama o canister de 2,0 L (Grasso et al., *Applied Radiation and Isotopes*, 2023, DOI 10.1016/j.apradiso.2023.110981).

### Fonte de cada cota

Cada linha da tabela, e os dois recipientes que ficaram sem diâmetro e altura, com o documento de onde o número saiu.

- **Gammacell 1000 Elite, 80 mm × 164 mm, 0,824 L, e Gammacell 3000 Elan, 124 mm × 194 mm, 2,34 L.** Best Theratronics, folheto *Gammacell 1000 Elite / 3000 Elan*, arquivo de 16 de março de 2023, tabela “Canister Diameter (internal)” e “Canister Height (internal)”. https://www.theratronics.ca/PDFs/03_16_2023_BT_MBTS_8005_GC1000E_3000E_brochure.pdf
- **IBL 437C, 130 mm × 290 mm, 3,8 L.** Três textos independentes repetem o mesmo cilindro de alumínio. Bogner e Häring, *Strahlentherapie und Onkologie*, 1998: https://epub.uni-regensburg.de/23393/1/BognerL_DosimterieBlutbestrahlung_StrahlentherOnkol1998.pdf. Cruz Vermelha da Tailândia, mapeamento com Fricke: https://inis.iaea.org/records/dp4da-mq312/files/33055351.pdf. Descrição da unidade turca: https://onkoloji.dergisi.org/text.php?id=732
- **Raycell Mk2, 167 mm × 97 mm e 240,5 mm × 119,5 mm.** Best Theratronics, folheto de 13 de novembro de 2023, bloco “Canister Features”. https://www.theratronics.ca/PDFs/11_13_2023_BT_MBTS_8014_RCMK2_v13_2023.pdf. Os dois tubos e o canister parado no centro estão na página do produto: https://www.theratronics.ca/product_raycell_mk2.html. A cota de 167 mm por 97 mm reaparece em Grasso et al., *Applied Radiation and Isotopes*, 2023, DOI 10.1016/j.apradiso.2023.110981.
- **SANGRAY, bandeja Ø 350 mm × 70 mm, até sete bolsas de 400 mL.** Ficha do produto, Fujifilm Medical: https://www.eizojoho.co.jp/medicaldevice/detail/105872. A bandeja fina, para espessura abaixo de 35 mm, e a regra do monitor estão na bula notificada à PMDA, aprovação 22700BZX00036000, instruções de julho de 2024: https://www.pmda.go.jp/PmdaSearch/kikiDetail/ResultDataSetPDF/671001_22700BZX00036000_A_03_01. O 510(k) americano é o K172087, Hitachi, 27 de outubro de 2017: https://fda.innolitics.com/device/K172087
- **MBR-1520A-TW, pilha até 60 mm, campo cerca de 430 mm.** Bula de 20 de março de 2006, 3ª edição, aprovação 20500BZZ00241000, Hitachi Medical. Traz 150 kV, 20 mA, filtro de 1 mm de alumínio, SID de 600 mm, campo de cerca de 430 mm e espessura máxima de 60 mm. A cópia consultada está em https://manualzilla.com/doc/6572518/pdf%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB. O trabalho de 1990 com o MBR-1520R, tubo único por cima, mediu a face de baixo da bolsa como a dose mínima: https://doi.org/10.3925/jjtc1958.36.510
- **RS 3400, 1 L por canister, seis por ciclo.** Folha do canister: volume interno de 1 L e cerca de 868 mL com os insertos. https://labex.dk/wp-content/uploads/Rad-Source-Product-Sheet_RS-3400-Canister-1.pdf. O carrossel que orbita sem tombar o conteúdo é a patente US 7.515.686. O folheto que anuncia “dimensions on next page” e na página seguinte só mostra foto é o da Labex, revisão de setembro de 2023: https://labex.dk/wp-content/uploads/RS3400-Blood-Irradiator-By-Labex_rev3_092023.pdf
- **RadGil 2, até 1 800 mL, câmara de 290 mm por 290 mm.** Folheto Gilardoni: canister girante de três e de quatro compartimentos, até seis bolsas ou 1 800 mL; com o canister removido, área de 29 cm de diâmetro e altura máxima de amostra de 29 cm. https://www.gamma-medical.info/fileadmin/user_upload/Bilder/Dateien/Radgil2_data_sheet.pdf

## Como a bandeja funciona

Na bandeja as bolsas ficam lado a lado, com a face larga para o tubo, e a espessura da pilha é o caminho do feixe.

No SANGRAY há um tubo em cima e outro embaixo, os dois ligados juntos. A bolsa entra numa bandeja redonda, com tampa, e o tubo da bolsa não pode passar da borda. A bandeja grande tem 350 mm de diâmetro e 70 mm de espessura. Produto com menos de 35 mm de espessura vai na bandeja fina. A ficha de produto resume o botão de 15, 20 ou 25 Gy como o mínimo dentro da bandeja. A bula da PMDA é mais precisa: o número marcado é a dose na posição do monitor, e essa dose do monitor fica abaixo do mínimo dentro da bandeja. O aviso da bula existe por causa do máximo. Como o monitor está mais frio que a bandeja, a bandeja já passou do número que aparece na tela.

No MBR-1520A-TW há um tubo só, por cima. A bolsa vai num balde, a mesa sai, o balde entra, a mesa volta. A espessura tem de ficar uniforme e não passar de 60 mm. O operador escolhe uma faixa de cor, vermelha, amarela ou azul, conforme essa espessura. O campo, a 600 mm do foco, é um círculo de cerca de 430 mm. Com um tubo só, a face de baixo é a que está mais longe. Foi o que a dosimetria de 1990 no MBR-1520R mediu: a face inferior da bolsa recebia menos que a face de cima. O limite de 60 mm existe para essa diferença ainda caber entre 15 Gy e 50 Gy.

O Raycell também irradia na vertical, com dois tubos e o canister parado, mas o recipiente continua um cilindro, de 97 mm ou 119,5 mm de altura. A bandeja japonesa é mais rasa e bem mais larga que esses dois cilindros.

## O caminho do feixe

O que a geometria muda no mapa é a espessura que o feixe atravessa.

No Gammacell e no IBL as fontes ficam ao lado e o canister gira no próprio eixo. No plano médio, essa espessura é o diâmetro: 80 mm, 124 mm e 130 mm. O IBL é 5% mais largo que o 3000 Elan e 49% mais alto. O diâmetro quase igual diz que o caminho radial é parecido; os 96 mm a mais de altura afastam as tampas do plano das fontes. O 1000 Elite é o mesmo tipo de máquina, com 65% do diâmetro e 35% do volume.

No Raycell os dois tubos ficam em cima e embaixo e o canister fica parado. A espessura atravessada é a altura, 97 mm ou 119,5 mm, cerca de metade da altura do 3000 Elan, num disco 35% ou 94% mais largo. A bandeja do SANGRAY também é irradiada na vertical, em 70 mm de espessura, num disco de 350 mm. O MBR-1520 de hospital, anterior a essa bandeja, limita a pilha a 60 mm num campo de cerca de 430 mm.

Ficam de fora do desenho porque a cota publicada não fecha um cilindro:

- RS 3400: 1 L por canister, seis por ciclo. Sem diâmetro e sem altura.
- RadGil 2: até 1 800 mL no canister que gira. Com o canister fora, a câmara aceita uma amostra de 290 mm de diâmetro por 290 mm de altura. Essa cota é da câmara, não do canister de sangue.

## Como está o mercado

O mercado não está crescendo porque o mundo passou a irradiar mais sangue. Está trocando a fonte. O aparelho novo é um gabinete de raios X. O aparelho velho é um Cs-137 de categoria alta, e o custo que empurra a troca é a segurança da fonte, não um gray diferente.

### Estados Unidos

O Cesium Irradiator Replacement Project (CIRP), da NNSA, começou em 2014. Paga a retirada da fonte e, no desenho atual, 50% do aparelho de raios X que entra no lugar. A meta do Congresso é tirar de serviço, em caráter voluntário, os irradiadores de sangue com Cs-137 até 31 de dezembro de 2027.

Em 7 de julho de 2025 a própria ORS apresentava 91% do inventário americano de irradiadores de sangue com Cs-137 como eliminado ou já contratado. No mesmo slide, 373 irradiadores de sangue tinham sido eliminados pelo programa da ORS, número que não é só o território americano, e 75% de todo o inventário americano de irradiadores autoblindados de Cs-137, sangue mais pesquisa, estava eliminado ou contratado. https://www.agreementstates.org/uploads/1/1/8/4/118443122/0830hirsch_final.pdf

Um recorte anterior, citado pela Universidade de Connecticut com data de 5 de setembro de 2024, falava em 235 irradiadores de sangue com Cs-137 já substituídos pelo programa e 82% dos autoblindados de sangue americanos substituídos, removidos ou sob contrato. https://today.uconn.edu/2025/02/irradiator-removal-saves-millions-of-dollars-while-make-campuses-safer/. Os dois textos não usam o mesmo verbo. “Substituído” e “eliminado ou contratado” não são a mesma fração. O número mais recente, e o que separa sangue de pesquisa, é o de julho de 2025.

A Cruz Vermelha Americana tinha 33 irradiadores de sangue em 2017, quando começou a troca, e o programa da ORS marca essa rede como concluída no ano fiscal de 2022. A Vitalant aparece como concluída no ano fiscal de 2023. National Academies, *Radioactive Sources: Applications and Alternative Technologies* (2021), registra os 33 aparelhos da Cruz Vermelha e, para 2017, a estimativa de que cerca de 75% dos hemocomponentes irradiados nos Estados Unidos ainda passavam por césio. Esse 75% é de 2017. Não descreve 2026.

O folheto CIRP de setembro de 2024 está em https://www.energy.gov/nnsa/articles/ors-reduce-cirp-brochure-september-2024. A ficha mais genérica, que fala em mais de 75% do inventário autoblindado sem separar sangue de pesquisa, está em https://www.energy.gov/documents/cirp-fact-sheet.

### Fora dos Estados Unidos

A Suíça comunicou, em 2024, uma retirada nacional dos irradiadores de sangue com Cs-137, no mesmo espírito do CIRP. O Reino Unido tem a Operation Fieldfare, do Home Office com a Nuclear Decommissioning Authority, para dispor fontes médicas e de pesquisa. Os dois fatos estão no slide da ORS de julho de 2025, acima. Não são uma estatística de qual marca de raios X entrou no lugar.

O programa internacional da ORS, descrito no mesmo material do Sandia, financiava até aquele texto a troca de irradiadores gama por tecnologia sem radioisótopo, em geral raios X. Isso explica parte das compras na América Latina e no Oriente Médio. Não é um mandato da IAEA sobre o gray.

O Japão não está nessa fila. A irradiação universal é de 1998, o aparelho de centro é de raios X, e o recipiente é a bandeja. Hospital sem irradiador pede produto já irradiado à Cruz Vermelha.

Na Europa Ocidental a base antiga é o IBL 437C e o Gammacell. A compra nova reparte-se entre Raycell, RS 3400 e RadGil. Não há, nesta consulta, participação de mercado por fabricante que eu possa citar sem transformar publicidade em censo.

### Brasil

O parque é misto, e a troca é a mesma cooperação com o Departamento de Energia dos Estados Unidos, não uma exigência nova da ANSN.

A Análise de Resultado Regulatório da Norma ANSN 6.16 diz isso com todas as letras: a passagem de Cs-137 para raios X vem de cooperação internacional, em especial com o DOE/NNSA, e não do efeito da norma. https://www.gov.br/ansn/pt-br/regulacao/regulacao/avaliacao-de-resultado-regulatorio/arr_6_16_final-pdf_assinada.pdf/@@display-file/file

O que está documentado, sem pretender a lista completa:

- O Hemoce ainda opera um Gammacell 3000 E, série 429. O edital 202621406/2026 pede mapeamento dosimétrico desse feixe. O cilindro de 124 mm por 194 mm continua em serviço no Ceará em 2026.
- O Hospital Sírio-Libanês, em São Paulo, foi o primeiro do país no programa americano de troca. O Hospital de Câncer Araújo Jorge, em Goiânia, informa ter sido o segundo, com um RS 3400, e descreve um ciclo de cerca de 4,5 minutos. https://accg.org.br/sem-categoria/haj-conta-com-novo-irradiador-sanguineo-que-funciona-a-base-de-raio-x/
- O Hemocentro de Botucatu instalou um RS 3400 no lugar da ida à radioterapia com bomba de cobalto. O resumo de 2025 na *Hematology, Transfusion and Cell Therapy* relata ciclo de 240 segundos e até 6 L por ciclo, contra um tempo total perto de duas horas quando a bolsa saía do serviço. https://doi.org/10.1016/j.htct.2025.106066

Quem faz dosimetria de irradiador de sangue no Brasil, em 2026, ainda encontra o Gammacell 3000. Quem inaugura serviço encontra o RS 3400.

## O que isto muda neste repositório

O volume padrão, 124 mm por 194 mm, é o canister certo para o Gammacell 3000 Elan e para o que ainda roda dessa família no Brasil. É o cilindro mais citado quando o serviço fala “o canister” sem dizer o modelo. Não é o recipiente da compra nova.

Um mapa azimutal desse cilindro não serve, sem outro trabalho, para:

- o Gammacell 1000 Elite, que é o mesmo tipo de máquina num cilindro de 80 mm por 164 mm
- o IBL 437C, mais alto, 130 mm por 290 mm, com rotação e carga de fonte que mudam de unidade para unidade
- o Raycell, parado, baixo e largo, com dois tubos
- o RS 3400, seis volumes de 1 L em órbita, sem cota publicada de diâmetro e altura
- a bandeja japonesa, de 350 mm por 70 mm, em que o número do painel já é o mínimo

A uniformidade de catálogo do 3000 Elan, 19 / 25 / 33 Gy, é o campo desenhado para 25 Gy no centro. Onde a regra pede 25 Gy em todo o volume, o mesmo fabricante opera o mesmo canister em 25 / 33 / 43,5 Gy. Trocar de país sem trocar de canister muda o timer, não o desenho do cilindro.
