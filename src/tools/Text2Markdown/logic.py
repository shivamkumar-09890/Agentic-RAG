from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type

class TextToMarkdownInput(BaseModel):
    text: str = Field(description="The text to convert to markdown")

class TextToMarkdownTool(BaseTool):
    name: str = "text_to_markdown"
    description: str = "Converts plain text into markdown format"
    args_schema: Type[BaseModel] = TextToMarkdownInput

    def _run(self, text: str) -> str:
        try:
            markdown_text = self._convert_to_markdown(text)
            return markdown_text
        except Exception as e:
            return f"Error converting text to markdown: {str(e)}"

    def _convert_to_markdown(self, text: str) -> str:
        """Convert the plain text into markdown format."""
        paragraphs = text.split('\n\n')
        
        markdown_paragraphs = []
        for para in paragraphs:
            # Handling different cases like headings, lists, or plain paragraphs
            if para.startswith('#'):
                markdown_paragraphs.append(para)
            elif para.startswith('- ') or para.startswith('* '):
                markdown_paragraphs.append(para)
            else:
                markdown_paragraphs.append(para)
        
        return '\n\n'.join(markdown_paragraphs)

    def execute(self, text: str) -> str:
        """
        Executes the markdown conversion.
        
        :param text: The input text to convert to markdown.
        :return: Converted markdown text.
        """
        return self._run(text)
        

# Example usage as a tool in your agent
if __name__ == "__main__":
    # Initialize the TextToMarkdownTool
    text_to_markdown_tool = TextToMarkdownTool()

    # Input text to be converted
    text = """# Heading 1

    This is a regular paragraph.
    
    - List item 1
    - List item 2
    
    This is another regular paragraph."""

    # Execute the tool and get the markdown output
    result = text_to_markdown_tool.execute(text=text)
    
    # Print the markdown result
    print("Converted Markdown:")
    print(result)
