# CHANGELOG-AGENT

Diário de mudanças feitas com o agente (intenção + resolução).
Mais recente no topo.

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
