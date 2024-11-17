import streamlit as st
import pandas as pd
import requests
import json
import plotly.express as px
import google.generativeai as genai
from abc import ABC, abstractmethod

# Abstract base class for LLM providers
class LLMProvider(ABC):
    @abstractmethod
    def generate_response(self, prompt: str) -> str:
        pass

class OllamaProvider(LLMProvider):
    def __init__(self, model: str = "llama2"):
        self.model = model
        self.url = "http://localhost:11434/api/generate"
    
    def generate_response(self, prompt: str) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        
        try:
            response = requests.post(self.url, json=payload)
            response.raise_for_status()
            return response.json()['response']
        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to Ollama: {str(e)}")
            return None

class GeminiProvider(LLMProvider):
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def generate_response(self, prompt: str) -> str:
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            st.error(f"Error connecting to Gemini: {str(e)}")
            return None

class DataAnalyzer:
    def __init__(self, df: pd.DataFrame, llm_provider: LLMProvider):
        self.df = df
        self.llm_provider = llm_provider
    
    def generate_analysis_prompt(self, question: str, context: str = None) -> str:
        df_info = f"Dataset Summary:\n"
        df_info += f"Columns: {', '.join(self.df.columns)}\n"
        df_info += f"Total Rows: {len(self.df)}\n\n"
        
        df_info += "Statistical Summary:\n"
        df_info += self.df.describe().to_string()
        
        df_info += "\n\nSample Data:\n"
        df_info += self.df.head().to_string()
        
        prompt = f"""You are a data analyst examining political survey data. Here's the context:

{df_info}

Additional Context: {context if context else 'No additional context provided'}

Question: {question}

Please provide a detailed analysis that includes:
1. Direct answers to the specific question
2. Relevant statistical insights
3. Notable patterns or trends
4. Important demographic variations
5. Historical comparisons where applicable

Format your response in a clear, structured manner using markdown formatting."""

        return prompt

    def analyze(self, question: str, context: str = None) -> str:
        prompt = self.generate_analysis_prompt(question, context)
        return self.llm_provider.generate_response(prompt)

class Visualizer:
    @staticmethod
    def create_visualization(df: pd.DataFrame, analysis_type: str):
        if analysis_type == "gender_distribution":
            fig = px.bar(df, x='Gender', y='Support', color='Party',
                        barmode='group', title='Party Support by Gender')
            return fig
        return None

def initialize_session_state():
    if 'gemini_api_key' not in st.session_state:
        st.session_state.gemini_api_key = ""

def render_sidebar():
    st.sidebar.header("Configuration")
    
    provider = st.sidebar.radio(
        "Select AI Provider",
        ["Ollama", "Gemini Pro"]
    )
    
    model = None
    if provider == "Ollama":
        model = st.sidebar.selectbox(
            "Select Ollama Model",
            ["llama2", "llama3.2:latest", "codellama"],
            index=0
        )
    else:
        api_key = st.sidebar.text_input(
            "Enter Gemini API Key",
            value=st.session_state.gemini_api_key,
            type="password"
        )
        st.session_state.gemini_api_key = api_key
    
    return provider, model

def main():
    st.title("Political Survey Data Analysis")
    
    initialize_session_state()
    provider, model = render_sidebar()
    
    uploaded_file = st.file_uploader("Upload your CSV file", type=['csv'])
    
    if uploaded_file is not None:
        try:
            df = pd.DataFrame(pd.read_csv(uploaded_file))
            
            st.subheader("Dataset Preview")
            st.dataframe(df.head())
            
            analysis_type = st.selectbox(
                "Select Analysis Type",
                ["Gender-based Analysis", "Historical Comparison", "Demographic Trends", "Custom Query"]
            )
            
            context = st.text_area(
                "Add any additional context (optional)",
                height=100,
                placeholder="Example: Focus on specific demographic trends or historical patterns..."
            )
            
            # Predefined questions mapping
            questions = {
                "Gender-based Analysis": "What are the key differences in political party support between genders?",
                "Historical Comparison": "How has party support changed compared to the 2019 modeled data?",
                "Demographic Trends": "What are the main demographic trends across all parties?",
            }
            
            question = (questions.get(analysis_type) or 
                       st.text_area("Enter your specific analysis question",
                                  height=100,
                                  placeholder="Example: What is the correlation between gender and party support?"))
            
            if st.button("Analyze"):
                # Initialize appropriate LLM provider
                if provider == "Ollama":
                    llm_provider = OllamaProvider(model)
                else:
                    if not st.session_state.gemini_api_key:
                        st.error("Please enter your Gemini API key in the sidebar")
                        return
                    llm_provider = GeminiProvider(st.session_state.gemini_api_key)
                
                with st.spinner("Analyzing data..."):
                    analyzer = DataAnalyzer(df, llm_provider)
                    analysis = analyzer.analyze(question, context)
                    
                    if analysis:
                        st.subheader("Analysis Results")
                        st.markdown(analysis)
                        
                        if analysis_type == "Gender-based Analysis":
                            try:
                                fig = Visualizer.create_visualization(df, "gender_distribution")
                                if fig:
                                    st.plotly_chart(fig)
                            except Exception as e:
                                st.warning("Could not create visualization with the current data format")
                        
                        st.download_button(
                            label="Download Analysis",
                            data=analysis,
                            file_name="political_analysis.txt",
                            mime="text/plain"
                        )
                        
        except Exception as e:
            st.error(f"Error processing the file: {str(e)}")
            
    else:
        st.info("""
        ## Instructions
        1. Upload a CSV file containing political survey data
        2. Select your preferred AI provider (Ollama or Gemini Pro)
        3. Select the type of analysis you want to perform
        4. Add any relevant context
        5. Click 'Analyze' to generate insights
        
        ### Expected Data Format
        Your CSV should include columns for:
        - Gender
        - Party support percentages
        - Historical data (if available)
        - Other demographic information
        """)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    ### Tips for Better Analysis:
    - Ensure your CSV is properly formatted
    - Add relevant context for more precise analysis
    - Try different analysis types for comprehensive insights
    - Use custom queries for specific investigations
    
    Note: For Ollama, ensure the service is running locally. For Gemini Pro, you'll need an API key.
    """)

if __name__ == "__main__":
    main()