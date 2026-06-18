# Deployment

Этот проект деплоится через GitHub Actions:

1. Первая job собирает Docker-образ и пушит его в GitHub Container Registry.
2. Вторая job подключается к удаленному серверу по SSH, скачивает свежий образ и перезапускает контейнер.

Workflow находится в файле `.github/workflows/deploy.yml`.

## Что нужно на сервере

На удаленном сервере должны быть установлены:

- Docker
- доступ по SSH
- пользователь, который может запускать команды `docker`

Проверить Docker на сервере можно командой:

```bash
docker --version
```

## GitHub Secrets

В репозитории нужно добавить secrets:

```text
SSH_HOST
SSH_USER
SSH_PRIVATE_KEY
SSH_PORT
GHCR_USERNAME
GHCR_TOKEN
```

Описание secrets:

- `SSH_HOST` - IP-адрес или домен сервера.
- `SSH_USER` - пользователь для подключения по SSH.
- `SSH_PRIVATE_KEY` - приватный SSH-ключ для подключения к серверу.
- `SSH_PORT` - SSH-порт сервера, обычно `22`.
- `GHCR_USERNAME` - GitHub username или organization account, который имеет доступ к образу.
- `GHCR_TOKEN` - GitHub token с правом `read:packages`.

## GitHub Container Registry

Образ публикуется в GHCR в формате:

```text
ghcr.io/<owner>/<repo>:<commit-sha>
ghcr.io/<owner>/<repo>:latest
```

Например:

```text
ghcr.io/my-user/server-time-api:latest
```

Для публикации образа workflow использует встроенный `GITHUB_TOKEN`.

## Как запускается деплой

Деплой запускается автоматически при push в ветку `main`.

Также его можно запустить вручную:

1. Открыть GitHub repository.
2. Перейти во вкладку `Actions`.
3. Выбрать workflow `Build and deploy`.
4. Нажать `Run workflow`.

## Что делает deploy job

На сервере выполняются команды:

```bash
echo "$GHCR_TOKEN" | docker login ghcr.io -u "$GHCR_USERNAME" --password-stdin
docker pull "$IMAGE:$TAG"
docker stop "$CONTAINER_NAME" || true
docker rm "$CONTAINER_NAME" || true
docker run -d --name "$CONTAINER_NAME" --restart unless-stopped -p "$CONTAINER_PORT:$CONTAINER_PORT" "$IMAGE:$TAG"
docker image prune -f
```

Контейнер запускается с параметрами:

```text
name: server-time-api
port: 8000
restart policy: unless-stopped
```

После успешного деплоя API будет доступно по адресу:

```text
http://<server-ip>:8000
```

## Проверка после деплоя

Проверить приложение можно командами:

```bash
curl http://<server-ip>:8000/
curl http://<server-ip>:8000/time
curl http://<server-ip>:8000/date
```

Проверить контейнер на сервере:

```bash
docker ps
docker logs server-time-api
```

## Частые проблемы

Если сервер не может скачать образ из GHCR, проверьте:

- secret `GHCR_USERNAME`
- secret `GHCR_TOKEN`
- права token на `read:packages`
- доступность package в GitHub Container Registry

Если контейнер не запускается, проверьте:

- установлен ли Docker
- свободен ли порт `8000`
- есть ли права на запуск `docker` у SSH-пользователя
- вывод команды `docker logs server-time-api`
