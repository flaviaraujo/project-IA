# project-IA

## TODO

- [ ] Descrição do problema - o que retiramos do enunciado
- [ ] Formulação do problema - estado inicial, estado/teste objetivo, operadores (ações disponíveis) e o custo da solução
- [x] Representação em grafo (zonas de entrega e caminhos possíveis)
- [ ] Implementar DFS e BFS
- [ ] Implementar A* e Greedy
- [ ] Implementar a nossa heurística
- [ ] Os algoritmos implementados serem testados com as condições das Notas
- [ ] Simular condições dinâmicas, como mudanças meteorológicas, que podem afetar a velocidade
dos veículos e bloquear acessos a determinadas zonas.

## Notas

- Diferentes prioridades de emergência (baseado no tempo de resposta e distância)
- Condições variáveis (rotas bloqueadas e limitações dos veículos)
- Limitações geográficas que impedem certos veículos de aceder a determinadas zonas (e.g.,
terrenos inacessíveis para camiões).
- Condições meteorológicas dinâmicas que afetam o tempo e a rota dos veículos (e.g.,
tempestades).
- Prioridades das zonas com base em necessidades e gravidade da situação.
- Limitação de recursos (e.g. peso e volume de carga) e combustível, forçando uma gestão eficiente
de reabastecimentos e escolhas de rotas.
- Cada zona tem uma janela de tempo crítica, após a qual o acesso pode se tornar impossível.

## Heurísticas

1. Distâncias para cada catástrofe por tipo de veículo e nível de acesso

```
A : {
    "car": {
        B: 3,
        F: infinity
    },
    "motorcycle": {
        B: 3,
        F: 9
    },
    ...
},
B : {
    "car": {
        B: 0,
        F: infinity
    },
    "motorcycle": {
        B: 0,
        F: 12
    },
    ...
},
...
```

2. Prioridades para cada catástrofe por tipo de veículo, nível de acesso, tempo_chegada_veículo - tempo_resposta_catastrofe e combustível

3. Prioridades para cada catástrofe por tipo de veículo, nível de acesso, tempo_chegada_veículo - tempo_resposta_catastrofe, carga_veiculo/demanda_catastrofe e combustível

## Algoritmo

Prioridades:
1. Chegar a tempo/Resolver catástrofe a tempo
2. Maximizar a carga de forma a resolver a catástrofe no menor número de viagens
3. Minimizar Combustível

---

- Calcular objetivo ótimo para cada veículo
    - Verificar se é possível chegar a tempo para cada catástrofe (ter em conta a perecibilidade de alimentos)
    - Para cada uma dessas catástrofes
        - Considerar a carga de veiculo perante as necessidades da catástrofe
        - Adicionar o veículo à lista de veículos que podem resolver a catástrofe:
            (Veículo(Capacidade_carga, Combustível), Catástrofe, Nº de viagens, boolean: resolve a tempo)
- Da lista de veículos que podem resolver a catástrofe, escolher o veículo que minimiza o combustível.
