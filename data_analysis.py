import pandas as pd
import numpy as np
from sklearn import metrics
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import seaborn as sns
import os

# CONFIGURAZIONE PERCORSI E PARAMETRI
FILE_RISULTATI = 'risultati.xlsx'
FILE_METADATI  = 'metadati.xlsx'
FOLDER_OUTPUT  = 'grafici'
CLASSI = ['REAL', 'VIRTUAL']

if not os.path.exists(FOLDER_OUTPUT):
    os.makedirs(FOLDER_OUTPUT)

PARAMETRI = ['Età']
METRICHE = ['Accuracy','Precision', 'Recall', 'F1-score']

# La funzione accetta DataFrame coi dati, titolo, nome file e folder di salvataggio; stampa il report, salva i file e restituisce dizionario del report
def analisi_dati (df_target, titolo, nome_file, folder=FOLDER_OUTPUT):
    y_true = df_target['y_true']
    y_pred = df_target['y_pred']
    
    print(f"\n" + "="*40)
    print(f">>>> ANALISI {titolo} <<<<")
    print("="*40)
    
    # Calcolo matrici di confusione e stampa report
    matrix = metrics.confusion_matrix(y_true, y_pred, labels=CLASSI)
    matrix_norm = metrics.confusion_matrix(y_true, y_pred, labels=CLASSI, normalize='true')
    print("\n---------- REPORT ----------")
    print(metrics.classification_report(y_true, y_pred, labels=CLASSI, target_names=CLASSI, zero_division=0))
    
    # Matrice di Confusione Valori Assoluti
    fig, ax = plt.subplots(figsize=(7, 6))
    disp = metrics.ConfusionMatrixDisplay(confusion_matrix=matrix, display_labels=CLASSI)
    disp.plot(cmap='Purples', values_format='d', ax=ax)
    ax.set_title(f'Matrice di Confusione\n{titolo}', fontsize=12, fontweight='bold', pad=15)
    ax.set_xlabel('Risposta (Predetto)')
    ax.set_ylabel('Verità (Reale)')
    plt.tight_layout()
    plt.savefig(os.path.join(folder, f"CM_{nome_file}.pdf"))
    plt.close(fig) 
    
    # Matrice Confusione Normalizzata
    fig_norm, ax_norm = plt.subplots(figsize=(7, 6))
    disp_norm = metrics.ConfusionMatrixDisplay(confusion_matrix=matrix_norm, display_labels=CLASSI)
    disp_norm.plot(cmap='Purples', values_format='.1%', ax=ax_norm) 
    ax_norm.set_title(f'Matrice di Confusione Normalizzata\n{titolo}', fontsize=12, fontweight='bold', pad=15)
    ax_norm.set_xlabel('Risposta (Predetto)')
    ax_norm.set_ylabel('Verità (Reale)')
    plt.tight_layout()
    plt.savefig(os.path.join(folder, f"CM_Normalized_{nome_file}.pdf"))
    plt.close(fig_norm) 
    
    # Report come dizionario e utilizzo di una Serie di Pandas che gestisca le colonne automaticamente
    report_dict = metrics.classification_report(y_true, y_pred, labels=CLASSI, output_dict=True, zero_division=0) 
    return pd.Series({
        'Accuracy': report_dict['accuracy'],
        'Precision': report_dict['macro avg']['precision'],
        'Recall': report_dict['macro avg']['recall'],
        'F1-score': report_dict['macro avg']['f1-score']
    })

df_metadati = pd.read_excel(FILE_METADATI) # tabella per i metadati
fogli_dict = pd.read_excel(FILE_RISULTATI, sheet_name=None, header=5) # dizionario (partecipante-tabella dei trial)
nomi_fogli = list(fogli_dict.keys())[:20] 
lista_df_partecipanti = []

# Ciclo sui partecipanti e pulizia dati
for i, nome_foglio in enumerate(nomi_fogli):
    df_foglio = fogli_dict[nome_foglio]
    df_slice = df_foglio.iloc[0:32].copy()

    df_slice['y_true'] = df_slice["Modalità"].map({'VIRTUAL': 'VIRTUAL', 'REALE': 'REAL'})
    df_slice['y_pred'] = df_slice["SÌ"].map({'x': 'VIRTUAL', np.nan: 'REAL'})
    
    # Mapping della confidence in modo uniforme nel range 0-1
    punti_scala = np.linspace(0, 1, 10)
    scala_real = punti_scala[:5][::-1]
    scala_virtual = punti_scala[5:]
    confidence = df_slice['Valutazione sicurezza']
    is_real = (df_slice['y_pred'] == 'REAL')
    df_slice['y_score'] = np.where(
        is_real,
        scala_real[confidence-1],
        scala_virtual[confidence-1]
    )
    
    # Copia metadati dell'i-esimo partecipante in una colonna del df dei risultati
    df_slice[df_metadati.columns] = df_metadati.iloc[i].values 
    lista_df_partecipanti.append(df_slice)

df_master = pd.concat(lista_df_partecipanti, ignore_index=True)
print(f"Totale prove analizzate: {len(df_master)}")

# ANALISI GLOBALE
analisi_dati(df_master, "Globale", "GLOBAL")

# ANALISI CICLICA PER PARAMETRI 
for param in PARAMETRI:
    subfolder = os.path.join(FOLDER_OUTPUT, param)
    os.makedirs(subfolder, exist_ok=True)
    dati_confronto = []
    for nome_cat, df_cat in df_master.groupby(param):
        nome = str(nome_cat).replace(" ", "_").replace("/", "-")
        res = analisi_dati(df_cat, f"{param}: {nome_cat}", f"{param}_{nome}", folder=subfolder)
        res['Gruppo'] = str(nome_cat)
        dati_confronto.append(res)
    
    # Creazione grafico comparativo tra le metriche
    if dati_confronto:
        df_plot = pd.DataFrame(dati_confronto)
        fig, ax = plt.subplots(figsize=(12, 7))
        ax_plot = df_plot.set_index('Gruppo')[METRICHE].plot(
            kind='bar', ax=ax,  width=0.8, 
            color=['#d1e0ec', '#a4c2d7', '#6697bc', '#2a6194'], rot=0
        )
        for container in ax.containers:
            ax.bar_label(container, padding=3, fmt='%.2f', fontsize=9)
        ax.set_ylim(0, 1.1) 
        ax.set_title(f'Confronto Metriche per {param}', fontsize=16, fontweight='bold', pad=20)
        ax.legend(title="Metriche", bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.savefig(os.path.join(subfolder, f"confronto_{param}.pdf"))
        plt.close(fig) 

# DATI GRAFICI ROC e PCR
yt_global = df_master['y_true'].map({'VIRTUAL': 1, 'REAL': 0})
baseline_precision = yt_global.mean()

# ROC Globale
fig_roc_global, ax_roc_global = plt.subplots(figsize=(8, 7))
fpr_global, tpr_global, _ = metrics.roc_curve(yt_global, df_master['y_score'])
auc_global = metrics.roc_auc_score(yt_global, df_master['y_score'])
ax_roc_global.plot(fpr_global, tpr_global, color='darkblue', lw=3, label=f'Globale (AUC = {auc_global:.2f})')
ax_roc_global.plot([0, 1], [0, 1], color='gray', linestyle='--')
ax_roc_global.set_title('ROC Curve Globale', fontsize=14, fontweight='bold')
ax_roc_global.set_xlabel('False Positive Rate (FPR)',labelpad=12)
ax_roc_global.set_ylabel('True Positive Rate (TPR)',labelpad=12)
ax_roc_global.legend(loc='lower right')
plt.savefig(os.path.join(FOLDER_OUTPUT, "ROC_Globale.pdf"))
plt.close(fig_roc_global)

# PRC Globale
fig_pr_global, ax_pr_global = plt.subplots(figsize=(8, 7))
prec_global, rec_global, _ = metrics.precision_recall_curve(yt_global, df_master['y_score'])
ap_global = metrics.average_precision_score(yt_global, df_master['y_score'])
ax_pr_global.plot(rec_global, prec_global, color='firebrick', lw=3, label=f'Globale (AP = {ap_global:.2f})')
ax_pr_global.axhline(y=baseline_precision, color='gray', linestyle='--', label='Baseline')
ax_pr_global.set_title('Precision-Recall Curve Globale', fontsize=14, fontweight='bold')
ax_pr_global.set_xlabel('Recall',labelpad=12)
ax_pr_global.set_ylabel('Precision',labelpad=12)
ax_pr_global.legend(loc='lower left')
plt.savefig(os.path.join(FOLDER_OUTPUT, "PRC_Globale.pdf"))
plt.close(fig_pr_global)

# Grafici parametrici
for param in PARAMETRI:
    subfolder_param = os.path.join(FOLDER_OUTPUT, param)
    os.makedirs(subfolder_param, exist_ok=True)
    fig_roc_param, ax_roc_param = plt.subplots(figsize=(10, 8))
    fig_pr_param, ax_pr_param = plt.subplots(figsize=(10, 8))
    
    # Divisione dati per categoria (groupby)
    for n, d in df_master.groupby(param):
        yt = d['y_true'].map({'VIRTUAL': 1, 'REAL': 0})
        if len(yt.unique()) > 1:
            # Calcoli ROC
            fpr, tpr, _ = metrics.roc_curve(yt, d['y_score'])
            auc_ind = metrics.roc_auc_score(yt, d['y_score'])
            ax_roc_param.plot(fpr, tpr, lw=1.5, alpha=0.7, label=f'{n} (AUC = {auc_ind:.2f})')
            # Calcoli PRC
            prec, rec, _ = metrics.precision_recall_curve(yt, d['y_score'])
            ap_ind = metrics.average_precision_score(yt, d['y_score'])
            ax_pr_param.plot(rec, prec, lw=1.5, alpha=0.7, label=f'{n} (AP = {ap_ind:.2f})')
    
    # Grafico ROC 
    ax_roc_param.plot([0, 1], [0, 1], color='gray', linestyle='--')
    ax_roc_param.set_title(f'Confronto ROC per {param}', fontsize=14, fontweight='bold')
    ax_roc_param.set_xlabel('False Positive Rate (FPR)',labelpad=12)
    ax_roc_param.set_ylabel('True Positive Rate (TPR)',labelpad=12)
    ax_roc_param.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='small')
    fig_roc_param.tight_layout()
    fig_roc_param.savefig(os.path.join(subfolder_param, f"ROC_Parametrico_{param}.pdf"))
    plt.close(fig_roc_param)
    
    # Grafico PRC 
    ax_pr_param.axhline(y=baseline_precision, color='gray', linestyle='--')
    ax_pr_param.set_title(f'Confronto Precision-Recall per {param}', fontsize=14, fontweight='bold')
    ax_pr_param.set_xlabel('Recall',labelpad=12)
    ax_pr_param.set_ylabel('Precision',labelpad=12)
    ax_pr_param.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='small')
    fig_pr_param.tight_layout()
    fig_pr_param.savefig(os.path.join(subfolder_param, f"PRC_Parametrico_{param}.pdf"))
    plt.close(fig_pr_param)

# Dati per ogni partecipante tramite ID 
risultati_per_soggetto = []
for id, df_sog in df_master.groupby('ID'):
    y_t = df_sog['y_true']
    y_p = df_sog['y_pred']
    report = metrics.classification_report(y_t, y_p, labels=CLASSI, output_dict=True, zero_division=0)  
    risultati_per_soggetto.append({
        'ID': id,
        'Accuracy': report['accuracy'],
        'Precision': report['macro avg']['precision'],
        'Recall': report['macro avg']['recall'],
        'F1-score': report['macro avg']['f1-score']
    })
    
# BOX PLOT
df_soggetti = pd.DataFrame(risultati_per_soggetto)
df_box = df_soggetti.melt(id_vars=['ID'], value_vars=METRICHE, var_name='Metrica', value_name='Valore')
plt.figure(figsize=(12, 7))
sns.set_theme(style="whitegrid")
sns.boxplot(data= df_box, x='Metrica', y='Valore', hue='Metrica', palette='Blues', width=0.5, fliersize=0)
plt.title('Variazione Metriche tra Soggetti', fontsize=14, fontweight='bold', pad = 20)
plt.ylim(0, 1.05)
plt.savefig(os.path.join(FOLDER_OUTPUT, "BoxPlot.pdf"))
plt.close()