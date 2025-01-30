import os
import traceback
import subprocess
from typing import Optional

class CodeDebugTool:
    def __init__(self):
        pass
    
    def run_code(self, code: str, language: str, debug: bool = False):
        """
        Execute the provided code based on the language type and debug it if an error occurs.
        :param code: Code to execute
        :param language: The programming language of the code (e.g., 'python', 'cpp', 'java', 'js', 'html', 'markdown')
        :param debug: Whether to enter interactive debugging on error
        """
        try:
            if language == 'python':
                self._run_python(code, debug)
            elif language == 'cpp':
                self._run_cpp(code)
            elif language == 'java':
                self._run_java(code)
            elif language == 'js':
                self._run_js(code)
            elif language == 'html':
                self._run_html(code)
            elif language == 'css':
                self._run_css(code)
            elif language == 'markdown':
                self._run_markdown(code)
            else:
                print(f"Unsupported language: {language}")
        except Exception as e:
            print(f"Error: {str(e)}")
            traceback.print_exc()

    def _run_python(self, code: str, debug: bool):
        try:
            exec(code)
        except Exception as e:
            print(f"Python Error: {str(e)}")
            traceback.print_exc()
            if debug:
                import pdb; pdb.set_trace()

    def _run_cpp(self, code: str):
        with open("temp.cpp", "w") as file:
            file.write(code)
        
        try:
            # Compile C++ code
            compile_proc = subprocess.run(['g++', 'temp.cpp', '-o', 'temp'], capture_output=True)
            if compile_proc.returncode != 0:
                print("C++ Compilation Error:")
                print(compile_proc.stderr.decode())
                return

            # Execute compiled C++ code
            exec_proc = subprocess.run(['./temp'], capture_output=True)
            if exec_proc.returncode != 0:
                print("C++ Execution Error:")
                print(exec_proc.stderr.decode())
            else:
                print("C++ Output:")
                print(exec_proc.stdout.decode())
        except Exception as e:
            print(f"C++ Error: {str(e)}")
            traceback.print_exc()

    def _run_java(self, code: str):
        with open("Temp.java", "w") as file:
            file.write(code)
        
        try:
            # Compile Java code
            compile_proc = subprocess.run(['javac', 'Temp.java'], capture_output=True)
            if compile_proc.returncode != 0:
                print("Java Compilation Error:")
                print(compile_proc.stderr.decode())
                return

            # Execute compiled Java code
            exec_proc = subprocess.run(['java', 'Temp'], capture_output=True)
            if exec_proc.returncode != 0:
                print("Java Execution Error:")
                print(exec_proc.stderr.decode())
            else:
                print("Java Output:")
                print(exec_proc.stdout.decode())
        except Exception as e:
            print(f"Java Error: {str(e)}")
            traceback.print_exc()

    def _run_js(self, code: str):
        try:
            exec_proc = subprocess.run(['node', '-e', code], capture_output=True)
            if exec_proc.returncode != 0:
                print("JavaScript Execution Error:")
                print(exec_proc.stderr.decode())
            else:
                print("JavaScript Output:")
                print(exec_proc.stdout.decode())
        except Exception as e:
            print(f"JavaScript Error: {str(e)}")
            traceback.print_exc()

    def _run_html(self, code: str):
        try:
            with open("temp.html", "w") as file:
                file.write(code)
            print("HTML code executed successfully. Open 'temp.html' in a browser to see the result.")
        except Exception as e:
            print(f"HTML Error: {str(e)}")
            traceback.print_exc()

    def _run_css(self, code: str):
        try:
            with open("temp.css", "w") as file:
                file.write(code)
            print("CSS code executed successfully. Link 'temp.css' to an HTML file to view the result.")
        except Exception as e:
            print(f"CSS Error: {str(e)}")
            traceback.print_exc()

    def _run_markdown(self, code: str):
        try:
            import markdown
            html = markdown.markdown(code)
            print("Markdown rendered as HTML:")
            print(html)
        except Exception as e:
            print(f"Markdown Error: {str(e)}")
            traceback.print_exc()

# Example usage:
if __name__ == "__main__":
    code_input = """
print("Hello, World!")  # Python Example
"""
    tool = CodeDebugTool()
    tool.run_code(code_input, language='python', debug=True)
    
    cpp_code = """
#include <iostream>
using namespace std;

int main() {
    cout << "Hello, World!" << endl;
    return 0;
}
"""
    tool.run_code(cpp_code, language='cpp')
