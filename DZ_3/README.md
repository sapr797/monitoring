Домашнее задание к занятию 15 «Система сбора логов Elastic Stack»

## Задание 1
Вам необходимо поднять в Docker и связать между собой:
- **Elasticsearch** (горячая и теплая ноды)
- **Logstash**
- **Kibana**
- **Filebeat**

**Требования:**
- Logstash должен быть сконфигурирован для приёма по TCP JSON-сообщений.
- Filebeat должен быть настроен на отправку логов Docker контейнеров вашей системы в Logstash.
- В директории `help` находятся манифест `docker-compose` и конфигурации Filebeat/Logstash для быстрого выполнения задания. Вы можете использовать их или создать свои.

**Результат выполнения задания 1:**
- Скриншот `docker ps` через 5 минут после запуска всех контейнеров (должно быть 5 контейнеров).
- Скриншот интерфейса Kibana.
- Файл `docker-compose.yml` (если вы не использовали готовый из `help`).
- Ваши YAML-конфигурации для стека (если не использовали готовые).

## Задание 2
1. Перейдите в меню создания **index patterns** (теперь **Data Views**) в Kibana и создайте несколько index patterns из имеющихся индексов.
2. Перейдите в меню просмотра логов в Kibana (**Discover**) и изучите, как отображаются логи и как производить поиск по логам.
3. В манифесте директории `help` также приведено **dummy-приложение**, которое генерирует случайные события в stdout контейнера. Эти логи должны попадать в индекс `logstash-*` в Elasticsearch. Если этого индекса нет — воспользуйтесь советами и источниками из раздела «Дополнительные ссылки».

**Дополнительные ссылки:**
- [Создание pipeline в Logstash](https://www.elastic.co/guide/en/logstash/current/configuration.html)
- [Условные выражения в Logstash](https://www.elastic.co/guide/en/logstash/current/event-dependent-configuration.html#conditionals)
- [Устранение неполадок обнаружения в Elasticsearch](https://www.elastic.co/guide/en/elasticsearch/reference/8.11/discovery-troubleshooting.html)

---

## Состав стека и версии
- **Elasticsearch:** 8.11.0 (две ноды: `elasticsearch-hot` и `elasticsearch-warm`)
- **Logstash:** 8.11.0
- **Kibana:** 8.11.0
- **Filebeat:** 8.11.0
- **Dummy-app:** alpine:latest (генерирует случайные логи в stdout)

## Структура файлов в директории `DZ_3`
DZ_3/
├── docker-compose.yml # Манифест для запуска всех контейнеров (включая dummy-app)
├── filebeat.yml # Конфигурация Filebeat
├── logstash.conf # Конфигурация Logstash (помещается в /usr/share/logstash/pipeline/)
├── README.md # Данный файл с инструкцией
└── screenshots/ # Папка со скриншотами (создать вручную)
├── docker_ps.png # Скриншот вывода команды docker ps
└── kibana_discover.png # Скриншот интерфейса Kibana с логами

text

## Инструкция по запуску

### 1. Подготовка
Проверка- на хосте установлены Docker и Docker Compose, копируем все файлы из этой директории (`DZ_3`) на свою виртуальную или локальную машину.

### 2. Запуск контейнеров

docker-compose up -d
Docker скачает необходимые образы и запустит контейнеры в фоновом режиме.

3. Проверка статуса
 все 6 контейнеров успешно запущены (5 основных + dummy-app):

docker ps

Проверка работоспособности
1. Доступность Elasticsearch
 запрос к API горячей ноды:

curl localhost:9200

Должен вернуться JSON с информацией о кластере и версии. Для тёплой ноды используйте порт 9201.

2. Проверка индексов
 1–2 минуты после запуска -наличие индексов filebeat-* и logstash-*:

curl -s localhost:9200/_cat/indices | grep -E "filebeat|logstash"

3. Доступ к Kibana
Откройте в браузере адрес http://<IP-вашего-сервера>:5601. Если Kibana запускается локально, используйте http://localhost:5601.

Создание Data View (индексных шаблонов)
Переходим в Stack Management → Data Views.

Нажмаем Create data view.
Для индекса filebeat-*:
Name: Filebeat logs
Index pattern: filebeat-*
Timestamp field: @timestamp
Create data view.

Для индекса logstash-*:
Name: Logstash logs
Index pattern: logstash-*
Timestamp field: @timestamp
Create data view.

Просмотр логов
Discover, выбираем Data View - логи отображаются. Для логов dummy-app  появляются в индексе logstash-*.

Скриншоты для отчёта
в папке screenshots/.

docker_ps.png — вывод команды docker ps через 5 минут после запуска всех контейнеров.
 На скриншоте должно быть видно 6 работающих контейнеров (5 основных + dummy-app).
kibana_discover.png — интерфейс Kibana в разделе Discover, отображающий логи из индекса logstash-* (или filebeat-*).
