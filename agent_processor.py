# agent_processor.py

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

def create_prompt_template(article_date: Optional[str] = None, filename: Optional[str] = None, author: Optional[str] = None) -> FewShotPromptTemplate:
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

        ## For the markdown:
        - Retain the same words, details, and context length.
        - **Add proper markdown formatting marks (#,*,etc..) for the article to make it stylish and readable providing headings, bullets, and so on**
        - DON'T use Horizontal Lines (-) at all.
        - Avoid starting a line with an English character unless it's the same in original text.
        - If the article mentions something in a comment, note this as a query.
        - Remove any lines asking for comments or opinions.
        - Replace article references with "link to be added", don't replace other links.
        - Do NOT start the md file with the title, just start with the same words in the original text.
        - Do NOT use weird character objects like emojis or special characters.
        
        ## For the metadata:
        - Use the provided filename for image filename if available (Don't create a filename key)
        - Include the author name if provided
        - Only use the exact date if provided
        - DO NOT guess or make up any values
        - If information isn't explicitly provided, omit the key entirely
        - Never use values (date,author, ..etc.) from example articles
        - Include these keys ONLY:
            "title": "", (provide the title in Arabic)
            "image_name": "", (Don't create this key if not provided)
            "description": "", (provide a brief description in Arabic)
            "date": "", (Don't create this key if not provided)
            "author": "" (Don't create this key if not provided)

        **THE ARTICLE SHOULD BE WRITTEN IN ARABIC, KEEP THE ORIGINAL TONE**"""
        
    # Create suffix with metadata information
    suffix = """
Now, process the following article:
{input}

Additional metadata:"""

    if filename:
        suffix += f"\nFilename for images: {filename}"
    if author:
        suffix += f"\nAuthor: {author}"
    if article_date:
        suffix += f"\nDate: {article_date}"

    suffix += """

Remember:
- Only include metadata fields that are explicitly present
- Use the provided filename for any image references
- Include the author name in metadata if provided
- DO NOT make up any values
- If date wasn't provided, don't include the date field
- Don't copy dates from examples
- *FILTER ANY LINES (-) FROM THE MARKDOWN OUTPUT*

Provide the markdown content and JSON metadata in the required format."""

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

def process_article(article_text: str, article_date: Optional[str] = None, filename: Optional[str] = None, author: Optional[str] = None) -> ArticleOutput:
    """Process an article using few-shot learning approach."""
    # Initialize the LLM
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    
    # Create the prompt template with metadata
    few_shot_prompt = create_prompt_template(article_date, filename, author)
    
    # Create the output parser
    output_parser = PydanticOutputParser(pydantic_object=ArticleOutput)
    
    # Create the chain
    chain = few_shot_prompt | llm | output_parser
    
    # Run the chain
    result = chain.invoke({"input": article_text})
    
    # Post-process the result to ensure metadata correctness
    if hasattr(result, 'json_metadata'):
        # Remove any empty values
        result.json_metadata = {k: v for k, v in result.json_metadata.items() if v and v.strip()}
        
        # Set metadata from provided values
        if filename:
            result.json_metadata['filename'] = filename
        if author:
            result.json_metadata['author'] = author
        if article_date:
            result.json_metadata['date'] = article_date
        elif 'date' in result.json_metadata:
            del result.json_metadata['date']
            
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