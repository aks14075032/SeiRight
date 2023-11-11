# Compliance Checking

This project provides two approaches for compliance checking:

1. **Compliance Check using OpenAI**
   - Utilizes the OpenAI GPT-3.5 Turbo model to check compliance between policy and webpage text.

2. **Compliance Check using Bart CNN** 
   - Uses the transformers library to summarize text and check compliance.
   - Need more work to be done on this method
## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/compliance_checking.git
   cd SeiRight
2. Activate Source Environment
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

3. Install dependencies:
    ```bash
   pip install -r requirements.txt

4. Usage
    ```bash
   Turn Flask Server On (Run Any of two A or B)
   A. Compliance Check using OpenAI
   python compliance_checker_openai.py 
   B. Compliance Check Using Bart CNN
   python compliance_checker_bart_cnn.py 
   
   Call API
   python main.py
