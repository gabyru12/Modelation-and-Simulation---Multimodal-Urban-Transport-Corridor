# Multimodal Urban Transport Corridor Simulation

Projeto académico de Modelling and Simulation para preparar uma simulação microscópica de um corredor urbano multimodal no Porto, aproximadamente entre a Rotunda da Boavista e a zona do Bessa.

Nesta fase o objetivo é apenas criar uma base técnica pequena e testável: Python deve conseguir lançar o SUMO, controlar a simulação via TraCI e avançar uma rede mínima de teste.

## Arquitetura

```text
OpenStreetMap
    |
SUMO
    | TraCI
Python integration layer
    |
Mesa
    |
Data collection / experiments / analysis
```

Responsabilidades iniciais:

- SUMO é a fonte de verdade temporal e física da simulação: movimento dos veículos, car-following, lane changing, junctions, semáforos e filas.
- TraCI fica encapsulado em `src/integration/sumo_interface.py`.
- Mesa fica reservado para agentes e decisões de nível superior. Nesta fase só é preparado estruturalmente.
- O projeto ainda não implementa prioridade semafórica, agentes inteligentes, OpenStreetMap ou análise estatística.

## Estrutura

```text
config/                  Configuração de cenários
network/
  raw/                   Dados de rede originais futuros
  final/                 Redes SUMO finais futuras
sumo/
  routes/                Ficheiros de rotas SUMO
  additional/            Ficheiros adicionais SUMO
  configs/               Ficheiros .sumocfg
src/
  model/
    agents/              Agentes Mesa futuros
    policies/            Políticas futuras
  integration/           Integração com SUMO/TraCI
  simulation/            Execução de simulações
  data/                  Recolha/transformação de dados futura
experiments/             Experiências reproduzíveis
results/
  raw/                   Saídas geradas brutas
  processed/             Resultados processados
analysis/                Notebooks/scripts de análise futura
tests/                   Testes automatizados
```

## Instalação

Instala primeiro o SUMO no sistema e confirma que os comandos `sumo` e `netconvert` estão acessíveis no terminal.

No Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Em macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Testes iniciais

Executa o smoke test com:

```bash
python -m pytest
```

O teste cria uma rede SUMO mínima a partir dos ficheiros em `tests/fixtures/sumo_smoke/`, inicia o SUMO em modo headless, avança a simulação via TraCI e confirma que pelo menos um veículo é observado durante a execução.

Se `mesa`, `traci`, `sumolib`, `sumo` ou `netconvert` não estiverem disponíveis, o teste é marcado como skipped com a razão correspondente.

## Milestones iniciais

1. Base do repositório, interface TraCI e smoke test SUMO.
2. Importação controlada de uma rede OpenStreetMap do corredor real.
3. Cenário base com semáforos fixos.
4. Integração Mesa para decisões de nível superior.
5. Cenários Bus Priority e Conditional Bus Priority.
6. Recolha de métricas e análise comparativa.
