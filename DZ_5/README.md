# Домашнее задание к занятию 15 «Система сбора логов Elastic Stack»

## Выполненные задачи

### ✅ Задание 1. Поднятие и настройка ELK-стека

Подняты и связаны между собой следующие сервисы в Docker:
- **Elasticsearch** (hot нода) — хранение и индексация логов
- **Logstash** — приём и обработка логов по TCP
- **Kibana** — визуализация и анализ логов
- **Filebeat** — сбор логов Docker-контейнеров

#### Скриншот `docker ps` через 5 минут после старта
рис.003+.png. рис.005+.png

#### Скриншот интерфейса Kibana
![Kibana Discover](рис.008.png, рис.00.png,рис.011.png)

---

### ✅ Задание 2. Работа с индексами и просмотр логов

1. **Создание index-patterns в Kibana**
   - Создан индексный паттерн `logstash-*` для просмотра логов
   - Поле времени: `@timestamp`

2. **Просмотр логов в Discover**
   - Логи успешно отображаются в Kibana
   - Доступен поиск по полям и содержимому``
   - Изучены основные возможности фильтрации и анализа

---Команды для запуска и проверки
Запуск стека

cd ~/elk-stack
docker compose up -d
Проверка работающих контейнеров

docker ps
Проверка индексов в Elasticsearch

curl http://localhost:9200/_cat/indices
Просмотр логов Filebeat

docker logs filebeat --tail 20
Просмотр логов Logstash

docker logs logstash --tail 30
Проверка доступности Kibana

curl -I http://localhost:5601
Результаты работы
Созданные индексы в Elasticsearch

yellow open logstash-2026.03.30 1 1 55110 0 78.5mb
Доступные сервисы
Kibana: http://84.252.130.220:5601

Elasticsearch API: http://localhost:9200

Logstash TCP input: порт 5000

Logstash metrics: порт 9600

Количество запущенных контейнеров (5+)
elasticsearch-hot

elasticsearch-warm

logstash

kibana

filebeat

dummy-app (дополнительный)

Решённые проблемы
1. Ошибка прав доступа Filebeat
Проблема: config file must be owned by root
Решение:

sudo chown root:root filebeat/filebeat.yml
sudo chmod 644 filebeat/filebeat.yml
2. Нехватка памяти Elasticsearch
Проблема: Контейнеры падали из-за нехватки памяти
Решение: Ограничено использование памяти через ES_JAVA_OPTS=-Xms128m -Xmx128m

3. Kibana не отвечала по публичному IP
Проблема: Порт 5601 был закрыт
Решение: Настроена группа безопасности в облаке (порты 22 и 5601)

4. Logstash не мог подключиться к Elasticsearch
Проблема: Ошибка разрешения имён в Docker-сети
Решение: Использован правильный network driver bridge и имена сервисов как хосты

Выводы
ELK-стек успешно развёрнут в Docker

Все сервисы связаны и работают стабильно

Логи Docker-контейнеров собираются Filebeat и передаются в Logstash

Logstash обрабатывает JSON-логи и отправляет в Elasticsearch

Kibana позволяет просматривать и анализировать логи в реальном времени

Созданы необходимые индексные паттерны для работы с данными

Дополнительные команды
Остановка всех сервисов

docker compose down
Просмотр логов всех сервисов в реальном времени

docker compose logs -f
Создание резервной копии конфигурации

tar -czf elk-backup-$(date +%Y%m%d).tar.gz docker-compose.yml filebeat/ logstash/
Очистка старых индексов (старше 7 дней)

curl -X DELETE "http://localhost:9200/logstash-$(date -d '7 days ago' +%Y.%m.%d)*"

