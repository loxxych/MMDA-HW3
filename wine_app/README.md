# Wine Quality

Приложение оценивает вероятность того, что вино хорошее, показывает метрики модели и позволяет обработать CSV с несколькими винами.

## Приложение

Опубликованная версия: [mmda-hw3-loxxych.streamlit.app](https://mmda-hw3-loxxych.streamlit.app/).


## Локальный запуск

Нужен Python 3.9. Из папки `wine_app` выполнить:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Для Windows: `py -3.9 -m venv .venv`, затем `.venv\Scripts\activate`.

## Устройство приложения

Модель загружается через `st.cache_resource`, потому что это один переиспользуемый объект. Таблица и рассчитанные вероятности кэшируются через `st.cache_data`, так как это данные. Без кэша модель загружалась бы с диска, а вероятности на тесте пересчитывались бы при каждом изменении интерфейса.
