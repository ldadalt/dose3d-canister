# Referências de irradiação de sangue

Consulta em 27 de outubro de 2026. Este arquivo reúne os documentos que fixam a dose absorvida para prevenir a doença do enxerto contra o hospedeiro associada à transfusão (TA-GVHD), e separa isso do que a IAEA e a ISO de fato publicam.

Não reproduz normas pagas nem guias com copyright. A frase de dose de cada documento está resumida e ligada à fonte. Antes de usar um número como critério de liberação, releia a edição vigente: AABB, EDQM e as diretrizes nacionais são revisadas.

## Como ler a dose

Há dois jeitos de escrever o mesmo irradiador.

O Japão especifica a **dose em qualquer ponto da bolsa**: no mínimo 15 Gy e no máximo 50 Gy. A diretriz VI diz explicitamente que, no exterior, “25 Gy no centro” é outro modo de garantir que a borda, onde a dose cai, ainda receba pelo menos 15 Gy. Nos centros da Cruz Vermelha Japonesa, o botão de 15 Gy é ajustado para que todo o campo fique em 15 Gy ou mais; na prática, o produto fornecido fica em geral entre 15 Gy e cerca de 25 Gy.

Estados Unidos, Europa e Brasil não usam essa frase da mesma forma.

| Referência | Mínimo em qualquer ponto | Centro ou plano médio | Máximo em qualquer ponto | Quem recebe sangue irradiado |
| --- | --- | --- | --- | --- |
| Japão, diretriz VI (2024) e Cruz Vermelha | 15 Gy | não é o número da especificação | 50 Gy | quase todo componente celular alogênico, exceto plasma fresco congelado |
| FDA, 1993, reiterado em 2023 e na proposta de 2026 | 15 Gy | 25 Gy no centro do recipiente | não fixa | indicações de risco e doadores aparentados, não é universal |
| AABB, 32ª edição, citada pela BSH em 2020 | 15 Gy | 25 Gy na área central | não fixa | indicações selecionadas |
| EDQM, Guia do Sangue, 22ª ed. (2025), item 4.3.1.1 | 25 Gy | o mínimo vale para toda a bolsa, logo o centro também | 50 Gy | grupos de risco descritos no guia; a política nacional varia |
| Reino Unido, BSH 2020 e Red Book JPAC | 25 Gy no campo | o requisito é o mínimo no volume | 50 Gy | grupos de risco, doação de parentes e componentes HLA selecionados |
| Brasil, Portaria GM/MS 158/2016, art. 114 | 15 Gy | pelo menos 25 Gy no plano médio | 50 Gy | lista fechada de indicações; fora dela, protocolo do serviço |

O preset `fda-aabb` deste repositório segue a linha americana: 25 Gy no centro e 15 Gy no volume, sem máximo. O preset `portaria158` segue o art. 114: 15 Gy, 50 Gy e 25 Gy no plano central. O preset `bcsh` segue Reino Unido e EDQM: 25 Gy a 50 Gy em todo o volume. O preset `japan` segue a Diretriz VI: 15 Gy a 50 Gy em qualquer ponto, sem exigir 25 Gy no centro.

A Portaria pede 25 Gy **no plano médio**, isto é, um mínimo nesse plano. O programa, hoje, compara a **média** dos nós desse plano com 25 Gy. São contas diferentes.

## Japão

O Japão é a referência de irradiação quase universal. A TA-GVHD foi um problema grave, inclusive em pacientes imunocompetentes, por compatibilidade HLA em um só sentido, frequente em doação entre parentes. Desde junho de 1998 a Cruz Vermelha fornece hemocomponentes já irradiados. A diretriz VI registra que, a partir de 2000, não houve caso confirmado de TA-GVHD por hemocomponente irradiado fornecido por esse sistema.

Documentos:

- Sociedade Japonesa de Transfusão e Terapia Celular. *輸血による GVHD 予防のための血液に対する放射線照射ガイドライン VI* (Diretriz VI de irradiação do sangue para prevenir GVHD transfusional). Outubro de 2024. Revista da sociedade, vol. 70, n. 5, 2024. DOI: 10.3925/jjtc.70.527. Texto: https://yuketsu.jstmct.or.jp/wp-content/uploads/2025/10/GVHD_v6_070050527.pdf. Índice: https://yuketsu.jstmct.or.jp/guidelines/
- Cruz Vermelha Japonesa. Página de irradiação dos hemocomponentes: https://www.jrc.or.jp/mr/blood_product/safety/irradiation/
- Ministério da Saúde, Trabalho e Bem-Estar. *輸血療法の実施に関する指針* (Diretriz para a prática da transfusão). O PDF consultado é o da revisão cuja comissão é de setembro de 2005 (Heisei 17): https://www.mhlw.go.jp/new-info/kobetu/iyaku/kenketsugo/dl/tekisei4a_0003.pdf. Já traz 15 Gy em todo o campo, sem ultrapassar 50 Gy. A diretriz VI de 2024 é o texto técnico atual.

Como funciona:

- Irradia-se todo componente celular de doador alogênico: sangue total, concentrado de hemácias, plaquetas, granulócitos e plasma líquido fresco. Plasma fresco congelado não é irradiado, porque o congelamento destrói os linfócitos.
- A dose em **qualquer parte** da bolsa fica entre 15 Gy e 50 Gy. Abaixo de 15 Gy a proliferação dos linfócitos T não é controlada de modo confiável. Acima de 50 Gy passa a haver dano a hemácias, plaquetas e granulócitos.
- O mapeamento é feito com a carga máxima de bolsas no campo. Entra no cálculo a queda da taxa de dose e a contribuição do espalhamento. A condição é corrigida na manutenção periódica.
- No ano fiscal de 2022 (Reiwa 4), 95,4% dos concentrados de hemácias e 99,5% dos concentrados de plaquetas fabricados pela Cruz Vermelha já saíam irradiados. Hospital sem irradiador pede só produto irradiado. Hospital com irradiador, mas sem operação de 24 horas, usa produto da Cruz Vermelha na emergência.
- A Cruz Vermelha descreve o processo atual com irradiador de raios X dedicado, na faixa de 15 Gy a não mais que 50 Gy. A diretriz ainda distingue fonte gama, em geral Cs-137, com meia-vida de cerca de 30 anos e área controlada, e tubo de raios X de 150 kV ou 210 kV.
- Potássio no sobrenadante sobe mais depois da irradiação. Isso importa em recém-nascido, prematuro, insuficiência renal e transfusão maciça rápida.

## Estados Unidos

A dose americana é a do centro mais um piso na borda. Não há teto de 50 Gy no memorando do FDA nem na edição da AABB citada abaixo.

Documentos:

- Food and Drug Administration, Center for Biologics Evaluation and Research. *Recommendations Regarding License Amendments and Procedures for Gamma Irradiation of Blood Products*. Memorando de 22 de julho de 1993. https://www.fda.gov/files/vaccines,%20blood%20&%20biologics/published/Recommendations-Regarding-License-Amendments-and-Procedures-for-Gamma-Irradiation-of-Blood-Products.pdf
- FDA. Folha regulatória de 7 de novembro de 2023: o memorando de 1993, escrito para fonte gama, foi adotado também para irradiador de raios X. https://www.fda.gov/media/173451/download
- Federal Register, 18 de março de 2026. Proposta de classificação dos irradiadores de sangue como dispositivo Classe II, com controle especial que repete 25 Gy no centro e no mínimo 15 Gy em qualquer outro ponto. É proposta, não regra final. https://www.federalregister.gov/documents/2026/03/18/2026-05320/medical-devices-radiology-devices-classification-of-blood-irradiators
- AABB. *Standards for Blood Banks and Transfusion Services*, 32ª edição, conforme citada por Foukaneli et al., *British Journal of Haematology*, 2020 (DOI 10.1111/bjh.17015): 25 Gy na área central e nenhuma porção abaixo de 15 Gy, sem limite superior. A AABB revisa os *Standards*; a edição corrente precisa ser conferida no texto da própria AABB.

O memorando de 1993 pede 2500 cGy (25 Gy) no centro do recipiente e no mínimo 1500 cGy (15 Gy) em qualquer outro ponto. Fontes aceitas à época: Cs-137, Co-60 ou acelerador linear. A curva de isodose do canister não substitui a dose na bolsa: a validação usa dosímetro, em geral TLD, todo ano e depois de reparo mecânico, sobretudo do mecanismo que gira a amostra. Etiqueta indicadora de exposição é recomendada.

A irradiação nos Estados Unidos não é universal. O histórico do memorando é a extensão, em 1993, da indicação a todo doador geneticamente aparentado ao receptor, além dos pacientes imunocomprometidos.

## Europa

O número harmonizado está no guia técnico do Conselho da Europa, não numa diretiva que diga “25 Gy”.

Documentos:

- Conselho da Europa, Recomendação n.º R(95)15. O anexo técnico é o *Guide to the preparation, use and quality assurance of blood components* (Blood Guide), publicado pelo EDQM. Edição corrente consultada: 22ª, publicada em 21 de maio de 2025. https://www.edqm.eu/en/blood-guide
- Item 4.3.1.1 dessa edição: o processo deve assegurar que nenhuma parte do componente receba menos de 25 Gy nem mais de 50 Gy. O item 4.3.1.2 pede mapeamento periódico, revalidação do tempo de exposição e indicador para separar produto irradiado de não irradiado.
- Diretiva 2002/98/CE e Diretiva 2004/33/CE fixam qualidade e segurança do sangue na União Europeia e não estabelecem o valor em gray. O Regulamento (UE) 2024/1938 as substitui, com transição até 7 de agosto de 2027. A dose continua no Blood Guide.
- Reino Unido, fora da regra da UE, mas alinhado ao mesmo intervalo. British Society for Haematology: Foukaneli et al., *Guidelines on the use of irradiated blood components*, Br J Haematol, 2020. DOI 10.1111/bjh.17015. Recomendação: mínimo de 25 Gy no volume irradiado e nenhuma parte acima de 50 Gy. Gama e raios X são equivalentes. A validação e a dosimetria periódica são obrigatórias, com físico médico.
- JPAC, *Guidelines for the Blood Transfusion Services in the UK* (Red Book), capítulo 7, componentes irradiados. Mesma dose, com a nota de ±10% no intervalo de confiança de 95%. Dosimetria anual no irradiador gama; o fabricante do equipamento de raios X recomenda dosimetria semestral. Texto de agosto de 2026: https://www.transfusionguidelines.org/red-book/chapter-7-specifications-for-blood-components

Plasma congelado abaixo de −25 °C e crioprecipitado não precisam de irradiação. Hemácias criopreservadas, depois de desglicerolizadas, também não, na regra britânica. Granulócitos são irradiados e usados logo.

A diretriz alemã da Bundesärztekammer e os textos da França não foram extraídos nesta consulta. O número europeu de partida é o do EDQM; o texto nacional pode ser mais estrito.

## Brasil

- Ministério da Saúde. Portaria de Consolidação, na origem Portaria GM/MS n.º 158, de 4 de fevereiro de 2016, art. 114. https://bvsms.saude.gov.br/bvs/saudelegis/gm/2016/prt0158_04_02_2016.html
- Anvisa. RDC n.º 34, de 11 de junho de 2014. O artigo localizado usa os mesmos três números: 25 Gy no plano médio, nenhuma parte abaixo de 15 Gy nem acima de 50 Gy. Os roteiros de inspeção da Anvisa ainda citam esse artigo.

O art. 114 exige procedimento que garanta a irradiação e dose mínima de 25 Gy no plano médio da unidade. Em nenhum ponto a dose fica abaixo de 15 Gy nem acima de 50 Gy. O objetivo é inativar linfócitos viáveis. Unidade rotulada, processo validado periodicamente, controle da fonte documentado no mínimo uma vez por ano. O equipamento próprio é o irradiador de células; na falta dele, acelerador linear de radioterapia, com profissional qualificado.

Não é política universal. O § 11 lista transfusão intrauterina, recém-nascido abaixo de 1 200 g ou prematuro abaixo de 28 semanas, imunodeficiência congênita grave, imunossupressão pós-transplante de medula, componente HLA compatível e receptor parente de primeiro grau do doador. Fora dessa lista, decide o protocolo do serviço.

A licença da fonte de Cs-137 é assunto da CNEN, não da Portaria. A Portaria fixa a dose no sangue.

## IAEA e ISO

Nenhuma das duas substitui o FDA, o EDQM ou a Portaria na escolha do gray clínico.

A IAEA classifica fontes radioativas e trata da segurança delas. O guia RS-G-1.9, *Categorization of Radioactive Sources* (2005), coloca irradiadores de alta atividade no topo da escala. Um irradiador de sangue com Cs-137, em atividade típica de dezenas a poucas centenas de TBq, cai nas categorias mais altas, em geral categoria 1. Documentos recentes da AIEA sobre instalações de irradiação registram que a Agência deixou de fornecer fontes de césio a Estados-Membros em desenvolvimento e que a substituição em curso é por tubo de raios X. Isso é segurança da fonte e tecnologia, não a prescrição de 15, 25 ou 50 Gy.

ISO e ASTM publicam a **dosimetria** do processo, não a indicação clínica:

- ISO/ASTM 51939:2013, *Practice for blood irradiation dosimetry*, foi retirada.
- O texto vigente consultado é o ASTM E1939-22e1 (também numerado 51939), *Standard Practice for Blood Irradiation Dosimetry*, 2022. https://www.astm.org/e1939-22.html
- Cobre qualificação de instalação, operação e desempenho, e o controle rotineiro, para irradiador autoblindado de Cs-137 ou Co-60 e para raios X de freamento, em geral de 40 keV a 300 keV. O intervalo típico citado é 15 Gy a 50 Gy. O próprio texto diz que o limite inferior, o teto ou a dose central vêm do regulamento aplicável, não da norma.
- Etiqueta sensível à radiação é indicador qualitativo de que o produto passou pelo irradiador. Não mede a dose.
- ISO 13485 é o sistema da qualidade do dispositivo médico. ISO 3826 é o recipiente de sangue. Nenhuma das duas fixa o gray da TA-GVHD.

## O que isto muda neste repositório

Um mapa que passa no preset americano pode falhar no europeu: 19 Gy na borda cumpre o FDA e não cumpre o EDQM nem o Reino Unido, que exigem 25 Gy em toda a bolsa. Um mapa japonês de 15 Gy a 25 Gy cumpre a diretriz VI e não cumpre o art. 114 brasileiro no plano médio.

A curva do fabricante do Gammacell 3000 Elan, cerca de 19 / 25 / 33 Gy quando o centro recebe 25 Gy, foi desenhada para a especificação americana. Para uma especificação de mínimo 25 Gy em todo o canister, o fabricante publica outro ponto de operação, com o centro acima de 25 Gy.

As cotas dos outros canisters, e o fato de a compra nova ser um recipiente de raios X e não esse cilindro, estão em [canisters-e-mercado.md](canisters-e-mercado.md).
