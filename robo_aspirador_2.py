import random


class Environment:
    """Classe base para o ambiente."""

    def __init__(self, linhas, colunas):
        self.linhas = linhas
        self.colunas = colunas
        self.grid = [[random.choice(['limpo', 'sujo'])
                      for _ in range(colunas)] for _ in range(linhas)]
        self.agent_position = (0, 0)  # Posição inicial do agente

    def percept(self):
        """Retorna a percepção para o agente."""
        linha, coluna = self.agent_position
        return self.grid[linha][coluna]

    def execute_action(self, action):
        """Executa uma ação no ambiente."""
        linha, coluna = self.agent_position
        if action == 'aspirar':
            self.grid[linha][coluna] = 'limpo'
        elif action == 'baixo' and linha < self.linhas - 1:
            self.agent_position = (linha + 1, coluna)
        elif action == 'cima' and linha > 0:
            self.agent_position = (linha - 1, coluna)
        elif action == 'direita' and coluna < self.colunas - 1:
            self.agent_position = (linha, coluna + 1)
        elif action == 'esquerda' and coluna > 0:
            self.agent_position = (linha, coluna - 1)

    def is_clean(self):
        """Verifica se todas as células estão limpas."""
        return all(cell == 'limpo' for row in self.grid for cell in row)

    def display(self):
        """Exibe o estado atual do ambiente."""
        for row in self.grid:
            print(row)
        print(f"Agente está em: {self.agent_position}\n")


class QLearningAgent:
    """Agente baseado em Q-Learning."""

    def __init__(self, linhas, colunas, actions, alpha=0.5, gamma=0.95, epsilon=0.8, epsilon_decay=0.995, epsilon_min=0.1):
        self.actions = actions
        self.alpha = alpha  # Taxa de aprendizado
        self.gamma = gamma  # Fator de desconto
        self.epsilon = epsilon  # Probabilidade de exploração
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.q_table = {}  # Tabela Q
        self.visited_positions = set()  # Posicionamentos visitados
        self.linhas = linhas
        self.colunas = colunas

    def get_state(self, environment):
        """Obtém o estado como uma tupla representando a posição e células vizinhas."""
        linha, coluna = environment.agent_position
        vizinhos = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nl, nc = linha + dx, coluna + dy
            if 0 <= nl < self.linhas and 0 <= nc < self.colunas:
                vizinhos.append(environment.grid[nl][nc])
            else:
                vizinhos.append('borda')
        return tuple(vizinhos + [environment.grid[linha][coluna], environment.agent_position])

    def choose_action(self, state):
        """Escolhe uma ação com base na política epsilon-greedy."""
        if random.random() < self.epsilon:
            return random.choice(self.actions)
        else:
            q_values = self.q_table.get(
                state, {action: 0 for action in self.actions})
            return max(q_values, key=q_values.get)

    def update_q_table(self, state, action, reward, next_state):
        """Atualiza a tabela Q usando a fórmula do Q-Learning."""
        if state not in self.q_table:
            self.q_table[state] = {action: 0 for action in self.actions}
        if next_state not in self.q_table:
            self.q_table[next_state] = {action: 0 for action in self.actions}

        current_q = self.q_table[state][action]
        max_next_q = max(self.q_table[next_state].values())
        new_q = (1 - self.alpha) * current_q + self.alpha * \
            (reward + self.gamma * max_next_q)
        self.q_table[state][action] = new_q

        # Decai o epsilon
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay


# Simulação
linhas, colunas = 4, 4
actions = ['aspirar', 'baixo', 'cima', 'esquerda', 'direita']
agent = QLearningAgent(linhas, colunas, actions)

# Treinamento do agente
episodes = 500  # Número de episódios para treinamento

for episode in range(episodes):
    environment = Environment(linhas, colunas)  # Reinicia o ambiente
    agent.visited_positions.clear()  # Limpa o histórico de estados visitados
    while not environment.is_clean():
        # Obtém o estado atual
        state = agent.get_state(environment)
        # Escolhe uma ação
        action = agent.choose_action(state)
        # Executa a ação no ambiente
        percept = environment.percept()
        environment.execute_action(action)

        # Calcula a recompensa
        if action == 'aspirar' and percept == 'sujo':
            reward = 50  # Grande recompensa por aspirar uma célula suja
        elif action == 'aspirar' and percept == 'limpo':
            reward = -20  # Penalidade alta por aspirar uma célula limpa
        elif environment.agent_position in agent.visited_positions:
            reward = -15  # Penalidade por retornar a posições já visitadas
        else:
            reward = -1  # Penalidade leve para movimentos gerais

        # Atualiza posições visitadas
        agent.visited_positions.add(environment.agent_position)

        # Obtém o próximo estado
        next_state = agent.get_state(environment)
        # Atualiza a tabela Q
        agent.update_q_table(state, action, reward, next_state)

# Teste do agente após o treinamento
environment = Environment(linhas, colunas)
print("Estado inicial do ambiente (teste):")
environment.display()

steps = 0
while not environment.is_clean():
    state = agent.get_state(environment)
    action = agent.choose_action(state)
    environment.execute_action(action)
    steps += 1
    print(f"Etapa {steps}: Agente executou '{action}'.")
    environment.display()

print(f"Todas as células foram limpas em {steps} etapas!")