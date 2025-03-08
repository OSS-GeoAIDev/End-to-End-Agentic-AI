import streamlit as st
import json
from src.langgraphagenticai.ui.streamlitui.loadui import LoadStreamlitUI
from src.langgraphagenticai.LLMS.groqllm import GroqLLM
from src.langgraphagenticai.graph.graph_builder import GraphBuilder
from src.langgraphagenticai.ui.streamlitui.display_result import DisplayResultStreamlit

# Main function Start

def load_langgraph_agenticai_app():
    """
    Loads and runs the LangGraph AgenticAI application with Streamlit UI.
    This function initializes the UI, handles user input, configures the LLM model,
    sets up the graph based on the selected use case, and displays the output while 
    implementing exception handling for robustness.
    """

    ui = LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()

    if not user_input:
        st.error("Error : Failed to load UI")
        return
    
    # Text input for user message
    if st.session_state.IsFetchButtonClicked:
        user_message = st.session_state.timeframe     
    else: 
          user_message = st.chat_input("Enter your message:")

    if user_message:
        try:
            #configure LLM
            obj_llm_config = GroqLLM(user_controls_input=user_input)
            model = obj_llm_config.get_llm_model()

            if not model:
                st.error("Initialize the LLM Model")
                return
            

            #initialize and setup the graph based usecase

            usecase = user_input.get('selected_usecase')

            if not usecase:
                st.error("Error: No usecase selected")
                return
            
            #Graph Builder
            graph_builder = GraphBuilder(model)
            try:
                graph = graph_builder.setup_graph(usecase)
                DisplayResultStreamlit(usecase,graph,user_message).display_result_on_ui()
            except Exception as e:
                st.error(f"Error : line 52 failed {e}")
                return
        
        except Exception as e:
            raise ValueError(f"Error occured with Exception: {e}")
        
        
         

        