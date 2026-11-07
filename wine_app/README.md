# Wine Quality

Демо-приложение оценивает вероятность того, что вино хорошее, показывает метрики модели и позволяет обработать CSV с несколькими винами.

## Приложение

Опубликованная версия: [mmda-hw3-loxxych.streamlit.app](https://mmda-hw3-loxxych.streamlit.app/).

В GitHub entry point находится по пути `wine_app/app.py`. Для Community Cloud выбери репозиторий, ветку `main`, этот путь и Python 3.12. `requirements.txt` лежит рядом с приложением.

## Локальный запуск

Нужен Python 3.9. Из папки `wine_app` выполни:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

В Windows создай окружение командой `py -3.9 -m venv .venv`, затем активируй его командой `.venv\Scripts\activate`.

Для запуска нужны `model.joblib`, `config.json` и `test.csv`. Они уже лежат в этой папке и были созданы в ноутбуке HW3. Не добавляй в GitHub папку `.venv`.

## Устройство приложения

Модель загружается через `st.cache_resource`, потому что это один переиспользуемый объект. Таблица и рассчитанные вероятности кэшируются через `st.cache_data`, так как это данные. Без кэша модель загружалась бы с диска, а вероятности на тесте пересчитывались бы при каждом изменении интерфейса.
