# Домашнее задание 14: Мониторинг (Prometheus + Grafana)

**Студент:** [Ваше имя]
**Репозиторий:** [https://github.com/sapr797/monitoring/](https://github.com/sapr797/monitoring/)

## Задание 1. Запуск стека Prometheus + Grafana

Был развернут стек мониторинга с помощью `docker-compose.yml`, включающий:
- **Prometheus** (для сбора метрик)
- **Node Exporter** (для сбора метрик хоста)
- **Grafana** (для визуализации)

Все сервисы запущены в одной сети `monitor-net`. Конфигурация Prometheus задается через файл `prometheus.yml`, который маппится в контейнер.

**Результат:**
- Grafana доступна по адресу `http://89.169.135.18:3000` (логин/пароль: admin/admin).
- Prometheus доступен по адресу `http://89.169.135.18:9090/targets`, цель `nodeexporter:9100` в статусе **UP**.

**Файлы:**
- `docker-compose.yml`
- `prometheus/prometheus.yml`

## Задание 2. Создание дашборда с панелями

В Grafana был создан пользовательский дашборд, на котором размещены четыре панели для ключевых метрик сервера:

1.  **Утилизация CPU (в процентах)**
    *   **PromQL:** `100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle", job="nodeexporter"}[$__rate_interval])) * 100)`
    *   **Описание:** Показывает процент загруженности процессора (сумма времени user, system и т.д. за вычетом idle).

2.  **Load Average (LA 1/5/15 минут)**
    *   **PromQL (для LA1):** `node_load1{job="nodeexporter"}`
    *   **PromQL (для LA5):** `node_load5{job="nodeexporter"}`
    *   **PromQL (для LA15):** `node_load15{job="nodeexporter"}`
    *   **Описание:** Отображает среднюю нагрузку на систему за 1, 5 и 15 минут.

3.  **Свободная оперативная память**
    *   **PromQL (в процентах):** `(node_memory_MemFree_bytes{job="nodeexporter"} / node_memory_MemTotal_bytes{job="nodeexporter"}) * 100`
    *   **Описание:** Показывает процент свободной оперативной памяти.

4.  **Свободное место на корневой файловой системе (/)**
    *   **PromQL (в процентах):** `(node_filesystem_free_bytes{mountpoint="/", job="nodeexporter"} / node_filesystem_size_bytes{mountpoint="/", job="nodeexporter"}) * 100`
    *   **Описание:** Отображает процент свободного дискового пространства на разделе `/`.

## Задание 3. Создание правил алертов (Alerting)

Для каждой из четырех панелей были настроены правила оповещения в Grafana Alerting. Правила срабатывают при превышении (или понижении) критических порогов в течение заданного времени.

1.  **High CPU Usage**
    *   **Условие:** Значение CPU > 80% в течение 5 минут.
    *   **Запрос:** `100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle", job="nodeexporter"}[$__rate_interval])) * 100)`
    *   **Порог:** > 80
    *   **Severity:** `warning`

2.  **High Load Average**
    *   **Условие:** Значение Load Average за 1 минуту > 4.0 в течение 5 минут (значение подобрано под 4-ядерную систему).
    *   **Запрос:** `node_load1{job="nodeexporter"}`
    *   **Порог:** > 4.0
    *   **Severity:** `warning`

3.  **Low Free Memory**
    *   **Условие:** Свободная RAM < 10% в течение 5 минут.
    *   **Запрос:** `(node_memory_MemFree_bytes{job="nodeexporter"} / node_memory_MemTotal_bytes{job="nodeexporter"}) * 100`
    *   **Порог:** < 10
    *   **Severity:** `critical`

4.  **Low Disk Space**
    *   **Условие:** Свободное место на корневом разделе < 10% в течение 5 минут.
    *   **Запрос:** `(node_filesystem_free_bytes{mountpoint="/", job="nodeexporter"} / node_filesystem_size_bytes{mountpoint="/", job="nodeexporter"}) * 100`
    *   **Порог:** < 10
    *   **Severity:** `critical`

Для отправки уведомлений был настроен SMTP (Gmail) с использованием пароля приложения. Контактная точка `Gmail` добавлена в правила.

## Задание 4. (Опционально или дополнительное)

*(Если в задании был четвертый пункт, опишите его здесь. Если нет, этот раздел можно удалить.)*

Например:
*   Настроена интеграция с Telegram для получения уведомлений.
*   Создан дополнительный дашборд для мониторинга Docker-контейнеров.
*   И т.д.

## Используемые файлы конфигурации

- [`docker-compose.yml`](docker-compose.yml) — файл оркестрации всех сервисов.
- [`prometheus/prometheus.yml`](prometheus/prometheus.yml) — конфигурация Prometheus (цели для сбора метрик).

## Скриншоты
