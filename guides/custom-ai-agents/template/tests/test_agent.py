"""Tests for the AI Agent Template."""

import pytest
import os
import tempfile
from unittest.mock import Mock, patch
from agent import TemplateAgent
from config import AgentConfig


class TestAgentConfig:
    """Test configuration management."""
    
    def test_from_env_with_minimal_config(self):
        """Test configuration with minimal environment variables."""
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'}):
            config = AgentConfig.from_env()
            assert config.openai_api_key == 'test_key'
            assert config.model == 'gpt-3.5-turbo'
            assert config.max_tokens == 500
    
    def test_from_env_missing_api_key(self):
        """Test configuration fails without API key."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="OPENAI_API_KEY"):
                AgentConfig.from_env()
    
    def test_validation(self):
        """Test configuration validation."""
        config = AgentConfig(openai_api_key="test_key")
        config.validate()  # Should not raise
        
        config.max_tokens = -1
        with pytest.raises(ValueError, match="max_tokens"):
            config.validate()


class TestTemplateAgent:
    """Test the template agent functionality."""
    
    @pytest.fixture
    def config(self):
        """Create a test configuration."""
        return AgentConfig(
            openai_api_key="test_key",
            memory_file=tempfile.mktemp(suffix=".json")
        )
    
    @pytest.fixture
    def agent(self, config):
        """Create a test agent."""
        with patch('agent.OpenAI'):
            return TemplateAgent(config)
    
    def test_initialization(self, agent):
        """Test agent initialization."""
        assert len(agent.messages) == 1  # System message
        assert agent.messages[0]["role"] == "system"
    
    def test_add_message(self, agent):
        """Test adding messages to conversation."""
        agent.add_message("user", "Hello")
        assert len(agent.messages) == 2
        assert agent.messages[-1]["role"] == "user"
        assert agent.messages[-1]["content"] == "Hello"
    
    def test_memory_truncation(self, agent):
        """Test memory truncation functionality."""
        # Set a small limit
        agent.config.max_memory_messages = 3
        
        # Add messages beyond limit
        for i in range(5):
            agent.add_message("user", f"Message {i}")
        
        # Should keep system message + 2 recent messages
        assert len(agent.messages) == 3
        assert agent.messages[0]["role"] == "system"
        assert "Message 3" in agent.messages[-2]["content"]
        assert "Message 4" in agent.messages[-1]["content"]
    
    def test_clear_memory(self, agent):
        """Test memory clearing."""
        agent.add_message("user", "Hello")
        agent.clear_memory()
        
        assert len(agent.messages) == 1
        assert agent.messages[0]["role"] == "system"
    
    @patch('agent.json.dump')
    @patch('builtins.open', create=True)
    def test_save_memory(self, mock_open, mock_json_dump, agent):
        """Test memory saving."""
        agent.save_memory()
        mock_open.assert_called_once()
        mock_json_dump.assert_called_once()
    
    @patch('agent.json.load')
    @patch('builtins.open', create=True)
    def test_load_memory(self, mock_open, mock_json_load, agent):
        """Test memory loading."""
        mock_json_load.return_value = [{"role": "system", "content": "test"}]
        agent.load_memory()
        assert len(agent.messages) == 1
    
    @patch('agent.OpenAI')
    def test_chat_response(self, mock_openai, config):
        """Test chat functionality."""
        # Mock OpenAI response
        mock_response = Mock()
        mock_response.choices[0].message.content = "Hello there!"
        mock_openai.return_value.chat.completions.create.return_value = mock_response
        
        agent = TemplateAgent(config)
        response = agent.chat("Hello")
        
        assert response == "Hello there!"
        assert len(agent.messages) == 3  # system + user + assistant


if __name__ == "__main__":
    pytest.main([__file__])