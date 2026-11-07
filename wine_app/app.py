import json
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from sklearn import metrics

BASE = Path(__file__).parent
FEATURES = ['fixed_acidity', 'volatile_acidity', 'citric_acid', 'residual_sugar', 'chlorides', 'free_sulfur_dioxide', 'total_sulfur_dioxide', 'density', 'pH', 'sulphates', 'alcohol', 'is_red']


@st.cache_resource
def load_model():
    return joblib.load(BASE / 'model.joblib')


@st.cache_data
def load_test():
    return pd.read_csv(BASE / 'test.csv')


@st.cache_data
def get_test_probabilities(_model, X):
    return _model.predict_proba(X)[:, 1]


model = load_model()
test = load_test()
config = json.loads((BASE / 'config.json').read_text())
threshold_default = float(config['threshold'])
with st.sidebar:
    threshold = st.slider('Порог хорошего вина', 0.0, 1.0, threshold_default, 0.01, key='threshold')

single_tab, metrics_tab, batch_tab, weights_tab = st.tabs(['Одно вино', 'Модельные метрики', 'Пакетная загрузка', 'Что выучила модель'])

with single_tab:
    st.subheader('Оценка одного вина')
    values = {}
    cols = st.columns(2)
    for i, feature in enumerate(FEATURES):
        series = test[feature]
        if feature == 'is_red':
            values[feature] = int(cols[i % 2].selectbox('Цвет вина', ['Белое', 'Красное']) == 'Красное')
        else:
            low, high = float(series.min()), float(series.max())
            values[feature] = cols[i % 2].number_input(feature, min_value=low, max_value=high, value=float(series.median()))
    if st.button('Оценить вино'):
        row = pd.DataFrame([values], columns=FEATURES)
        probability = float(model.predict_proba(row)[:, 1][0])
        st.metric('Вероятность хорошего вина', f'{probability:.2%}')
        st.success('Рекомендуем в подборку' if probability >= threshold else 'Не включаем в подборку')

with metrics_tab:
    st.subheader('Качество на тестовой выборке')
    X_test = test[FEATURES]
    y_test = test['target'].to_numpy()
    probabilities = get_test_probabilities(model, X_test)
    predictions = (probabilities >= threshold).astype(int)
    cm = metrics.confusion_matrix(y_test, predictions, labels=[0, 1])
    confusion_display = metrics.ConfusionMatrixDisplay(cm, display_labels=['Обычное', 'Хорошее'])
    confusion_display.plot()
    st.pyplot(confusion_display.figure_)
    c1, c2, c3 = st.columns(3)
    c1.metric('Precision', f'{metrics.precision_score(y_test, predictions, zero_division=0):.3f}')
    c2.metric('Recall', f'{metrics.recall_score(y_test, predictions, zero_division=0):.3f}')
    c3.metric('F1', f'{metrics.f1_score(y_test, predictions, zero_division=0):.3f}')
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    fpr, tpr, _ = metrics.roc_curve(y_test, probabilities)
    axes[0].plot(fpr, tpr)
    fpr_point = np.mean((probabilities >= threshold) & (y_test == 0)) / max(np.mean(y_test == 0), 1e-12)
    tpr_point = np.mean((probabilities >= threshold) & (y_test == 1)) / max(np.mean(y_test == 1), 1e-12)
    axes[0].scatter([fpr_point], [tpr_point], color='red')
    axes[0].set(xlabel='False positive rate', ylabel='True positive rate', title='ROC')
    precision_curve, recall_curve, pr_thresholds = metrics.precision_recall_curve(y_test, probabilities)
    axes[1].plot(recall_curve, precision_curve)
    point_precision = metrics.precision_score(y_test, predictions, zero_division=0)
    point_recall = metrics.recall_score(y_test, predictions, zero_division=0)
    axes[1].scatter([point_recall], [point_precision], color='red')
    axes[1].set(xlabel='Recall', ylabel='Precision', title='Precision-Recall')
    st.pyplot(fig)
    st.caption('При увеличении порога в подборку попадет меньше вин, обычно precision вырастет, а recall снизится. При уменьшении порога подборка станет шире.')

with batch_tab:
    st.subheader('Пакетное предсказание')
    uploaded = st.file_uploader('Загрузите CSV с признаками вин', type='csv')
    if uploaded is not None:
        batch = pd.read_csv(uploaded)
        missing = [col for col in FEATURES if col not in batch.columns]
        if missing:
            st.error('В CSV не хватает столбцов: ' + ', '.join(missing))
        else:
            probs = model.predict_proba(batch[FEATURES])[:, 1]
            result = batch.copy()
            result['probability_good'] = probs
            result['recommend'] = probs >= threshold
            st.dataframe(result)
            st.download_button('Скачать результаты', result.to_csv(index=False).encode('utf-8'), 'wine_predictions.csv', 'text/csv')

with weights_tab:
    st.subheader('Коэффициенты логистической регрессии')
    estimator = model.steps[-1][1]
    coefficients = pd.Series(estimator.coef_.ravel(), index=FEATURES).sort_values()
    fig, ax = plt.subplots(figsize=(8, 5))
    coefficients.plot.barh(ax=ax)
    ax.set_xlabel('Коэффициент после стандартизации')
    st.pyplot(fig)
    st.write('Положительные коэффициенты повышают оценку вероятности хорошего вина, отрицательные понижают ее.')
