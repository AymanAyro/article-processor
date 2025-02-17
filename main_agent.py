import os
from pathlib import Path
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate, FewShotPromptTemplate, PromptTemplate
import json
import getpass

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google AI API key: ")

class ArticleOutput(BaseModel):
    markdown: str = Field(description="The article content converted to markdown format")
    json_metadata: dict = Field(description="Metadata about the article in JSON format")
    user_queries: List[str] = Field(default_factory=list, description="List of queries needed from the user")

class Example(BaseModel):
    input: str
    markdown_output: str
    json_output: dict

def load_examples() -> List[Dict[str, Any]]:
    """
    Load example files to use for few-shot learning.
    Expects .txt files for input and corresponding .md and .json files for output.
    """
    example_names = [
        "nomacs-image-viewer",
        "fontPreviewer"
    ]
    
    examples = []
    for name in example_names:
        txt_path = Path(f"data/{name}.txt")  # Original article text
        md_path = Path(f"data/{name}.md")    # Processed markdown
        json_path = Path(f"data/{name}.json") # Metadata
        
        if all(p.exists() for p in [txt_path, md_path, json_path]):
            with open(txt_path, 'r', encoding='utf-8') as f:
                original_text = f.read()
            with open(md_path, 'r', encoding='utf-8') as f:
                md_content = f.read()
            with open(json_path, 'r', encoding='utf-8') as f:
                json_content = f.read()
                
            examples.append({
                "input": original_text,            # Use original text as input
                "markdown_output": md_content,     # Use processed markdown as output
                "json_output": json_content        # Use metadata as output
            })
        else:
            missing_files = [p for p in [txt_path, md_path, json_path] if not p.exists()]
            print(f"Warning: Missing files for example '{name}': {missing_files}")
    
    if not examples:
        raise ValueError("No complete examples found. Each example requires .txt, .md, and .json files.")
    
    return examples

def create_prompt_template(article_date: Optional[str] = None) -> FewShotPromptTemplate:
    """Create a FewShotPromptTemplate with example formatting."""
    
    # Define how each example should be formatted
    example_template = """
Original article:
{input}

Processed markdown:
{markdown_output}

Generated metadata:
{json_output}
"""
    example_prompt = PromptTemplate(
        input_variables=["input", "markdown_output", "json_output"],
        template=example_template
    )
    
    # Create the prefix (system prompt)
    prefix = """You convert articles to markdown and json pairs. Here are some examples of the expected input and output format.

        Your response must be a valid JSON object with the following required fields:
        1. "markdown": a string containing the article in markdown format
        2. "json_metadata": an object with metadata keys
        3. "user_queries": a list of strings (can be empty if no queries are needed)

        For the markdown:
        - Retain the same words, details, and context length.
        - Add markdown formatting (#,*, ```, etc) and marks to make it suitable for a blog post.
        - Avoid starting a line with an English character unless it's the same in original text.
        - If the article mentions something in a comment, note this as a query.
        - Remove any lines asking for comments.
        - Replace article references with "link to be added", don't replace other links.
        - Do NOT start the md file with the title, just start with the same words in the original text.

        For the json_metadata object, include these keys:
        {{{{
            "title": "",
            "image": "",
            "description": "",
            "date": "{date}",
            "author": ""
        }}}}

        Extract values from the article if available. Use the provided date if given, or an appropriate date format if not.
        If title and description aren't explicitly mentioned, create them based on the article content.

        **THE ARTICLE SHOULD BE WRITTEN IN ARABIC, KEEP THE ORIGINAL TONE**"""
    if article_date:
        prefix = prefix.format(date=article_date)
    else:
        prefix = prefix.format(date="")
        
    # Create suffix (the actual task prompt)
    suffix = """
Now, process the following article:
{input}

Provide the markdown content and JSON metadata in the required format."""

    # Load and format examples
    examples = load_examples()
    
    # Create the FewShotPromptTemplate
    few_shot_prompt = FewShotPromptTemplate(
        examples=examples,
        example_prompt=example_prompt,
        prefix=prefix,
        suffix=suffix,
        input_variables=["input"],
        example_separator="\n\n---\n\n"
    )
    
    return few_shot_prompt

def process_article(article_text: str, article_date: str = None):
    """Process an article using few-shot learning approach."""
    # Initialize the LLM
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    
    # Create the prompt template
    few_shot_prompt = create_prompt_template(article_date)
    
    # Create the output parser
    output_parser = PydanticOutputParser(pydantic_object=ArticleOutput)
    
    # Create the chain
    chain = few_shot_prompt | llm | output_parser
    
    # Run the chain
    result = chain.invoke({"input": article_text})
    return result

def save_files(output: ArticleOutput, base_filename: str) -> tuple[Path, Path]:
    """Save the processed output to files."""
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    markdown_path = output_dir / f"{base_filename}.md"
    with open(markdown_path, "w", encoding="utf-8") as f:
        f.write(output.markdown)
    
    json_path = output_dir / f"{base_filename}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(output.json_metadata, f, ensure_ascii=False, indent=2)
    
    return markdown_path, json_path

# Example usage
if __name__ == "__main__":
    sample_article = """
    انفيديا من كام ساعة أعلنت عن كروت RTX 50، في البوست ده هوضحلك شوية حاجات عشان متتغفلش وكمان هشرحلك ايه الجديد وايه اللي المفروض تهتم بيه.
لو معاك أي كارت قديم من كروت RTX ممكن البوست ده يهمك برضه
الأول نتكلم شوية عن DLSS 4
زي ما "طوب الأرض" كان متوقع، انفيديا عملت Frame Generation عن طريق الـ Extrapolation بدل الـ Interpolation.
يعني الأول كانت التقنية دي:
بترندر الفريم الحالي وليكن فريم رقم 1 وتعرضه على الشاشة (كدة فريم 1 معروض خلي بالك)، ثم ترندر الفريم الجاي اللي هو رقم 2 من غير ما يتعرض على الشاشة، وبعدين تعمل فريم بينهم يبقى رقمه 1.5 مثلاً، ثم تعرض الفريم 1.5 اللي هي عملته ده، ثم تعرض الفريم 2، وتستمر العملية دي على طول.
ده كان بيعمل مشكلة واضحة جداً، إن استجابة اللعبة بتبقى بطيئة/تقيلة حتى لو شكلها smooth، وده عشان التقنية محتاجة تأخرلك عرض الشاشة عقبال ما تعمل فريمات وسيطة.
الجديد بقى:
إن التقنية دي بقيت بترندر وتعرض فريم 1 وترندر وتعرض فريم 2 عادي جداً
ثم تنتج فريم 3 عن طريق التنبؤ بيه!
يعني من غير ما تعمل حسابات الإضاءة من تاني ولا تعمل حسابات الفيزياء ولا أي حاجة
مجرد تشوف آخر فريمين وتتوقع التالت شكله عامل ازاي (دي حاجة بديهية أوي يعني معرفش إيه اللي أخرهم كدة بصراحة 😭)
--
كروت RTX 50 كلها هتقدر تنتج عدد كبير من الفريمات عن طريق الـ Frame Generation (انفيديا بتقول 3 إنتاج و1 حساب لكل 4 فريمات معروضة عالشاشة)
انفيديا بتقول إنهم عملوا تعديل في الهاردوير بتاع الـ FG عشان يخلوه يقدر ينتج فريمات كتيرة بحسبة واحدة بس، وانهم استبدلوا وحدة حساب الموشن فيكتورز بموديل AI يشتغل على الـ tensor cores.
كروت RTX 40 كسبت نفس الميزة برضه بس هتقدر تنتج فريم واحد بس من المستقبل مش تلاتة.
انفيديا بتقول انهم حاولوا يخلوه ينتج أكتر من فريم لكن الهاردوير بتاعه محتاج يعمل حسبة الموشن فيكتورز كل مرة ينتج فيها فريم جديد عشان كدة لو زودوا عدد الفريمات الآداء هيبقى أقل من لما تطفي الخاصية خالص 💀.
كروت 30 و 20 ملهومش حاجة من الـ Frame Generation 😅
بس خاصية DLSS كاملة على كل الكروت هتستلم موديلات جديدة هتشتغل على أي لعبة فيها DLSS
الموديل الجديد معمول بـ Transformer Architecture بدل الـ CNN
أيوة ترانسفورمر زي شات جيبيتي كدة 🤣
ميزته انه بيقدر يشوف الصورة كلها ويربط التفاصيل ببعض، على عكس الـ CNN اللي بيعالج كل جزء من الصورة لوحده
جودته المفروض تكون أفضل بكتير جداً من الأول والمفروض يخلصنا من الفازلين اللي الألعاب بتدهن بيه الشاشة اليومين دول.
كمان هيبقى عندك القدرة تستبدل الـ DLSS القديم بالجديد عن طريق أبلكيشن انفيديا في أي فيها DLSS.
----------------
نيجي بقى للمهم أوي، انفيديا بتقول ان الـ RTX 5070 هيكون بسعر 550 دولار بس هيديك آداء قد الـ 4090!
ده كلام مضلل شوية، هو هيديك الآداء ده فعلاً لكن بالـ DLSS FG عن طريق انه يعمل 3 فريمات أو أكتر من الهوا ويرندر فريم واحد حقيقي.
تقدر تتأكد من الكلام ده عن طريق الجراف اللي نشروه
شوف المقارنة بين الـ 5090 والـ 4090، هتلاقي الزيادة في لعبة Far Cry 6 اللي مطفي فيها الـ DLSS تقدر بحوالي 20% بس.
كذلك في كل الكروت هتلاقي الزيادة بين الجيل اللي فات والجديد من 20% لـ 30% بس.
في الـ AI القصة مختلفتش كتير
لو بصيت عالجراف هتلاقي آداء Flux أعلى بـ 2X من الجيل اللي فات!
لكن ده كلام مضلل برضه لإنك لو بصيت تحت على الفوت برنت هتلاقي إن الموديل شغالة بنصف دقة الحسابات على الـ RTX 5090 اللي هي fp4، بدل fp8 على الـ 4090.
ده هيفرق جداً في الآداء واستهلاك الرام وكمية الحسابات وكل حاجة، طبعاً هيفرق في النتيجة كمان فبالتالي مش هيديك نفس تفاصيل الصور ولا قريب منها حتى.
الـ VRAM نكتة هنسيبها ليوم تاني بس هقول كلمة صغيرة، انفيديا عملت حتة موديل صغنون وظيفته يضغط الداتا بتاعت اللعبة في الـ vram، المبهر إن الموديل ده عنده القدرة يعالج الداتا دي وهي مضغوطة! دي حاجة أول مرة نشوفها عموماً بس لازم نشوف نتايجها بعدين قبل ما نقول حاجة.
تفصيلة إضافية تانية، بيقولوا شغالين على تقنية Reflex 2 Frame warp، مفيش تفاصيل عنها بس الظاهر انها هتغير الفريم بعد ما يترندر عشان يديك آخر حركة بعتها الماوس قبل ما الفريم يوصل للشاشة.
عموماً أنا كنت متوقع حاجات معينة مبهرة أكتر من كدة بس شكلها لسة في المطبخ ومحتاجة تستوي شوية كمان
لو حد مش فاهم حاجة الكومنتات مفتوحة خد راحتك واسأل
والسلام عليكم
    """
    
    result = process_article(sample_article, "2023-01-10")
    md_path, json_path = save_files(result, "ai_article")
    
    print(f"Markdown saved to: {md_path}")
    print(f"JSON saved to: {json_path}")
    
    if result.user_queries:
        print("\nQueries for user:")
        for query in result.user_queries:
            print(f"- {query}")