# CHANGELOG-AGENT

Diário de mudanças feitas com o agente (intenção + resolução).
Mais recente no topo.

## 2026-10-27 — Fonte de cada cota e o corte da bandeja

- **Chat:** Dose 3D canister de sangue
- **Intenção:** Colocar a referência de cada dimensão no documento e desenhar como a bandeja irradia.
- **Resolução:**
  - Cada cota de `docs/canisters-e-mercado.md` ficou ligada ao folheto, ao artigo ou à bula de onde saiu.
  - A seção da bandeja descreve o SANGRAY, com dois tubos e monitor abaixo do mínimo da bandeja, e o MBR-1520A-TW, com um tubo por cima e pilha de até 60 mm.
- **Resultado:** ok
- **Evidência:** `docs/canisters-e-mercado.md`

## 2026-10-27 — Quinto set de teste TLD (grade E, 21×20)

- **Chat:** Dose 3D canister de sangue
- **Intenção:** Incluir mais uma planilha amarela/azul no banco de testes.
- **Resolução:**
  - `examples/tld_grid_e_21x20.csv` (20–36 Gy, 21 linhas × 20 colunas).
  - Mesma família do set A, com a linha `34,33,30…` entre a faixa de 35 Gy e o pico vermelho de 36 Gy.
  - Japão passa; BCSH/EDQM falha no mínimo.
- **Resultado:** ok
- **Evidência:** `examples/tld_grid_e_21x20.csv`

## 2026-10-27 — Geometria dos canisters na mesma escala

- **Chat:** Dose 3D canister de sangue
- **Intenção:** Juntar as medidas dos canisters mais citados para comparar a geometria.
- **Resolução:**
  - Tabela em `docs/canisters-e-mercado.md` com Ø, altura, altura/Ø e volume do cilindro para 1000 Elite, 3000 Elan, IBL 437C, Raycell 2 L e 5 L, e a bandeja SANGRAY.
  - O 3000 Elan fica como referência: o IBL é 5% mais largo e 49% mais alto; o Raycell é mais largo e tem cerca de metade da altura.
  - RS 3400 e RadGil 2 continuam sem diâmetro e altura publicados; o folheto que promete a cota só mostra foto.
- **Resultado:** ok
- **Evidência:** `docs/canisters-e-mercado.md`

## 2026-10-27 — Canisters frequentes e o mercado

- **Chat:** Dose 3D canister de sangue
- **Intenção:** Montar, no mesmo espírito do documento de legislação, quais canisters são os mais usados e como está o mercado.
- **Resolução:**
  - `docs/canisters-e-mercado.md` separa cilindro girante de Cs-137, Raycell parado, carrossel RS 3400 e bandeja japonesa.
  - Cotas publicadas: Gammacell 3000 Elan 124×194 mm, 1000 Elite 80×164 mm, IBL 437C 130×290 mm, Raycell 167×97 mm e 240,5×119,5 mm, bandeja Sangray Ø350×70 mm.
  - Mercado descrito pela troca de fonte, não por fatia de fabricante: 91% do inventário americano de sangue com Cs-137 eliminado ou contratado em julho de 2025; Brasil ainda com Gammacell 3000 e compra nova em RS 3400.
- **Resultado:** ok
- **Evidência:** `docs/canisters-e-mercado.md`

## 2026-10-27 — Quarto set de teste TLD (grade D, metade espelhada)

- **Chat:** Dose 3D canister de sangue
- **Intenção:** Incluir a planilha decimal que traz só metade do mapa, usando inteiros e espelhando o outro lado.
- **Resolução:**
  - Espelho parede→centro→parede em `tld_grid_d_20x20.csv` (14–37 Gy); só o mapa completo ficou no repositório.
  - O ponto frio 14 Gy na parede faz o Japão e o BCSH falharem.
- **Resultado:** ok
- **Evidência:** `examples/tld_grid_d_20x20.csv`

## 2026-10-27 — Terceiro set de teste TLD (grade C)

- **Chat:** Dose 3D canister de sangue
- **Intenção:** Incluir a terceira heat map 20×20 como outro conjunto de teste.
- **Resolução:**
  - `examples/tld_grid_c_20x20_matrix.csv` e `examples/tld_grid_c_20x20.csv` (16–43 Gy).
  - Pontos frios em 16 Gy e pico de parede em 43 Gy.
  - Japão passa; BCSH/EDQM falha pelo mínimo abaixo de 25 Gy.
- **Resultado:** ok
- **Evidência:** `examples/tld_grid_c_20x20.csv`

## 2026-10-27 — Segundo set de teste TLD (grade B)

- **Chat:** Dose 3D canister de sangue
- **Intenção:** Incluir a segunda planilha/heat map como outro conjunto de dados de teste.
- **Resolução:**
  - `examples/tld_grid_b_20x20_matrix.csv` e `examples/tld_grid_b_20x20.csv` (21–36 Gy).
  - Mesmo mapeamento no plano `y = 0` e expansão axisimétrica.
  - Japão passa; BCSH/EDQM falha pelo mínimo de 21 Gy.
- **Resultado:** ok
- **Evidência:** `examples/tld_grid_b_20x20.csv`

## 2026-10-27 — Grade TLD 20×20 como conjunto de teste

- **Chat:** Dose 3D canister de sangue
- **Intenção:** Usar a planilha 20×20 de doses (Gy) como set de teste.
- **Resolução:**
  - Transcrição em `examples/tld_grid_20x20_matrix.csv` e pontos no plano `y = 0` em `examples/tld_grid_20x20.csv`.
  - Faixa 20–36 Gy; paredes laterais no meio da altura chegam a 36 Gy.
  - Flag `--axisymmetric` copia o plano ao redor do eixo, porque o canister gira.
  - No Japão o mapa passa (20–36 Gy). No BCSH/EDQM falha, porque o mínimo medido é 20 Gy e a Europa pede 25 Gy em todo o volume.
- **Resultado:** ok
- **Evidência:** `examples/tld_grid_20x20.csv`, `src/dose3d_canister/axisymmetric.py`

## 2026-10-27 — Isodose em gray e modelo 3D nos mesmos níveis

- **Chat:** Dose 3D canister de sangue
- **Intenção:** Ter o mapa de isodose consagrado no meio e, junto, o modelo 3D feito a partir dos pontos.
- **Resolução:**
  - Curvas rotuladas em 15, 20, 25, 30, 35, 40, 45 e 50 Gy nos planos axial e coronal, só quando a dose reconstruída cruza esse valor.
  - Superfícies 3D nos mesmos níveis, no mesmo HTML.
  - PNG, GIF e PDF passam a desenhar essas curvas sobre o mapa de cores.
- **Resultado:** ok
- **Evidência:** `src/dose3d_canister/view.py`

## 2026-10-27 — Preset japonês de 15 a 50 Gy

- **Chat:** Dose 3D canister de sangue
- **Intenção:** Incluir o critério do Japão na comparação de doses.
- **Resolução:**
  - Preset `japan` (também `jrc`): 15 Gy a 50 Gy em qualquer ponto, sem exigir 25 Gy no centro.
  - Um mapa com 20 Gy no centro passa no Japão e falha no FDA/AABB.
  - README e o arquivo de referências passam a citar o preset.
- **Resultado:** ok
- **Evidência:** `src/dose3d_canister/criteria.py`, testes em `tests/test_canister.py`

## 2026-10-27 — Referências de dose Japão, EUA, Europa, Brasil, IAEA e ISO

- **Chat:** Dose 3D canister de sangue
- **Intenção:** Juntar num arquivo os documentos de países e de IAEA/ISO sobre irradiação de sangue, com o modo japonês, americano e europeu de escrever a dose.
- **Resolução:**
  - Criado `docs/referencias-irradiacao-de-sangue.md` com a tabela de 15, 25 e 50 Gy e o link de cada documento.
  - O Japão especifica 15 a 50 Gy em qualquer ponto da bolsa; FDA e AABB especificam 25 Gy no centro e 15 Gy na borda.
  - EDQM 22ª edição e BSH 2020 exigem 25 a 50 Gy em toda a bolsa. A IAEA não fixa o gray clínico; ASTM E1939-22e1 trata da dosimetria.
  - O README passou a apontar para esse arquivo e a citar a edição vigente de cada número.
- **Resultado:** ok
- **Evidência:** `docs/referencias-irradiacao-de-sangue.md`
- **Pendências:** o arquivo ainda não foi para o GitHub; preset japonês (15–50 Gy, sem 25 Gy no centro) não entrou no código.

## 2026-10-27 — Dose 3D no canister de irradiação de sangue

- **Chat:** Dose 3D canister de sangue
- **Intenção:** Analisar o artigo do irradiador e o plano de carreira, e começar aqui o projeto público de dose 3D no canister.
- **Resolução:**
  - Pacote Python `dose3d-canister` com o cilindro interno do Gammacell 3000 Elan (124 mm × 194 mm).
  - Leitura de CSV, interpolação linear dentro do casco dos pontos, métricas e critérios FDA/AABB, Portaria 158 e BCSH.
  - Correção do tempo de irradiação pelo decaimento do Cs-137 e relatório PDF mais vista HTML.
  - Mapa sintético ilustrativo, testes e figuras no README. Nenhum dado de serviço entrou no repositório.
- **Resultado:** ok
- **Evidência:** pacote 0.1.0, 13 testes, https://github.com/ldadalt/dose3d-canister
