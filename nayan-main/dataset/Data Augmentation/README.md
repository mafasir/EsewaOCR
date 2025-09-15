# OCR Error Simulation for Dataset Preparation

The scripts in this folder introduces realistic OCR-like errors into a clean text dataset. This process, known as data augmentation, helps in training more robust and resilient machine learning models for OCR post-correction tasks.

The goal is to make a model that can fix errors from a real OCR engine by showing it how to handle artificially created mistakes during training.

---

## Simulated Error Types

The script can simulate several types of common OCR errors, including:

* **Character Substitution:** Swapping visually similar characters (e.g., `o` -> `0`, `l` -> `1`, `S` -> `5`).
* **Word Merging:** Incorrectly joining adjacent words (e.g., `John Smith` -> `JohnSmith`).
* **Word Splitting:** Incorrectly splitting a single word (e.g., `William` -> `Will iam`).
* **Character Splitting/Merging:** Misinterpreting multi-stroke characters (e.g., `m` -> `rn`, `d` -> `cl`).
* **Insertions & Deletions:** Adding random noise characters or completely missing others.

---

##  Devanagari Script

The simulation logic is adapted for Devanagari scripts. 

**Devanagari Error Examples:**
* **Character Confusion:** `भ` (bha) vs. `म` (ma), `ण` (ṇa) vs. `ण` (ṇa with a different stroke), `घ` (gha) vs. `ध` (dha).
* **Matra (Vowel Sign) Errors:** Missing or incorrect vowel signs, like misreading `कि` as `क`.
* **Compound Character Errors:** Incorrectly segmenting complex conjuncts.
