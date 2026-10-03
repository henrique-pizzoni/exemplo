# exemplo

Exemplo simples de API de tarefas com FastAPI, separada em
**routes**, **services** e **repositories**.

## Estrutura

```
main.py                                      # cria o app e registra as rotas
app/
  models.py                                  # Task e TaskCreate (pydantic)
  routes/task_routes.py                      # HTTP: recebe request e traduz erro em status code
  services/task_service.py                   # regras de negocio (depende do repositorio)
  services/task_stats_service.py             # funcoes puras de estatistica
  repositories/task_repository.py            # le e escreve no arquivo tasks.json
tests/unit/
  test_task_service.py                       # testes do TaskService
  test_task_stats_service.py                 # testes do task_stats_service
```

A ideia da separacao:

- **route**: so cuida de HTTP (status code, path, query param).
- **service**: onde estao as regras de negocio. E a camada que a gente testa.
- **repository**: onde os dados ficam. Aqui, um arquivo `tasks.json` no disco.

## Rodando a API

```bash
fastapi dev main.py
```

| Metodo | Rota            | O que faz                          |
| ------ | --------------- | ---------------------------------- |
| POST   | `/tasks`        | cria uma tarefa (envia so o titulo) |
| GET    | `/tasks`        | lista as tarefas                    |
| GET    | `/tasks/stats`  | quantas feitas, pendentes e a %     |
| GET    | `/tasks/{id}`   | busca uma tarefa                    |

## Rodando os testes

```bash
pytest
```

## Sobre os testes

Os testes sao organizados pela **unidade testada**, nao pela tecnica usada.
Cada arquivo cobre uma unidade e tem uma classe com o nome dela
(`TaskService` -> `TestTaskService`). Todos os testes daquela unidade ficam
dentro dessa classe, usando mock ou nao.

Dentro da classe, cada metodo e um teste, e todos seguem os mesmos tres
passos, marcados com comentario:

1. **fixtures** — monta os dados e as dependencias
2. **processamento** — chama a funcao que esta sendo testada
3. **assertivas** — verifica o resultado

### Quando usar mock

O `JsonTaskRepository` le e escreve no arquivo `tasks.json`. Em teste unitario a
gente nao quer depender do disco (o arquivo pode nao existir, pode estar sujo de
outro teste, e o teste fica lento). Entao trocamos ele por um mock:

```python
repository = Mock(spec=JsonTaskRepository)      # finge ser o arquivo
repository.read_all.return_value = [Task(...)]  # "o arquivo tem isso aqui"
service = TaskService(repository)               # injeta no service
```

Isso so e possivel porque o `TaskService` recebe o repositorio no construtor
(injecao de dependencia).

O `spec=` amarra o mock na classe real: ele so aceita metodos que existem no
`JsonTaskRepository`. Sem isso, um erro de digitacao (`raed_all`) passaria
despercebido e o teste ficaria verde sem testar nada.

Com o mock da para fazer dois tipos de assertiva:

- no **retorno** do service: `assert tasks[0].title == "Estudar"`
- na **chamada** que o service fez: `repository.add.assert_called_once_with(...)`
  ou `repository.add.assert_not_called()`

### Quando nao usar mock

Quando nao existe dependencia externa no caminho testado:

- as funcoes de `task_stats_service` sao puras (recebem uma lista, devolvem um
  numero), entao nenhum teste delas usa mock;
- em `TaskService`, o titulo vazio e recusado antes de chegar no repositorio,
  entao esse teste tambem dispensa mock.

Compare os dois primeiros testes de `TestTaskService`: os dois cobrem o titulo
vazio. O sem mock so confirma que o erro foi lancado. O com mock vai alem e
prova que nada foi gravado no arquivo. E exatamente isso que o mock acrescenta.

## CI/CD com Jenkins

A pipeline tem tres etapas: **Build -> Test -> Deploy** (o deploy vai para o
Render e so roda na `main`).

- `docker-compose.yml` sobe o Jenkins ja configurado (`docker compose up -d --build`)
- `jenkins/plugins.txt` e `jenkins/casc.yaml` instalam os plugins e criam
  usuario, credenciais e o job, lendo os segredos do `.env` (copie do `.env.example`)
- `Jenkinsfile` define a pipeline e explica, no comeco do arquivo, o passo a
  passo (Render, `.env`, subir o Jenkins e ver funcionando)
