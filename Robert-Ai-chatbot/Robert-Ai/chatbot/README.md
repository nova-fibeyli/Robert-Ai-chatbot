# Robert-Ai: Empathic Emotional Support Robo Friend

## Overview

**Robert-Ai** is an AI-powered **emotional support chatbot** designed to provide **empathetic** interactions. It utilizes **Multi-Query Retrieval, RAG Fusion, MongoDB, and Streamlit** to create **realistic** and **emotionally aware** conversations. Users can **ask questions, upload documents, and receive context-aware responses**.

---

## Installation

### 0. Create a Directory and Move the Project

Ensure that your project is stored in a dedicated directory on your system:

```bash
mkdir "C:\Users\<your-username>\Downloads\Robert-Ai-chatbot"
```

### **1. Clone the Repository**

```bash
git clone https://github.com/nova-fibeyli/Robert-Ai-chatbot.git
cd "C:\Users\<your-username>\Downloads\Robert-Ai-chatbot"
```

### **2. Install Required Dependencies**

```bash
pip install -r requirements.txt
```

### **3. Download the Ollama Model**

```bash
ollama pull mistral
```

---

## **Project Structure**

```
Main Application Code:
│── src/
│   ├── app.py        # Main chatbot application
│   ├── app_alt.py        # Alternitive chatbot application
│   ├── file_handler.py    # Handles file uploads & text extraction
│   ├── db_handler.py      # Manages MongoDB interactions
│   ├── query_manager.py   # Handles multi-query processing
│   ├── rag_fusion.py      # Implements Reciprocal Rank Fusion (RAG)
│   ├── dataset/
│   │   ├── constitution.json  # Legal document dataset
│
Testing Files:
│── test/
│   ├── test_app.py               # Tests the main app
│   ├── test_preprocess.py        # Data preprocessing
│   ├── test_verification.py      # Tests veriffication
│
Documentation and Requirements:
│── README.md
│── requirements.txt
│── LICENSE
```

---

## **Key Features**

### **🔹 Core Functionalities**

✅ **Multi-Query Retrieval** – Searches **multiple queries efficiently**  
✅ **Reciprocal Rank Fusion (RAG Fusion)** – Improves response accuracy  
✅ **MongoDB Integration** – Stores **all queries and answers** dynamically  
✅ **Streamlit UI** – Interactive chat interface  
✅ **Ollama AI Integration** – Runs locally for **AI-powered responses**  
✅ **File Upload & Document Querying**

- Supports **.txt, .pdf, .docx**
- Extracts **document content**
- Supports **multiple file** uploading
- **Ask questions based on uploaded files**
  ✅ **Datasets Used:**
- **EmpathicDialogues**: AI training data for **empathetic responses**
- **Constitution Dataset**: For **legal document-based assistance**

---

## **Usage Instructions**

### **1. Start the Chatbot**

```bash
cd src
streamlit run app.py
```

---

### **2. Upload Files & Interact**

- Type your **question** and click **Send**.
- Upload **.txt, .pdf, .docx** files for **context-aware answers**.
- Retrieve **document-specific insights** interactively.

---

### **3. Use Alternative Precision Mode**

For **more accurate** responses:

```bash
streamlit run src/app_alt3.py
```

---

## **Technologies Used**

| **Technology** | **Purpose**                           |
| -------------- | ------------------------------------- |
| **Python**     | Main programming language             |
| **MongoDB**    | Stores chat history & query responses |
| **Streamlit**  | Provides interactive chatbot UI       |
| **Ollama**     | AI-based conversation engine          |
| **PyMuPDF**    | Extracts text from PDFs               |
| **pymongo**    | Enables MongoDB communication         |
| **LlamaIndex** | Manages chat message history          |

---

## **🛠 MongoDB Setup**

### **Accessing MongoDB**

- **Email**: `magzhan.ikram@astanait.edu.kz`
- **Password**: `<your-password>`
- **Login URL**: [MongoDB Login](https://account.mongodb.com/account/login?signedOut=true)
- **Go here then** *https://cloud.mongodb.com/v2/677182969e97fe1106690865#/metrics/replicaSet/677183b107aecd340960ea9e/explorer/support_bot/dialogues/find*

## **Examples**

### **Example 1: Basic Conversation**

```
User: Hi Robert-Ai, I feel a bit down today.
Robert-Ai: I'm here for you. Do you want to talk about what's on your mind?
```

### **Example 2: Document-Based Interaction**

```
User: Uploads "constitution.pdf"
User: What does Article 5 state?
Robert-Ai: Article 5 states that [relevant text extracted from the document].
```

---

## **License**

This project is **licensed under the Apache License 2.0**.

## **Repository**

[Robert-Ai GitHub Repository](https://github.com/nova-fibeyli/Robert-Ai-chatbot.git)

```

```
