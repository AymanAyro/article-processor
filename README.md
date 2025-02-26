# 🌙 Article Processor

![Article Processor Banner](https://github.com/user-attachments/assets/83015b9b-0702-4267-ad03-d5759baad414)

> Transform articles into markdown and structured metadata effortlessly with AI-powered processing.

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![PyQt5](https://img.shields.io/badge/PyQt5-5.15.2-brightgreen)](https://pypi.org/project/PyQt5/)
[![LangChain](https://img.shields.io/badge/LangChain-0.1.0-orange)](https://python.langchain.com/docs/get_started/introduction)
[![Google Generative AI](https://img.shields.io/badge/Google%20Generative%20AI-API-4285F4)](https://ai.google.dev/)

## 📖 Overview

Article Processor is a sophisticated NLP tool that leverages Google's Generative AI to transform raw articles into beautifully formatted Markdown and structured JSON metadata. This tool preserves the original content while adding professional formatting and extracting key information for organized content management.

### Key Features

- 🔄 Convert plain text articles to formatted Markdown
- 📊 Extract metadata (title, author, date, description) into JSON
- 🖼️ Include and manage article images
- 📝 Maintain the original content and tone
- 🧠 Powered by Google's Gemini AI (via LangChain)
- 🎨 User-friendly PyQt5 GUI interface
- 🔍 Few-shot learning for improved output quality

## 🖥️ Screenshots

### Main Application Interface
![Main Interface](https://github.com/user-attachments/assets/a6234a8a-d249-44c0-b9d4-c63e0d3eebd1)
*The main interface showing the input panel, processing controls, and output panels*

### Processing Result
![Processing Result](https://github.com/user-attachments/assets/98ef19c8-d844-44e2-b0e1-ff19d2b2d27d)
*Example of an article processed with markdown formatting and extracted metadata*

## 🚀 Installation

### Prerequisites
- Python 3.7+
- Google AI API key

### Setup

1. Clone the repository:
```bash
git clone https://github.com/your-username/article-processor.git
cd article-processor
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

1. **Input**: Paste your article text into the application
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
فيه ميزة مفيدة جداً في أغلب أنظمة الملفات مفيش كتير يعرفوها اسمها symbolic links.
الخاصية دي بتعمل زي بورتال كدة يشاور على مكان ملف من مكان تاني، حاجة عاملة زي الـ shortcut كدة بس بتشتغل مع البرامج والألعاب والويندوز بشكل عام.
أنا إستخدمت الخاصية دي عشان ألعب Starfield من غير stutters كل شوية، عشان حجمها كبير ومفيش مكان يكفيها في أي SSD واحد عندي... روحت قسّمت اللعبة على هاردين مختلفين واتنين SSD مختلفين
يعني اللعبة كانت شغالة وبتـ load من 4 أجهزة تخزين مختلفة 😅
// هفصّلك أكتر
فيه أمر في ويندوز اسمه mklink بيخليك تعمل اللينكات دي، متشيلش هم الأوامر هقولك على طريقة سهلة في الآخر.
فيه كذا نوع من اللينكات، أهمهم هما الـ Symbolic link والـ Hard link
الـ symbolic link اسمه برضه soft link، بيشتغل في طبقة السوفتوير، بيعمل ملف يشاور على ملف تاني والملف التاني ده بيشاور على مكان الداتا الفيزيائي في الهارد.
أما الـ Hard link فهو مدعوم من كل أنظمة التشغيل تقريباً (القديمة خصوصاً) ومدعوم في نظام ملفات Fat32، بيعمل ملف يشاور على مكان الداتا الفيزيائي مباشرةً.
// اللينكات دي ممكن تستخدمها إستخدامات كتيرة جداً
- ممكن مثلاً لو عندك ملف كبير وفيه برنامجين مختلفين بيستخدموه تقوم عامل لينك منه للبرنامج التاني بدل ما تنسخ الملف وياخد مساحة زيادة.
- ممكن زي ما أنا عملت تاخد ملف من لعبة وتحطه في هارد تاني وتعمل لينك منه لمكان اللعبة الأصلي.
- ممكن مثلاً تنقل فولدر برنامج سطبته في الـ C لأي مكان تاني براحتك وترجع تعمل لينك للمكان الأصلي في الـ C، البرنامج ولا هياخد باله من حاجة وهيشتغل عادي.
// فيه إستخدامات تانية كتيرة مش هخلص لو فضلت أحكي فيها فخليني أخش عالتنبيهات
* السوفت لينك بيشتغل من الكيرنال، فمينفعش تستعمله مع أي لعبة فيها Anti-cheat
* متنقلش ملفات السيستيم، فولدر اليوزر، فولدر Downloads، ولا حتى فولدر temp، حصلت مشاكل كتيرة لما جربت كدة.
بس كدة 😅
* جرب اللي عاوز تجربه على ملف ملهوش لازمة الأول (مثلاً هيحصل إيه لو مسحت اللينك؟ هل الملف هيتمسح؟ جرب وشوف) وبعدين جرب انقل برامجك وألعابك وملفاتك التقيلة.
// الطريقة بكل بساطة:
1- سيرش عن برنامج: Link Shell Extension (LSE) وحمله وسطبه.
2- دوس كليك يمين على أي ملف أو فولدر عايز تعمله لينك.
3- اختار Pick Link Source.
4- روح للمكان اللي عايز تحط اللينك فيه (اعتبر نفسك بتلعب لعبة بورتال😂).
5- دوس كليك يمين في حتة فاضية واختار Drop As اختار Symbolic link.
6- استمتع؟ استفيد؟ انبسط؟ اعمل اللي تعمله 😅
* بكرر، جرب على ملف ملهوش لازمة الأول
* لأصحاب ويندوز 11، خيارات كليك يمين اللي أنا قولتها دي هتلاقيها في Show more options
```

### Output (Markdown)
```markdown
فيه ميزة مفيدة جداً في أغلب أنظمة الملفات مفيش كتير يعرفوها اسمها **Symbolic Links**.

الخاصية دي بتعمل زي بورتال كدة يشاور على مكان ملف من مكان تاني، حاجة عاملة زي الـ Shortcut كدة بس بتشتغل مع البرامج والألعاب والويندوز بشكل عام.

أنا إستخدمت الخاصية دي عشان ألعب Starfield من غير stutters كل شوية، عشان حجمها كبير ومفيش مكان يكفيها في أي SSD واحد عندي... روحت قسّمت اللعبة على هاردين مختلفين واتنين SSD مختلفين.
يعني اللعبة كانت شغالة وبتـ load من 4 أجهزة تخزين مختلفة.

## يعني إيه Symbolic Links؟

فيه أمر في ويندوز اسمه `mklink` بيخليك تعمل اللينكات دي، متشيلش هم الأوامر هقولك على طريقة سهلة في الآخر.

فيه كذا نوع من اللينكات، أهمهم هما الـ **Symbolic link** والـ **Hard link**.

- الـ Symbolic link اسمه برضه soft link، بيشتغل في طبقة السوفتوير، بيعمل ملف يشاور على ملف تاني والملف التاني ده بيشاور على مكان الداتا الفيزيائي في الهارد.
- أما الـ Hard link فهو مدعوم من كل أنظمة التشغيل تقريباً (القديمة خصوصاً) ومدعوم في نظام ملفات Fat32، بيعمل ملف يشاور على مكان الداتا الفيزيائي مباشرةً.

## استخدامات الـ Symbolic Links:

- ممكن مثلاً لو عندك ملف كبير وفيه برنامجين مختلفين بيستخدموه تقوم عامل لينك منه للبرنامج التاني بدل ما تنسخ الملف وياخد مساحة زيادة.
- ممكن زي ما أنا عملت تاخد ملف من لعبة وتحطه في هارد تاني وتعمل لينك منه لمكان اللعبة الأصلي.
- ممكن مثلاً تنقل فولدر برنامج سطبته في الـ C لأي مكان تاني براحتك وترجع تعمل لينك للمكان الأصلي في الـ C، البرنامج ولا هياخد باله من حاجة وهيشتغل عادي.

## تنبيهات مهمة:

* السوفت لينك بيشتغل من الكيرنال، فمينفعش تستعمله مع أي لعبة فيها Anti-cheat
* متنقلش ملفات السيستيم، فولدر اليوزر، فولدر Downloads، ولا حتى فولدر temp، حصلت مشاكل كتيرة لما جربت كدة.
* جرب اللي عاوز تجربه على ملف ملهوش لازمة الأول (مثلاً هيحصل إيه لو مسحت اللينك؟ هل الملف هيتمسح؟ جرب وشوف) وبعدين جرب انقل برامجك وألعابك وملفاتك التقيلة.

## طريقة عمل Symbolic Links بسهولة:

1. سيرش عن برنامج: **Link Shell Extension (LSE)** وحمله وسطبه.
2. دوس كليك يمين على أي ملف أو فولدر عايز تعمله لينك.
3. اختار **Pick Link Source**.
4. روح للمكان اللي عايز تحط اللينك فيه (اعتبر نفسك بتلعب لعبة بورتال).
5. دوس كليك يمين في حتة فاضية واختار **Drop As** اختار **Symbolic link**.
6. استمتع؟ استفيد؟ انبسط؟ اعمل اللي تعمله.

* بكرر، جرب على ملف ملهوش لازمة الأول
* لأصحاب ويندوز 11، خيارات كليك يمين اللي أنا قولتها دي هتلاقيها في Show more options
...
```

### Output (JSON)
```json
{
  "title": "إزاي تستخدم Symbolic Links؟",
  "image_name": "symboic_links",
  "description": "تعرف على ميزة Symbolic Links وكيفية استخدامها لنقل الألعاب والبرامج بين الهاردات المختلفة بدون مشاكل. شرح مبسط مع تحذيرات مهمة.",
  "date": "9 Jan 2025",
  "author": "Creative Geek",
  "filename": "symboic_links",
  "image": "symboic_links.jpg"
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
- Ahmed Taha (Creative Geek) for his contributions in this project 🙏

---

<p align="center">Made with ❤️ for content creators</p>
