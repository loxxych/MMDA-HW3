# Wine Quality

Локальное приложение для оценки качества вина и просмотра метрик модели.

Нужен Python 3.9. Перейдите в папку `wine_app`, установите зависимости и запустите приложение:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Windows: активируйте окружение командой `.venv\\Scripts\\activate`.

Для деплоя на Streamlit Community Cloud укажите эту папку как корень приложения и файл `app.py` как entry point. Добавьте файлы `model.joblib`, `config.json` и `test.csv`, созданные ноутбуком.

Модель загружается через `st.cache_resource`, потому что это один переиспользуемый объект. Таблица и готовые вероятности кэшируются через `st.cache_data`, так как это данные, которые Streamlit может безопасно хранить и копировать для повторных запусков. Без кэша `joblib.load` и расчет вероятностей запускались бы при каждом изменении интерфейса.
