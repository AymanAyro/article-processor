# 🌙 Arabic Article Processor

![Arabic Article Processor Banner](https://via.placeholder.com/1200x300)

> Transform Arabic articles into markdown and structured metadata effortlessly with AI-powered processing.

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![PyQt5](https://img.shields.io/badge/PyQt5-5.15.2-brightgreen)](https://pypi.org/project/PyQt5/)
[![LangChain](https://img.shields.io/badge/LangChain-0.1.0-orange)](https://python.langchain.com/docs/get_started/introduction)
[![Google Generative AI](https://img.shields.io/badge/Google%20Generative%20AI-API-4285F4)](https://ai.google.dev/)

## 📖 Overview

Arabic Article Processor is a sophisticated NLP tool that leverages Google's Generative AI to transform raw Arabic articles into beautifully formatted Markdown and structured JSON metadata. This tool preserves the original Arabic content while adding professional formatting and extracting key information for organized content management.

### Key Features

- 🔄 Convert plain text Arabic articles to formatted Markdown
- 📊 Extract metadata (title, author, date, description) into JSON
- 🖼️ Include and manage article images
- 📝 Maintain the original Arabic content and tone
- 🧠 Powered by Google's Gemini AI (via LangChain)
- 🎨 User-friendly PyQt5 GUI interface
- 🔍 Few-shot learning for improved output quality

## 🖥️ Screenshots

### Main Application Interface
![Main Interface](https://via.placeholder.com/800x500)
*The main interface showing the input panel, processing controls, and output panels*

### Processing Result
![Processing Result](https://via.placeholder.com/800x500)
*Example of an article processed with markdown formatting and extracted metadata*

## 🚀 Installation

### Prerequisites
- Python 3.7+
- Google AI API key

### Setup

1. Clone the repository:
```bash
git clone https://github.com/your-username/arabic-article-processor.git
cd arabic-article-processor
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your Google AI API key:
```bash
export GOOGLE_API_KEY="your-api-key"  # On Windows: set GOOGLE_API_KEY=your-api-key
```

## 💻 Usage

### Running the GUI Application

```bash
python gui.py
```

### Using the Command Line Interface

```bash
python main_agent.py
```

### Processing Flow

1. **Input**: Paste your Arabic article text into the application
2. **Configure**: Set filename, author, date, and attach an image (optional)
3. **Process**: The AI processes the article, preserving the original content
4. **Review**: Check the markdown and metadata outputs
5. **Save**: Export the results as .md and .json files

## 🧩 Architecture

The application is built with a clean separation of concerns:

- **main_agent.py**: Core processing logic using LangChain and Google's Generative AI
- **gui.py**: User interface built with PyQt5
- **Examples**: Few-shot learning examples for improved AI performance

### How It Works

1. The application loads example pairs (original text → markdown + JSON) to teach the model
2. It constructs a prompt with the examples and your article
3. Google's Generative AI processes the content
4. The results are parsed into markdown and structured JSON

## 📝 Examples

### Input (Raw Article)
```
انفيديا من كام ساعة أعلنت عن كروت RTX 50، في البوست ده هوضحلك شوية حاجات عشان متتغفلش وكمان هشرحلك ايه الجديد وايه اللي المفروض تهتم بيه.
لو معاك أي كارت قديم من كروت RTX ممكن البوست ده يهمك برضه...
```

### Output (Markdown)
```markdown
انفيديا من كام ساعة أعلنت عن كروت RTX 50، في البوست ده هوضحلك شوية حاجات عشان متتغفلش وكمان هشرحلك ايه الجديد وايه اللي المفروض تهتم بيه.

لو معاك أي كارت قديم من كروت RTX ممكن البوست ده يهمك برضه

## الأول نتكلم شوية عن DLSS 4

زي ما "طوب الأرض" كان متوقع، انفيديا عملت Frame Generation عن طريق الـ Extrapolation بدل الـ Interpolation.

يعني الأول كانت التقنية دي:
...
```

### Output (JSON)
```json
{
  "title": "انفيديا تعلن عن كروت RTX 50: كل ما تحتاج معرفته",
  "image": "nvidia-rtx-50.jpg",
  "description": "شرح مفصل عن إعلان انفيديا لكروت RTX 50 الجديدة، مع تحليل لتقنية DLSS 4 وميزات الكروت",
  "date": "2023-01-10",
  "author": "Tech Blogger"
}
```

## 🛠️ Customization

### Adding New Examples

To improve the AI's output quality, you can add new examples:

1. Place original text in `data/your-example.txt`
2. Place corresponding markdown in `data/your-example.md`
3. Place corresponding JSON in `data/your-example.json`
4. Update the `example_names` list in `main_agent.py`

### Adjusting the Model

You can modify the `process_article` function in `main_agent.py` to use different Google AI models:

```python
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")  # Change model here
```

## 📈 Future Enhancements

- [ ] Support for batch processing multiple articles
- [ ] Integration with content management systems
- [ ] Enhanced metadata extraction (tags, categories)
- [ ] Direct publishing to popular blogging platforms
- [ ] Support for additional languages besides Arabic

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- [Google Generative AI](https://ai.google.dev/) for the powerful language model
- [LangChain](https://python.langchain.com/) for the AI framework
- [PyQt5](https://pypi.org/project/PyQt5/) for the GUI framework
- All contributors who have helped shape this project

---

<p align="center">Made with ❤️ for Arabic content creators</p>
