# Data

This directory contains the anonymized judicial event logs analyzed by the MPV-TraC experiment, the anonymization script used to derive them from the Codex source records, and the activity-name translation table.

## Source

The raw records come from the **Codex data lake**, maintained by the Brazilian National Council of Justice (CNJ). Codex consolidates, in structured form, public-process data from courts across the country. The records used here cover **18 first-instance judicial units across six competences** of the Brazilian Judiciary, as reported in the multi-competence extension of Araújo et al. (2025, *Artificial Intelligence and Law*).

## Anonymization

The scripts in `anonymization/` document the procedure applied on top of the Codex source data. The CNJ Codex itself already restricts access to public-process data and pre-anonymizes the case parties; the two scripts in this repository implement the additional anonymization steps described in the paper, namely:

- Removal of party names and other personally identifying free-text fields
- Replacement of original NPU (Unified Process Number) with synthetic identifiers
- Replacement of user identifiers with random hashes
- Replacement of all source-system identifiers by dense sequential integers, per log (`anonymization/renumber_ids.py`): the case identifier `processoID` is numbered 0…N−1 in chronological order of each case's first event, and, in Schema A, the event identifier `id` (0…M−1, row order) and the document identifier `documentoID` (order of first appearance) likewise. The new values are not a function of the source keys and the mapping was not retained, so the logs cannot be joined back to the source records
- Preservation of structural attributes needed for process mining (case ID, activity label, timestamps, judicial class, judicial subject, movement code, complement)

The resulting files in [`event_logs/`](event_logs/) are the **cleaned, anonymized event logs** distributed under CC-BY-4.0.

## Storage format

Event logs are stored as **gzip-compressed CSV** (`.csv.gz`), which reduces their total footprint to about 13% of the uncompressed size. The `pandas` library reads and writes this format transparently from the file extension:

```python
import pandas as pd
df = pd.read_csv("data/event_logs/civel_1_cleaned.csv.gz")
```

No additional arguments or libraries are required.

## File schema

Each CSV in `event_logs/` follows one of two schemas, depending on the source competence:

### Schema A (JECs — T1)

| column | type | description |
|---|---|---|
| `id` | int | event identifier, sequential (0…M−1) in row order |
| `processoID` | int | case identifier, sequential (0…N−1) in chronological order of the case's first event |
| `Case` | string | synthetic NPU (Unified Process Number) |
| `activity` | string | judicial movement label (English; see `translation/activity_translation.csv`) |
| `duration` | int | duration in seconds (atomic event spans the closing timestamp) |
| `dataInicio` | datetime | event start timestamp |
| `dataFinal` | datetime | event end timestamp |
| `usuarioID` | int | anonymized user (court officer) identifier |
| `documentoID` | int | document identifier, sequential in order of first appearance (empty when absent) |
| `movimentoID` | int | TPU (Tabela Processual Unificada) movement code |

### Schema B (other competences — T2, T3, T4, T5, T7)

| column | type | description |
|---|---|---|
| `processoID` | int | case identifier, sequential (0…N−1) in chronological order of the case's first event |
| `activity` | string | judicial movement label (English; see `translation/activity_translation.csv`) |
| `dataInicio` | datetime | event start timestamp |
| `dataFinal` | datetime | event end timestamp |
| `classe` | string | judicial class (preserved in Portuguese, TPU code) |
| `assunto` | string | judicial subject (preserved in Portuguese, TPU code) |
| `movimentoID` | float | TPU movement code |
| `complemento` | string | TPU movement complement (preserved in Portuguese) |

## Unit ↔ file mapping

The 18 units used in the experiment are coded **TXUY** in the paper. The mapping to the CSV filenames in this repository is:

| Code | Competence | CSV file |
|---|---|---|
| T1U1 | Special Civil Courts | `juizados_1_cleaned.csv.gz` |
| T1U2 | Special Civil Courts | `juizados_2_cleaned.csv.gz` |
| T1U3 | Special Civil Courts | `juizados_3_cleaned.csv.gz` |
| T2U1 | Ordinary Civil | `civel_1_cleaned.csv.gz` |
| T2U2 | Ordinary Civil | `civel_2_cleaned.csv.gz` |
| T2U3 | Ordinary Civil | `civel_3_cleaned.csv.gz` |
| T3U1 | Criminal | `criminal_1_cleaned.csv.gz` |
| T3U2 | Criminal | `criminal_2_cleaned.csv.gz` |
| T3U3 | Criminal | `criminal_3_cleaned.csv.gz` |
| T4U1 | Electoral | `eleitoral_1_cleaned.csv.gz` |
| T4U2 | Electoral | `eleitoral_2_cleaned.csv.gz` |
| T4U3 | Electoral | `eleitoral_3_cleaned.csv.gz` |
| T5U1 | Treasury | `fazenda_1_cleaned.csv.gz` |
| T5U2 | Treasury | `fazenda_2_cleaned.csv.gz` |
| T5U3 | Treasury | `fazenda_3_cleaned.csv.gz` |
| T7U1 | Labor | `trabalho_1_cleaned.csv.gz` |
| T7U2 | Labor | `trabalho_2_cleaned.csv.gz` |
| T7U3 | Labor | `trabalho_3_cleaned.csv.gz` |

Filenames are sequential within each competence (`1`, `2`, `3`) and carry no information about the source courts or judicial units: no court, unit, or other originating identifier is encoded in the filenames, in the file contents, or anywhere else in this repository. The `TXUY` codes above are the anonymous labels used in the paper, and the numeric suffix of each filename matches the `UY` index.

### Scope note

The experiment covers six competences of the Brazilian Judiciary; the Military Justice (Justiça Militar) was **not** part of the study and no units from that competence are included in this repository. Some CSVs contain incidental string matches of the word `militar` in their `assunto` (subject) column — these are legitimate TPU subject codes for Labor and Treasury cases whose legal matter involves military police personnel or military jurisdictional issues (e.g., "Policial Militar e Civil", "Competência da Justiça Militar dos Estados", "Tempo de serviço militar"). They are case attributes of the included units, not references to the excluded Military Justice competence, and are preserved as part of the data integrity.

## Activity name translation

Each event log was originally extracted with activity labels in Brazilian Portuguese (judicial movement names). For consistency with the published paper, the `activity` column has been **translated to English** following the canonical vocabulary established in Araújo et al. (2025).

The full translation table is in [`translation/activity_translation.csv`](translation/activity_translation.csv) and covers **263 unique activities** (100% of events). Each entry has a `source` field with the following values:

| source | meaning |
|---|---|
| `paper` | explicit translation appearing in Araújo et al. (2025) |
| `paper-ext` | extension of an Art. 1 translation to a closely related label |
| `tpu` | standardized term from CNJ's Tabela Processual Unificada |
| `legal` | established Brazilian-Portuguese legal-to-English translation |
| `literal` | best-effort literal rendering for rare activities |

The original Portuguese labels are preserved in `event_logs_original_pt/` for reproducibility and downstream domain analysis.

## Reproducing the translation

Run from the repository root:

```bash
python _translate_event_logs.py
```

The script reads from `event_logs_original_pt/` (which holds the PT-BR backups) and overwrites the files in `event_logs/` with the translated `activity` column. The translation dictionary is hard-coded at the top of the script for full auditability.
