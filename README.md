 🤖 Robô Aspirador Inteligente com Q-Learning

Este projeto simula um **robô aspirador inteligente** que aprende a limpar um ambiente de forma eficiente usando o algoritmo de aprendizado por reforço **Q-Learning**.

## ✅ O que o projeto faz

O sistema cria um ambiente 2D onde células podem estar limpas ou sujas, e um agente (o robô) se move e aprende a aspirar sujeira da melhor forma possível. O robô:

- Percebe o estado atual do ambiente.
- Escolhe ações com base na política **epsilon-greedy**.
- Aprende com recompensas ou penalidades:
  - 🎯 +50 por aspirar uma célula suja
  - ⚠️ -20 por aspirar uma célula limpa
  - 🌀 -15 por retornar a uma célula já visitada
  - ➖ -1 por movimentos normais

## 🚀 Como começar a usar o projeto

1. **Execute o script Python**:
   Certifique-se de ter o Python 3 instalado. Em seguida:
   ```bash
   python robo_aspirador_2.py
   ```

2. **Acompanhe o treinamento e o teste**:
   O console exibirá o ambiente, ações do robô e o número total de etapas até o ambiente estar limpo.

## 👥 Quem mantém e contribui com o projeto

- 👨‍💻 Desenvolvido por estudantes da disciplina de Inteligência Artificial
- 🎓 Universidade Federal do Maranhão (UFMA)

---

Projeto com fins acadêmicos e didáticos.
