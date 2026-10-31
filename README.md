# 🍳 Personal Chef

Un assistant culinaire conversationnel en ligne de commande, construit avec
**LangChain** et **LangGraph**. Il répond à tes questions de cuisine, te propose
des recettes à partir des ingrédients qu'il te reste et cherche des recettes
récentes sur le web via Tavily.

> Projet d'apprentissage personnel pour explorer les concepts de LangChain :
> agents, tools, checkpointer, streaming et system prompts.

---

## ✨ Fonctionnalités

- 💬 **Conversation multi-tours** — mémoire du contexte grâce à un checkpointer LangGraph (`InMemorySaver` + `thread_id`).
- 🔧 **Outil `web_search`** — recherche web via [Tavily](https://tavily.com/) pour trouver des recettes actuelles ou vérifier des informations.
- ⚡ **Streaming token par token** — la réponse s'affiche en temps réel dans le terminal.
- 🧠 **System prompt spécialisé** — l'assistant se comporte comme un chef cuisinier pédagogue : quantités, étapes, substitutions, régimes, sécurité alimentaire, etc.
- 📎 **Sources citées** — le prompt demande au modèle de rechercher systématiquement une recette sur le web et d'en citer la source.

---

## 🛠️ Prérequis

- **Python ≥ 3.14** (projet développé et testé avec Python 3.14.7)
- **[uv](https://docs.astral.sh/uv/)** pour la gestion du projet et des dépendances
- Une clé API **[OpenRouter](https://openrouter.ai/)** (pour le modèle `deepseek-v4.1-flash-1017`)
- Une clé API **[Tavily](https://tavily.com/)** (pour l'outil `web_search`)

---

## 🚀 Installation

### 1. Cloner le projet

```bash
git clone https://github.com/pierreraffoul/Personal-Chef.git
cd Personal-Chef
```

### 2. Installer les dépendances

```bash
uv sync
```

### 3. Configurer les variables d'environnement

Copie le modèle fourni puis renseigne tes clés :

```bash
cp .env.example .env
```

```dotenv
OPENROUTER_API_KEY=sk-or-v1-...
TAVILY_API_KEY=tvly-...
```

⚠️ Le fichier `.env` ne doit jamais être commité (il est dans `.gitignore`).

---

## ▶️ Utilisation

```bash
uv run python main.py
```

Tu arrives dans une boucle interactive :

```text
Entrez un message : Qu'est-ce que je peux faire avec du poulet et du riz ?
Chef : [réponse en streaming]
```

Tape `quit`, `exit` ou `q` (insensible à la casse) pour quitter.

- La conversation garde le contexte tant que le `thread_id` est le même.
- La mémoire est **en processus** (`InMemorySaver`) : elle est perdue à la fermeture du programme.
- Le system prompt impose de chercher une recette sur le web et de citer la source, donc l'agent appelle `web_search` de lui-même.

---

## 📁 Structure du projet

```text
personal_chef/
├── main.py              # Point d'entrée : agent, tool, boucle de chat
├── config.py            # Chargement du .env (load_config, non utilisée)
├── system_prompt.py     # System prompt (variable `systemprompt`)
├── pyproject.toml       # Dépendances gérées par uv
├── uv.lock              # Versions verrouillées (à commiter)
├── .python-version      # Version Python demandée (3.14)
├── .env                 # Clés API (JAMAIS commité)
├── .env.example         # Modèle de fichier .env (à copier en .env)
├── .gitignore
└── README.md
```

---

## 🧩 Détails techniques

### Modèle

`deepseek-v4.1-flash-1017` via OpenRouter, instancié avec `init_chat_model` :

```python
init_chat_model(
    model="deepseek-v4.1-flash-1017",
    model_provider="openrouter",
)
```

L'usage de `model_provider="openrouter"` est nécessaire car le préfixe du nom
n'indique pas le provider à LangChain. Le provider est fourni par la dépendance
`langchain-openrouter`.

### Outil `web_search`

```python
@tool
def web_search(query: str) -> dict[str, Any]:
    """utilise le web pour chercher des informations"""
    return tavily_client.search(query)
```

La docstring sert de description à l'outil : c'est ce que le modèle lit pour
décider s'il doit l'utiliser. Elle doit être claire et décrire quand utiliser
l'outil, pas seulement ce qu'il fait.

### Mémoire conversationnelle

```python
config = {"configurable": {"thread_id": "conversation-1"}}
```

Le checkpointer enregistre chaque tour sous un `thread_id`. Il suffit de passer
le nouveau message : le contexte est reconstitué automatiquement.

### Streaming

```python
stream_mode="messages"
```

Émet chaque token (ou petit chunk) dès sa production par le modèle.
Le filtre `if token.content:` ignore les chunks non textuels (appels d'outils,
métadonnées). La variable `metadata` n'est pas utilisée pour l'instant.

---

## ⚠️ Points d'amélioration connus

Ce projet est un support d'apprentissage. Les points suivants ont été identifiés :

### Code

1. **Retour Tavily brut.** `web_search` renvoie directement le dict complet de
   Tavily (titres, URLs, contenus, scores...), qui peut être volumineux et
   saturer la fenêtre de contexte. → Résumer le retour en texte dans l'outil
   (par exemple concaténer les 5 premiers titres + extraits).
2. **Retour de l'outil non typé.** La signature `dict[str, Any]` est correcte,
   mais un retour `str` résumé serait plus simple à consommer pour le modèle.
3. **`config.py` peu utile en l'état.** Le fichier définit `load_config()` mais
   ne l'utilise pas ; `main.py` importe `load_dotenv` depuis `config`, qui le
   ré-exporte simplement depuis `python-dotenv`. → Soit appeler explicitement
   `load_config()`, soit importer `load_dotenv` directement depuis `dotenv`.

---

## 📚 Ce que ce projet m'a appris

- Créer un agent LangChain avec `create_agent`
- Exposer une fonction Python comme outil via `@tool` (rôle de la docstring)
- Gérer une conversation avec checkpointer et `thread_id`
- Streamer des tokens dans le terminal
- Écrire un system prompt efficace (règles, format, garde-fous)

---

## 🔗 Ressources

- [Documentation LangChain](https://docs.langchain.com/)
- [Documentation LangGraph](https://docs.langchain.com/oss/python/langgraph/overview)
- [uv — Documentation](https://docs.astral.sh/uv/)
- [Tavily — Documentation](https://docs.tavily.com/)
- [OpenRouter — Modèles](https://openrouter.ai/models)

---

## 📝 Licence

Projet personnel d'apprentissage — libre d'utilisation et de modification.
Aucun fichier `LICENSE` n'est fourni à ce jour : il ne s'agit donc pas d'une
licence formelle.
